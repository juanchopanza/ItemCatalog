'''Define up Item Catalog ORM'''
from . import db

#  Representation of a table of a relational DB as a python object.
#  We will extend this because we think OOP is awesome.
Base = db.Model

class User(Base):

    __tablename__ = 'user'
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    id = db.Column(db.Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.id
        }

class Category(Base):

    __tablename__ = 'category'
    name = db.Column(db.String(128), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id
        }
