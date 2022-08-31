import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api


app = Flask(__name__)

# Gets absolute file path
basedir = os.path.abspath(os.path.dirname(__file__))

# Tells application where database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tell application what data to migrate to db
db.create_all()
Migrate(app, db)
api = Api(app)

class Product(db.Model):

    __tablename__ = 'gpus'
    id = db.Column(db.Integer, nullable=True, primary_key=True)
    title = db.Column(db.String)
    soldprice = db.Column(db.Float)
    solddate = db.Column(db.DateTime)
    bids = db.Column(db.String)
    link = db.Column(db.String)

    def __init__(self, id, title, soldprice, solddate, bids, link):
        self.id = id
        self.title = title
        self.soldprice = soldprice
        self.solddate = solddate
        self.bids = bids
        self.link = link

    def json(self):
        return {'id': self.id, 'title': self.title, 'soldprice': self.soldprice, 'solddate': str(self.solddate),
                'bids': self.bids, 'link': self.link}

class ProductApiGet(Resource):

    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            return product.json()
        else:
            return {'id': 'not found'}, 404


api.add_resource(ProductApiGet, '/product/get/<int:id>')

if __name__ == '__main__':
    app.run()
