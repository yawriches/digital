# Smart Watches - Premium E-Commerce Platform

A full-stack e-commerce website for premium smart watches, built with Flask and a luxury dark-themed frontend.

## Tech Stack

- **Backend:** Python 3.10+, Flask, SQLAlchemy ORM, Flask-Login
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** SQLite
- **Payments:** Paystack (initialize + verify webhook)
- **Auth:** Flask-Login with bcrypt password hashing

## Features

### Customer-Facing
- Homepage with hero section, featured products, testimonials, newsletter
- Shop/catalog with filtering (category, price range) and sorting
- Product detail pages with image gallery, reviews/ratings, related products
- Shopping cart with persistent sessions (guest + authenticated)
- Checkout flow with address form and Paystack payment gateway
- Order confirmation and order history
- User authentication: signup, login, logout with form validation
- Wishlist functionality
- Live search suggestions

### Admin Panel (`/admin`)
- Dashboard with sales analytics, revenue charts, KPIs
- Product management: add, edit, delete, manage stock and images
- Order management: view all orders, update statuses
- Customer management: view users, enable/disable accounts
- Category management

## Quick Start

### 1. Clone and set up environment

```bash
cd smartwatches
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
# Edit .env with your own SECRET_KEY and Paystack keys
```

### 4. Seed the database

```bash
python seed.py
```

### 5. Run the application

```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Default Accounts

| Role     | Email                    | Password    |
|----------|--------------------------|-------------|
| Admin    | admin@smartwatches.com   | admin123    |
| Customer | john@example.com         | password123 |

## Project Structure

```
smartwatches/
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py        # Flask extensions
│   ├── models.py            # SQLAlchemy models
│   ├── blueprints/
│   │   ├── auth/            # Authentication (signup, login, profile)
│   │   ├── main/            # Customer pages (shop, cart, checkout, etc.)
│   │   ├── admin/           # Admin panel (dashboard, products, orders)
│   │   └── payment/         # Paystack integration
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── main/
│   │   └── admin/
│   └── static/
│       ├── css/style.css    # Dark luxury theme
│       ├── js/main.js       # Frontend interactivity
│       └── uploads/         # Product image uploads
├── config.py                # App configuration
├── run.py                   # Entry point
├── seed.py                  # Database seeder
├── requirements.txt
├── .env.example
└── README.md
```

## Paystack Integration

The app supports Paystack for payment processing. If no Paystack keys are configured, the app runs in **demo mode** where payments are automatically marked as successful.

To enable real payments:
1. Create a Paystack account at https://paystack.com
2. Get your test/live API keys
3. Add them to your `.env` file

## Deployment

Ready for deployment on Railway, Render, or any VPS:

- Set environment variables for `SECRET_KEY`, `DATABASE_URL`, `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY`
- For production, use a proper WSGI server like Gunicorn:
  ```bash
  pip install gunicorn
  gunicorn run:app
  ```

## Security Features

- Password hashing with bcrypt
- CSRF protection on all forms
- SQL injection-safe parameterized queries via SQLAlchemy ORM
- Session-based authentication with Flask-Login
- Admin route protection with decorator
- Environment variables for secrets
