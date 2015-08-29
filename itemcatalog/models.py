'''Define up Item Catalog ORM'''
from . import db

#  Representation of a table of a relational DB as a python object.
#  We will extend this because we think OOP is awesome.
Base = db.Model


class Category(Base):

    __tablename__ = 'category'
    name = db.Column(db.String(128), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class CatalogItem(Base):

    __tablename__ = 'catalog_item'
    name = db.Column(db.String(128), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(Category)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
        }
