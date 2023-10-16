from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Use your database URI
db = SQLAlchemy(app)

################################################### LOAD PAGES ###################################################################
@app.route('/')

def returnHTML():
    return render_template('reg_log.html')      # o flask para detetar as paginas html precisa de ser corrido da root do projeto
                                                # (fora de qqr pasta) e os html têm que estar numa pasta chamada 'templates'

###################################################### SQL #######################################################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('normal', 'admin'), nullable=False)
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(5, 2))
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    photo = db.Column(db.String(255))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    order_status = db.Column(db.Enum('pending', 'processing', 'shipped', 'delivered'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    order = db.relationship('Order', foreign_keys=[order_id])
    product = db.relationship('Product', foreign_keys=[product_id])

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.Enum('pending', 'paid', 'late'), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    order = db.relationship('Order', foreign_keys=[order_id])

class ProductComment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    user = db.relationship('User', foreign_keys=[user_id])
    product = db.relationship('Product', foreign_keys=[product_id])

class ProductReview(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    user = db.relationship('User', foreign_keys=[user_id])
    product = db.relationship('Product', foreign_keys=[product_id])

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    product = db.relationship('Product', foreign_keys=[product_id])

db.create_all()
app.run()