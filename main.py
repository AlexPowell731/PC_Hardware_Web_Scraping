import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api


# app = Flask(__name__)
#
# # Gets absolute file path
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# # Tells application where database is located
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
# # Tell application what data to migrate to db
# db.create_all()
# Migrate(app, db)
# api = Api(app)


class NewProduct:

    # id = db.Column(db.Integer, nullable=True, primary_key=True)
    # title = db.Column(db.String)
    # price = db.Column(db.Float)
    # link = db.Column(db.String)
    # date = db.Column(db.Date)

    def __init__(self, title, price, link, date):
        self.title = title
        self.price = price
        self.link = link
        self.date = date

    def json(self):
        return {'title': self.title, 'price': self.price, 'link': self.link, 'date': self.date}


class EbayProduct:

    # # DON'T FORGET TO DO DB MIGRATIONS AFTER MAKING CHANGES #
    # id = db.Column(db.Integer, nullable=True, primary_key=True)
    # title = db.Column(db.String)
    # condition = db.Column(db.String)
    # soldprice = db.Column(db.Float)
    # solddate = db.Column(db.DateTime)
    # bids = db.Column(db.String)
    # link = db.Column(db.String)

    def __init__(self, title, condition, soldprice, solddate, bids, link):
        self.title = title
        self.condition = condition
        self.soldprice = soldprice
        self.solddate = solddate
        self.bids = bids
        self.link = link

    def json(self):
        return {'title': self.title, 'condition': self.condition, 'soldprice': self.soldprice,
                'solddate': str(self.solddate), 'bids': self.bids, 'link': self.link}


