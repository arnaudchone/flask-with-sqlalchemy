# wsgi.py
import logging

from flask import Flask, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # Order is important here!
db = SQLAlchemy(app)
ma = Marshmallow(app)


from models import Product
from schemas import products_schema, product_schema

from flask import request

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)


@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    from tasks import very_slow_add
    very_slow_add.delay(1, 2) # This pushes a task to Celery and does not block.

    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@app.route('/products/<int:product_id>')
def get_product(product_id):
    product = db.session.query(Product).get(product_id)
    return product_schema.jsonify(product)


@app.route('/products/<int:product_id>', methods=['DELETE'])
def del_product(product_id):
    # db.session.query(Product).filter(id=product_id).delete()
    product = db.session.query(Product).get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return ('Deleted product', 204)
    else:
        return ('Product not found', 404)

@app.route('/products', methods=['POST'])
def create_product():
    body = request.get_json()
    # new_product = product_schema.load(body)
    product = Product(name = body['name'], description = body.get('description', ''))
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@app.route('/products', methods=['PATCH'])
def patch_product():
    body = request.get_json()
    product = db.session.query(Product).get(body['id'])
    product.name = body['name']
    product.description = body['description']
    db.session.add(product)
    db.session.commit()
    return ('', 204)
