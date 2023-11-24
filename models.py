from datetime import datetime
from config import db, ma 

class Warehouse(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'warehouse'
    warehouse_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(50))
    food_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WarehouseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Warehouse
        sqla_session = db.session