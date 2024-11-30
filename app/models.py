from . import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)  # New field for city
    image = db.Column(db.String(100), nullable=True)
    available_from = db.Column(db.String(50), nullable=False)


def __repr__(self):
        return f'<Property {self.title}>'