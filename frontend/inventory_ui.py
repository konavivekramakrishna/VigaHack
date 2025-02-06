from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableView, QLabel, QLineEdit, QSizePolicy, QProgressBar, QHBoxLayout
from PySide6.QtCore import Qt, QThread, Signal, QAbstractTableModel, QTimer
from PySide6.QtGui import QFont
import requests
import sys

API_BASE_URL = "http://127.0.0.1:5000"
TIMEOUT_SECONDS = 30  

class InventoryModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 2  

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]["name"] if index.column() == 0 else str(self._data[index.row()]["quantity"])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Name" if section == 0 else "Quantity"
        return None

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

class FetchInventoryThread(QThread):
    data_fetched = Signal(list)
    error_occurred = Signal(str)

    def run(self):
        try:
            response = requests.get(f"{API_BASE_URL}/get-items", timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if data.get("message") == "Items retrieved successfully":
                self.data_fetched.emit(data["data"])
            else:
                self.error_occurred.emit("Error fetching inventory.")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Request timed out. Try again later.")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Network error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {str(e)}")

class AddItemThread(QThread):
    item_added = Signal(bool, str)

    def __init__(self, name, quantity):
        super().__init__()
        self.name = name
        self.quantity = quantity

    def run(self):
        try:
            response = requests.post(
                f"{API_BASE_URL}/add-item",
                json={"name": self.name, "quantity": int(self.quantity)},
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()
            data = response.json()
            if response.status_code == 201 and data.get("message") == "Item added successfully":
                self.item_added.emit(True, "Item added successfully.")
            else:
                self.item_added.emit(False, data.get("error", "Error adding item."))
        except requests.exceptions.Timeout:
            self.item_added.emit(False, "Request timed out. Try again later.")
        except requests.exceptions.RequestException as e:
            self.item_added.emit(False, f"Network error: {str(e)}")
        except Exception as e:
            self.item_added.emit(False, f"Unexpected error: {str(e)}")

class UpdateItemThread(QThread):
    item_updated = Signal(bool, str)

    def __init__(self, name, quantity):
        super().__init__()
        self.name = name
        self.quantity = quantity

    def run(self):
        try:
            response = requests.put(
                f"{API_BASE_URL}/update-quantity",
                json={"name": self.name, "quantity": int(self.quantity)},
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Quantity updated successfully":
                    self.item_updated.emit(True, "Quantity updated successfully.")
                else:
                    self.item_updated.emit(False, data.get("error", "Error updating quantity."))
        except requests.exceptions.Timeout:
            self.item_updated.emit(False, "Request timed out. Try again later.")
        except requests.exceptions.RequestException as e:
            d = response.json()
            self.item_updated.emit(False, f"Error: {str(d.get('error', e))}")
        except Exception as e:
            self.item_updated.emit(False, f"Unexpected error: {str(e)}")

class DeleteItemThread(QThread):
    item_deleted = Signal(bool, str)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        try:
            response = requests.delete(
                f"{API_BASE_URL}/remove-item",
                json={"name": self.name},
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200 and data.get("message") == "Item removed successfully":
                self.item_deleted.emit(True, f"Item {self.name} removed successfully.")
            else:
                self.item_deleted.emit(False, data.get("error", "Error removing item."))
        except requests.exceptions.Timeout:
            self.item_deleted.emit(False, "Request timed out. Try again later.")
        except requests.exceptions.RequestException as e:
            d = response.json()
            self.item_deleted.emit(False,   f"Error: {str(d.get('error', e))}")
        except Exception as e:
            self.item_deleted.emit(False, f"Unexpected error: {str(e)}")

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(300, 300, 1000, 600)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Create a layout to center the table horizontally
        table_layout = QHBoxLayout()
        table_layout.addStretch()  # Adds flexible space before the table

        self.table = QTableView()
        self.table.setFont(QFont("Arial", 12))
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumWidth(400)  # Ensuring a wider table

        table_layout.addWidget(self.table, 2)  # Stretch factor to make table take more space
        table_layout.addStretch()  # Adds flexible space after the table

        self.layout.addLayout(table_layout)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        form_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")

        self.add_button = QPushButton("Add Item")
        self.add_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 10px;")
        self.add_button.clicked.connect(self.add_item)

        self.update_button = QPushButton("Update Item")
        self.update_button.setStyleSheet("background-color: #FF9800; color: white; border-radius: 5px; padding: 10px;")
        self.update_button.clicked.connect(self.update_item)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.setStyleSheet("background-color: #F44336; color: white; border-radius: 5px; padding: 10px;")
        self.delete_button.clicked.connect(self.delete_item)

        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Quantity:"))
        form_layout.addWidget(self.quantity_input)
        form_layout.addWidget(self.add_button)
        form_layout.addWidget(self.update_button)
        form_layout.addWidget(self.delete_button)

        self.layout.addLayout(form_layout)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px;")
        self.refresh_button.clicked.connect(self.load_inventory)
        self.layout.addWidget(self.refresh_button)

        self.model = InventoryModel([])
        self.table.setModel(self.model)

        # Ensure the table stretches to fit the width dynamically
        self.table.setColumnWidth(0, 400)  
        self.table.setColumnWidth(1, 300)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.load_inventory()

    def load_inventory(self):
        self.progress_bar.setVisible(True)
        self.status_label.setText("Fetching inventory...")
        self.worker = FetchInventoryThread()
        self.worker.data_fetched.connect(self.update_table)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def update_table(self, data):
        self.progress_bar.setVisible(False)
        self.status_label.setText("Inventory loaded successfully.")
        self.model.update_data(data)
        self.table.resizeColumnsToContents()

    def handle_error(self, message):
        self.progress_bar.setVisible(False)
        self.status_label.setText(message)

    def add_item(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not quantity.isdigit() or int(quantity) <= 0:
            self.status_label.setText("Invalid input. Enter a valid name and quantity.")
            QTimer.singleShot(2000, lambda: self.status_label.clear())
            return

        self.status_label.setText("Adding item...")

        self.add_worker = AddItemThread(name, quantity)
        self.add_worker.item_added.connect(self.handle_add_item_response)
        self.add_worker.start()

    def handle_add_item_response(self, success, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())
        if success:
            self.name_input.clear()
            self.quantity_input.clear()
            self.load_inventory()

    def update_item(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()

        if not name or not quantity.isdigit() or int(quantity) <= 0:
            self.status_label.setText("Invalid input. Enter a valid name and quantity.")
            QTimer.singleShot(2000, lambda: self.status_label.clear())
            return

        self.status_label.setText("Updating item...")

        self.update_worker = UpdateItemThread(name, quantity)
        self.update_worker.item_updated.connect(self.handle_update_item_response)
        self.update_worker.start()

    def handle_update_item_response(self, success, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())
        if success:
            self.name_input.clear()
            self.quantity_input.clear()
            self.load_inventory()

    def delete_item(self):
        name = self.name_input.text().strip()

        if not name:
            self.status_label.setText("Item name cannot be empty.")
            QTimer.singleShot(2000, lambda: self.status_label.clear())
            return

        self.status_label.setText("Deleting item...")

        self.delete_worker = DeleteItemThread(name)
        self.delete_worker.item_deleted.connect(self.handle_delete_item_response)
        self.delete_worker.start()

    def handle_delete_item_response(self, success, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.clear())
        if success:
            self.name_input.clear()
            self.load_inventory()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
