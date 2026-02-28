from app.utils.db import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
            "user_id": self.user_id
        }
