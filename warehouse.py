from flask import make_response, abort
from config import db
from models import Warehouse, WarehouseSchema



def read_all():
    warehouse = Warehouse.query.order_by(Warehouse.warehouse_id).all()
    
    warehouse_schema = WarehouseSchema(many=True)
    data = warehouse_schema.dump(warehouse)
    return data


def read_one(warehouse_id):
    warehouse = Warehouse.query.filter(Warehouse.warehouse_id == warehouse_id).one_or_none()

    if warehouse is not None:
        warehouse_schema = WarehouseSchema()
        data = warehouse_schema.dump(warehouse)
        return data

    else:
        abort(
            404, "item not found for Id: {warehouse_id}".format(warehouse_id=warehouse_id)
        )


def create(warehouse):
    food_name = warehouse.get("food_name")
    food_type = warehouse.get("food_type")
    existing_warehouse = (
        Warehouse.query.filter(Warehouse.food_name == food_name)
        .filter(Warehouse.food_type == food_type)
        .one_or_none()
    )

    if existing_warehouse is None:
        schema = WarehouseSchema()
        new_warehouse = Warehouse(food_name=food_name, food_type=food_type)
        db.session.add(new_warehouse)
        db.session.commit()
        data = schema.dump(new_warehouse)
        return data, 201
    else:
        abort(
            409,
            "Warehouse {food_name} {food_type} exists already".format(
                food_name=food_name, food_type=food_type
            ),
        )

def update(warehouse_id, warehouse):
    update_warehouse = Warehouse.query.filter(
        Warehouse.warehouse_id == warehouse_id
    ).one_or_none()

    food_name = warehouse.get("food_name")
    food_type = warehouse.get("food_type")

    existing_warehouse = (
        Warehouse.query.filter(Warehouse.food_name == food_name)
        .filter(Warehouse.food_type == food_type)
        .one_or_none()
    )


    if update_warehouse is None:
        abort(
            404,
            "Wish not found for Id: {warehouse_id}".format(warehouse_id=warehouse_id),
        )
    elif (
        existing_warehouse is not None and existing_warehouse.warehouse_id != warehouse_id
    ):
        abort(
            409,
            "Item {food_name} {food_type} exists already".format(
                food_name=food_name, food_type=food_type
            ),
        )
    else:
        schema = WarehouseSchema()
        updt_wish = Warehouse(food_name=food_name, food_type=food_type, warehouse_id=warehouse_id)
        db.session.merge(updt_wish)
        db.session.commit()
        data = schema.dump(update_warehouse)
        return data, 200


def delete(warehouse_id):


    warehouse = Warehouse.query.filter(Warehouse.warehouse_id == warehouse_id).one_or_none()

    if warehouse is not None:
        db.session.delete(warehouse)
        db.session.commit()
        return make_response(
            "Item {warehouse_id} deleted".format(warehouse_id=warehouse_id), 200
        )
    else:
        abort(
            404,
            "Item not found for Id: {warehouse_id}".format(warehouse_id=warehouse_id),
        )