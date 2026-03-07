import stripe
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, CartItem, Order, OrderItem, Category, WishlistItem
from dotenv import load_dotenv

# Force load .env from the same folder as app.py
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- USER LOADER ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
        return {"cart_count": int(count)}
    return {"cart_count": 0}


@app.context_processor
def inject_categories():
    categories = Category.query.order_by(Category.name).all()
    return {"categories": categories}


def _product_query(search=None, category_slug=None, sort="default"):
    q = Product.query
    if search:
        term = f"%{search}%"
        q = q.filter(db.or_(Product.name.ilike(term), Product.description.ilike(term)))
    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            q = q.filter(Product.category_id == cat.id)
    if sort == "price_low":
        q = q.order_by(Product.price.asc())
    elif sort == "price_high":
        q = q.order_by(Product.price.desc())
    elif sort == "rating":
        q = q.order_by(Product.rating.desc())
    elif sort == "name":
        q = q.order_by(Product.name.asc())
    return q


# ---------------- HOME ----------------
@app.route("/")
def home():
    search = request.args.get("q", "").strip()
    category_slug = request.args.get("category")
    sort = request.args.get("sort", "default")
    products = _product_query(search=search or None, category_slug=category_slug, sort=sort).all()
    cat = Category.query.filter_by(slug=category_slug).first() if category_slug else None
    return render_template("index.html", products=products, search=search, current_category=category_slug, current_category_name=cat.name if cat else None, sort=sort)


# ---------------- SEARCH ----------------
@app.route("/search")
def search():
    return redirect(url_for("home", q=request.args.get("q", "")))


# ---------------- PRODUCT DETAIL ----------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter(
        Product.id != product.id,
        db.or_(Product.category_id == product.category_id, Product.category_id.is_(None))
    ).limit(4).all()
    if len(related) < 4:
        related = list(related) + list(Product.query.filter(Product.id != product.id).limit(4 - len(related)).all())
    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first() is not None
    return render_template("product_detail.html", product=product, related=related[:4], in_wishlist=in_wishlist)


# ---------------- WISHLIST ----------------
@app.route("/wishlist")
@login_required
def wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template("wishlist.html", items=items)


@app.route("/add-to-wishlist/<int:product_id>", methods=["POST"])
@login_required
def add_to_wishlist(product_id):
    Product.query.get_or_404(product_id)
    if not WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        db.session.add(WishlistItem(user_id=current_user.id, product_id=product_id))
        db.session.commit()
        flash("Added to wishlist.", "success")
    next_url = request.form.get("next") or request.referrer or url_for("home")
    return redirect(next_url)


@app.route("/remove-from-wishlist/<int:product_id>", methods=["POST"])
@login_required
def remove_from_wishlist(product_id):
    WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).delete()
    db.session.commit()
    flash("Removed from wishlist.", "success")
    next_url = request.form.get("next") or request.referrer or url_for("home")
    return redirect(next_url)


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return render_template("register.html")

        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# ---------------- ADD PRODUCTS (RUN ONCE) ----------------
@app.route("/add-products")
def add_products():
    if Product.query.first():
        return redirect(url_for("home"))

    categories = [
        Category(name="Electronics", slug="electronics"),
        Category(name="Clothing", slug="clothing"),
        Category(name="Accessories", slug="accessories"),
        Category(name="Home", slug="home"),
        Category(name="Books", slug="books"),
        Category(name="Sports", slug="sports"),
    ]
    db.session.add_all(categories)
    db.session.flush()

    products = [
        # Electronics
        Product(name="Wireless Earbuds Pro", price=8900, description="Active noise cancellation, 24hr battery. Crystal-clear sound.", image_url="https://images.unsplash.com/photo-1598331668826-20cecc596b86?w=400", category_id=1, rating=4.7, review_count=2847),
        Product(name="Smart Watch Series 5", price=24900, description="Health tracking, GPS, water-resistant. 5-day battery life.", image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", category_id=1, rating=4.6, review_count=1203),
        Product(name="Laptop Stand Aluminum", price=4500, description="Ergonomic design, adjustable height. Fits all laptops up to 17\".", image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400", category_id=1, rating=4.5, review_count=892),
        Product(name="Portable Bluetooth Speaker", price=6900, description="360° sound, 20hr battery. IPX7 waterproof.", image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", category_id=1, rating=4.4, review_count=1567),
        Product(name="Mechanical Keyboard", price=12000, description="Cherry MX switches, RGB backlight. Premium build.", image_url="https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400", category_id=1, rating=4.8, review_count=2103),
        Product(name="USB-C Hub 7-in-1", price=3500, description="HDMI, USB 3.0, SD card reader. Compact design.", image_url="https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?w=400", category_id=1, rating=4.3, review_count=445),
        # Clothing
        Product(name="Classic Cotton T-Shirt", price=1500, description="Premium 100% organic cotton, breathable and soft.", image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", category_id=2, rating=4.6, review_count=3421),
        Product(name="Slim Fit Chinos", price=4500, description="Stretch fabric, modern fit. Available in 8 colors.", image_url="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400", category_id=2, rating=4.5, review_count=876),
        Product(name="Merino Wool Sweater", price=8900, description="Soft, temperature-regulating. Perfect for layering.", image_url="https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400", category_id=2, rating=4.7, review_count=534),
        Product(name="Lightweight Jacket", price=12000, description="Water-resistant, packable. Ideal for travel.", image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400", category_id=2, rating=4.4, review_count=1203),
        Product(name="Performance Leggings", price=3800, description="Four-way stretch, moisture-wicking. High-rise fit.", image_url="https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400", category_id=2, rating=4.6, review_count=2890),
        # Accessories
        Product(name="Leather Backpack", price=5500, description="Handcrafted genuine leather. Laptop sleeve included.", image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", category_id=3, rating=4.7, review_count=1567),
        Product(name="Aviator Sunglasses", price=3200, description="UV400 protection, polarized. Classic style.", image_url="https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400", category_id=3, rating=4.5, review_count=892),
        Product(name="Minimalist Watch", price=2500, description="Sleek stainless steel. Water-resistant.", image_url="https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400", category_id=3, rating=4.6, review_count=2103),
        Product(name="Leather Belt", price=2800, description="Full-grain leather, brass buckle. Timeless design.", image_url="https://images.unsplash.com/photo-1624222247344-550fb60583f2?w=400", category_id=3, rating=4.4, review_count=445),
        Product(name="Canvas Crossbody Bag", price=4200, description="Compact, durable. Multiple pockets.", image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400", category_id=3, rating=4.5, review_count=678),
        # Home
        Product(name="Ceramic Coffee Set", price=5500, description="Handcrafted ceramic. 4 cups, 1 carafe.", image_url="https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400", category_id=4, rating=4.7, review_count=534),
        Product(name="Desk Lamp LED", price=4500, description="Adjustable brightness, USB charging port.", image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400", category_id=4, rating=4.5, review_count=1203),
        Product(name="Throw Blanket", price=3800, description="Soft fleece, machine washable. 50x60 inches.", image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400", category_id=4, rating=4.6, review_count=876),
        Product(name="Candle Set 3-Pack", price=2400, description="Soy wax, long-lasting. Lavender, cedar, vanilla.", image_url="https://images.unsplash.com/photo-1602874801006-4e411e29a924?w=400", category_id=4, rating=4.4, review_count=2103),
        # Books
        Product(name="Productivity Guide", price=1899, description="Best-selling guide to getting more done. 320 pages.", image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400", category_id=5, rating=4.8, review_count=3421),
        Product(name="Design Principles", price=2499, description="Essential design theory for creators. Hardcover.", image_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", category_id=5, rating=4.6, review_count=892),
        Product(name="Cooking Essentials", price=2200, description="100 recipes for everyday meals. Full-color photos.", image_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400", category_id=5, rating=4.5, review_count=1567),
        # Sports
        Product(name="Running Shoes", price=4000, description="Lightweight performance runners. Cushioned sole.", image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", category_id=6, rating=4.7, review_count=2890),
        Product(name="Yoga Mat 6mm", price=3200, description="Non-slip, eco-friendly. Includes carry strap.", image_url="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400", category_id=6, rating=4.6, review_count=1203),
        Product(name="Resistance Bands Set", price=2500, description="5 levels of resistance. For home workouts.", image_url="https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400", category_id=6, rating=4.5, review_count=678),
    ]
    db.session.add_all(products)
    db.session.commit()

    return redirect(url_for("home"))


# ---------------- ADD TO CART ----------------
@app.route("/add-to-cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    next_url = request.args.get("next", url_for("cart"))
    return redirect(next_url)


# ---------------- REMOVE FROM CART ----------------
@app.route("/remove-from-cart/<int:cart_item_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for("cart"))


# ---------------- UPDATE CART QUANTITY ----------------
@app.route("/update-cart/<int:cart_item_id>", methods=["POST"])
@login_required
def update_cart_quantity(cart_item_id):
    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first_or_404()
    qty = request.form.get("quantity", type=int, default=1)
    if qty < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = qty
    db.session.commit()
    return redirect(url_for("cart"))


# ---------------- CART PAGE ----------------
@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).order_by(CartItem.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/create-checkout-session")
@login_required
def create_checkout_session():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for("cart"))

    line_items = []
    for item in cart_items:
        product = item.product
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": product.price,
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for("success", _external=True),
        cancel_url=url_for("cancel", _external=True),
    )

    return redirect(session.url)

@app.route("/success")
@login_required
def success():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return redirect(url_for("orders"))
    total = sum(item.product.price * item.quantity for item in cart_items)

    new_order = Order(user_id=current_user.id, total_amount=total)
    db.session.add(new_order)
    db.session.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price,
        )
        db.session.add(order_item)

    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return render_template("success.html", order=new_order)


@app.route("/cancel")
@login_required
def cancel():
    return render_template("cancel.html")


# ---------------- ORDERS ----------------
@app.route("/orders")
@login_required
def orders():
    orders_list = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template("orders.html", orders=orders_list)
# ---------------- MIGRATIONS ----------------
def run_migrations():
    """Add new columns/tables (e.g. after schema changes)."""
    with app.app_context():
        db.create_all()
        migrations = [
            "ALTER TABLE product ADD COLUMN image_url VARCHAR(500)",
            "ALTER TABLE product ADD COLUMN category_id INTEGER",
            "ALTER TABLE product ADD COLUMN rating FLOAT DEFAULT 0",
            "ALTER TABLE product ADD COLUMN review_count INTEGER DEFAULT 0",
        ]
        for sql in migrations:
            try:
                db.session.execute(db.text(sql))
                db.session.commit()
            except Exception:
                db.session.rollback()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    run_migrations()

    app.run(debug=True)
    

