from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# ---------------- USER ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    orders = db.relationship("Order", backref="user", lazy=True)
    wishlist_items = db.relationship("WishlistItem", backref="user", lazy=True)


# ---------------- CATEGORY ----------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    products = db.relationship("Product", backref="category", lazy=True)


# ---------------- PRODUCT ----------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Integer)  # stored in cents
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    rating = db.Column(db.Float, default=0)  # 0-5 stars
    review_count = db.Column(db.Integer, default=0)


# ---------------- CART ITEM ----------------
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product", backref="cart_items", lazy=True)


# ---------------- WISHLIST ITEM ----------------
class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    product = db.relationship("Product", backref="wishlist_items", lazy=True)


# ---------------- ORDER ----------------
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_amount = db.Column(db.Integer)

    order_items = db.relationship("OrderItem", backref="order", lazy=True)


# ---------------- ORDER ITEM ----------------
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)  # price at time of purchase

    product = db.relationship("Product", backref="order_items", lazy=True)
