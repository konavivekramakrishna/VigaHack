from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableView, QDialog, QDialogButtonBox, QLabel, QLineEdit, QSizePolicy, QProgressBar, QHBoxLayout
from PySide6.QtCore import Qt, QThread, Signal, QAbstractTableModel, QTimer
from PySide6.QtGui import QFont
import requests
import sys

API_BASE_URL = "http://127.0.0.1:5000"

class InventoryModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 2  # Name and Quantity

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._data[index.row()]["name"]
            elif index.column() == 1:
                return str(self._data[index.row()]["quantity"])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return "Name" if section == 0 else "Quantity"
        return None

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

class FetchInventoryThread(QThread):
    data_fetched = Signal(list)

    def run(self):
        try:
            response = requests.get(f"{API_BASE_URL}/get-items")
            data = response.json()
            if data["message"] == "Items retrieved successfully":
                self.data_fetched.emit(data["data"])
            else:
                self.data_fetched.emit([])
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.data_fetched.emit([])

class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 1000, 800)  # Increase window size

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Table Setup
        self.table = QTableView()
        self.table.setFont(QFont("Arial", 12))
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.table)

        # Stretch Factor (to make table more expansive)
        self.layout.setStretch(0, 2)  # Stretch the table more

        # Progress Bar (for showing loading state)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # Status Label
        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Button Setup
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px;")
        self.refresh_button.clicked.connect(self.load_inventory)
        self.layout.addWidget(self.refresh_button)

        # Add Item Button
        self.add_button = QPushButton("Add Item")
        self.add_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px; padding: 10px;")
        self.add_button.clicked.connect(self.open_add_item_dialog)
        self.layout.addWidget(self.add_button)

        # Load Inventory
        self.load_inventory()

    def load_inventory(self):
        self.progress_bar.setVisible(True)  # Show progress bar
        self.status_label.setText("")
        self.thread = FetchInventoryThread()
        self.thread.data_fetched.connect(self.populate_table)
        self.thread.start()

    def populate_table(self, items):
        # Hide progress bar after data is fetched
        self.progress_bar.setVisible(False)

        # Handle Empty Data
        if not items:
            self.show_no_data_dialog()
            self.table.setRowCount(0)
            return

        model = InventoryModel(items)
        self.table.setModel(model)

    def show_no_data_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("No Data")
        dialog.setGeometry(100, 100, 300, 100)
        
        layout = QVBoxLayout()
        label = QLabel("No items found in the inventory.")
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.rejected.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def open_add_item_dialog(self):
        # Inline Modal Layout for Add Item with improved design
        self.modal_layout = QVBoxLayout()
        self.modal_overlay = QWidget(self)
        self.modal_overlay.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px; border: 1px solid #ddd;")
        self.modal_overlay.setGeometry(150, 150, 700, 350)  # Increase modal size
        self.modal_overlay.setVisible(True)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter Item Name")
        name_input.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 5px;")

        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter Quantity")
        quantity_input.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 5px;")

        self.modal_layout.addWidget(QLabel("Item Name:"))
        self.modal_layout.addWidget(name_input)
        self.modal_layout.addWidget(QLabel("Quantity:"))
        self.modal_layout.addWidget(quantity_input)

        add_button = QPushButton("Add")
        add_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px;")
        add_button.clicked.connect(lambda: self.add_item(name_input.text(), quantity_input.text(), name_input, quantity_input))
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 10px;")
        cancel_button.clicked.connect(lambda: self.close_modal(self.modal_overlay))

        self.modal_layout.addWidget(add_button)
        self.modal_layout.addWidget(cancel_button)

        self.modal_overlay.setLayout(self.modal_layout)

    def close_modal(self, modal):
        modal.setVisible(False)

    def add_item(self, name, quantity, name_input, quantity_input):
        if not name or not quantity.isdigit():
            self.status_label.setText("Error: Invalid input.")
            QTimer.singleShot(2000, lambda: self.status_label.clear())  # Clear after 2 seconds
            return
        
        # Close modal immediately after clicking add
        self.close_modal(self.modal_overlay)

        # Show loading status
        self.status_label.setText("Loading...")

        try:
            response = requests.post(f"{API_BASE_URL}/add-item", json={"name": name, "quantity": int(quantity)})
            if response.status_code == 200:
                # On success, reload inventory
                self.status_label.setText("Item added successfully.")
                QTimer.singleShot(2000, lambda: self.status_label.clear())  # Clear after 2 seconds
                self.load_inventory()  # Reload after adding item
            else:
                self.status_label.setText(f"Error: {response.json().get('error')}")
                QTimer.singleShot(2000, lambda: self.status_label.clear())  # Clear after 2 seconds
        except Exception as e:
            print(f"Error adding item: {e}")
            self.status_label.setText("Error adding item.")
            QTimer.singleShot(2000, lambda: self.status_label.clear())  # Clear after 2 seconds

        name_input.clear()
        quantity_input.clear()

    def closeEvent(self, event):
        self.thread.quit()  # Ensure the thread is properly stopped before closing
        self.thread.wait()  # Wait for the thread to fully finish
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
