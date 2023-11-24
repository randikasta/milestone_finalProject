import os
from config import db
from models import Warehouse
from app import connex_app

WAREHOUSE = [
    {'food_name': 'Qitela', 'food_type' : 'Snack' },
    {'food_name': 'Lays', 'food_type' : 'Snack' },
    {'food_name': 'LeMinerale', 'food_type' : 'Drinks' },
    {'food_name': 'Sprite', 'food_type' : 'Soft Drinks' }
]

if os.path.exists('warehouse.db'):
    os.remove('warehouse.db')

with connex_app.app.app_context():
    db.create_all()

    for warehouse in WAREHOUSE:
        p = Warehouse(food_name=warehouse['food_name'], food_type=warehouse['food_type'])
        db.session.add(p)

    db.session.commit()