from database import db

class Inventory(db.Model):
    """
    Represents the inventory table in the database.
    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Unique name of the inventory item.
        quantity (int): Quantity of the item, default is 0.
    """
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)