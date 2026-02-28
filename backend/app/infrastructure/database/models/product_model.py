from app.utils.db import db
from sqlalchemy.sql import func

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True)
    image_mime_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "brand": self.brand,
            "quantity": self.quantity,
            "user_id": self.user_id,
            "image_url": f"/v1/products/{self.id}/image" if self.image_data else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
