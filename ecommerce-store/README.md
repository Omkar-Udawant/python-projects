# LUXE E‑Commerce Store

Modern, Amazon‑inspired e‑commerce store built with **Flask**, **Stripe Checkout**, and a **dark premium UI**.

This repo is ready to drop into GitHub as a showcase project or starter template.

---

## Features

- **Authentication**
  - Email / password sign up & login (Flask‑Login)
  - Protected routes for cart, orders, checkout, wishlist

- **Product catalog**
  - 20+ seeded products
  - **6 categories** (Electronics, Clothing, Accessories, Home, Books, Sports)
  - Product detail pages with breadcrumbs and “You may also like” section
  - Ratings + review counts displayed on cards and detail pages

- **Shopping cart**
  - Add to cart from listings, product detail, and wishlist
  - Quantity update, remove item, auto‑recalculated totals
  - Cart badge in navbar showing total item count

- **Wishlist**
  - Save products for later
  - Move items from wishlist → cart

- **Orders & payments**
  - Stripe Checkout integration (card payments)
  - Order + order items persisted with totals
  - Order history page per user
  - Success / cancel pages with friendly UI

- **UI / UX**
  - Dark, modern theme with custom CSS
  - Responsive layout (Bootstrap 5)
  - Hero section, category pills, sort dropdown, search bar

---

## Tech Stack

- **Backend**: Flask, Flask‑Login, SQLAlchemy
- **Database**: SQLite
- **Payments**: Stripe Checkout
- **Frontend**: Jinja2 templates, Bootstrap 5, custom CSS

---

## Getting Started

### 1. Create & activate virtualenv (Windows)

```bash
cd ecommerce-store
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Stripe

Create a `.env` file in the project root:

```env
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
```

You can get a test key from your Stripe dashboard.

### 4. Run database migrations & start the server

```bash
python app.py
```

On first run, the app will create `store.db` automatically.

### 5. Seed the catalog

Visit:

- `http://127.0.0.1:5000/add-products`

This will insert a curated catalog of products across all categories.

### 6. Fresh start / reset DB

If you change models or want a clean slate:

1. Stop the Flask server  
2. Delete the SQLite file:

   - `instance/store.db` (or `store.db` in the project root)

3. Run `python app.py` again  
4. Hit `/add-products` to reseed products

---

## Main Routes

- `/` – Home, product listing + search, category filter, sort
- `/product/<id>` – Product detail
- `/wishlist` – Wishlist (auth required)
- `/cart` – Shopping cart (auth required)
- `/orders` – Order history (auth required)
- `/add-products` – Seed demo catalog (dev only)
- `/create-checkout-session` – Stripe Checkout session
- `/success` / `/cancel` – Post‑payment pages

Auth:

- `/register` – Sign up
- `/login` – Login
- `/logout` – Logout

---

## Screenshots (optional for GitHub)

You can add screenshots to a `screenshots/` folder and embed them here, for example:

```md
![Home page]()
![Product detail](![img.png](img.png))
![Cart](![img_2.png](img_2.png))
```

---

## Ideas for Extensions

- Product reviews with user comments
- Admin dashboard for managing products & orders
- Coupons / discount codes
- Pagination and infinite scroll
- Multi‑currency support

Feel free to fork and customize for your own store or portfolio.
