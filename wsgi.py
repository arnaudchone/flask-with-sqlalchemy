# wsgi.py
import logging

from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)


from models import Product
from schemas import products_schema, product_schema


@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<int:product_id>')
def get_product(product_id):
    product = db.session.query(Product).get(product_id)
    return product_schema.jsonify(product)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def del_product(product_id):
    product = db.session.query(Product).get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return ('Deleted product', 204)
    else:
        return ('Product not found', 404)

@app.route('/products', methods=['POST'])
def create_product():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

