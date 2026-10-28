# BakeryHub — Multi-vendor Bakery Marketplace

A responsive Django web application for a BCA semester project. Bakery owners can create a shop profile, publish products and offers, and manage incoming orders. Customers can register, explore bakeries, add products to a cart, place an order, and review a bakery after ordering.

## Technology
- Python 3.10+
- Django 5.2
- SQLite (database file is created automatically)
- HTML, CSS, Bootstrap 5, JavaScript
- Pillow for image uploads

## Run on Ubuntu/Linux
```bash
cd bakeryhub
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations marketplace
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Admin: http://127.0.0.1:8000/admin/ .

## Run on Windows PowerShell
```powershell
cd bakeryhub
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations marketplace
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```
If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.

## Demo flow
You can seed a sample bakery and products with `python manage.py seed_demo`. Demo accounts are `demo_baker` / `BakeryDemo123!` and `demo_customer` / `CustomerDemo123!`; these are for local demonstration only.

1. Register a new account and select **Bakery owner**. Edit the default shop profile, add a few products, and publish an offer.
2. Log out, register a separate **Customer** account, browse bakeries, add a product to the cart, and place an order.
3. Log back in as the bakery owner, open Orders, and change the order status.
4. Log back in as the customer and submit a review for the bakery.
5. Create a superuser and visit `/admin/` to demonstrate platform administration.

## Current MVP scope
- Separate customer and bakery-owner experiences
- Shop profile and product CRUD
- Active/inactive offers
- Session-based cart and checkout
- Orders and status updates
- Customer reviews after ordering
- Responsive Bootstrap layout

## Important notes before any public deployment
This starter is configured for local development (`DEBUG=True`, development `SECRET_KEY`, SQLite). Before publishing publicly, set `DEBUG=False`, use a private environment variable for `SECRET_KEY`, configure `ALLOWED_HOSTS`, run `python manage.py collectstatic`, and use HTTPS and production hosting. Do not use the development server as a production server. The demo checkout does not collect online payments. A single order currently contains products from one bakery only.


## Deploy on Render

1. Create a Render PostgreSQL database and wait until its status is Available.
2. Create a Render **Web Service** connected to this repository and branch `main`.
3. Set **Root Directory** to `.` if the repository root contains `manage.py`; if `manage.py` is inside `bakeryhub/`, set Root Directory to `bakeryhub`.
4. Build command: `bash build.sh`
5. Start command: `python manage.py migrate --noinput && gunicorn config.wsgi:application`
6. Add these environment variables to the Web Service:
   - `SECRET_KEY`: generate a new random secret in Render; do not reuse a key committed to GitHub.
   - `DEBUG`: `False`
   - `DATABASE_URL`: paste the database's **Internal Database URL**. Keep the database and Web Service in the same Render region.
7. Deploy. After it starts, create an admin user using Render Shell: `python manage.py createsuperuser`.

The local SQLite database is intentionally not included in the deployment source archive. Existing local data does not automatically transfer to PostgreSQL. Uploaded media stored on the service filesystem is not durable across redeploys; use persistent/object storage if you need production uploads to persist.
