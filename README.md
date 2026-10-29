# CaféConnect — Multi-vendor Café Marketplace

A responsive Django web application for a BCA semester project. Café owners can create a shop profile, publish products and offers, and manage incoming orders. Customers can register, explore cafés, add products to a cart, place an order, and review a café after ordering.

## Technology
- Python 3.10+
- Django 5.2
- SQLite (database file is created automatically)
- HTML, CSS, Bootstrap 5, JavaScript
- Pillow for image uploads

## Run on Ubuntu/Linux
```bash
cd caféhub
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
cd caféhub
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
You can seed a sample café and products with `python manage.py seed_demo`. Demo accounts are `demo_cafe_reserve` / `CafeDemo123!` and `demo_customer` / `CustomerDemo123!`; these are for local demonstration only.

1. Register a new account and select **Café owner**. Edit the default shop profile, add a few products, and publish an offer.
2. Log out, register a separate **Customer** account, browse cafés, add a product to the cart, and place an order.
3. Log back in as the café owner, open Orders, and change the order status.
4. Log back in as the customer and submit a review for the café.
5. Create a superuser and visit `/admin/` to demonstrate platform administration.

## Current MVP scope
- Separate customer and café-owner experiences
- Shop profile and product CRUD
- Active/inactive offers
- Session-based cart and checkout
- Orders and status updates
- Customer reviews after ordering
- Responsive Bootstrap layout

## Important notes before any public deployment
This starter is configured for local development (`DEBUG=True`, development `SECRET_KEY`, SQLite). Before publishing publicly, set `DEBUG=False`, use a private environment variable for `SECRET_KEY`, configure `ALLOWED_HOSTS`, run `python manage.py collectstatic`, and use HTTPS and production hosting. Do not use the development server as a production server. The demo checkout does not collect online payments. A single order currently contains products from one café only.



## Bundled café and menu photos (important)

This ZIP includes local JPEG photos for all four demo café covers and the demo drink/food catalogue in both `media/` and `static/images/`. The demo templates use the bundled static copies for seeded showcase items, so these images do not depend on a Cloudinary upload and are included in `collectstatic` for Render. Uploaded photos for newly created products continue to use the configured media storage.

After extracting the ZIP, from the `BakeryHub` folder run the following commands to rebuild the sample café data and attach the bundled image filenames to the sample products. **This resets demo shop/product/order/review/marketing records**; back up your database first if you need to preserve them.

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`. If old bakery entries are still visible, the demo seed command has not been run against the database currently being used.

## Deploy on Render

1. Create a Render PostgreSQL database and wait until its status is Available.
2. Create a Render **Web Service** connected to this repository and branch `main`.
3. Set **Root Directory** to `.` if the repository root contains `manage.py`; if `manage.py` is inside `caféhub/`, set Root Directory to `caféhub`.
4. Build command: `bash build.sh`
5. Start command: `python manage.py migrate --noinput && gunicorn config.wsgi:application`
6. Add these environment variables to the Web Service:
   - `SECRET_KEY`: generate a new random secret in Render; do not reuse a key committed to GitHub.
   - `DEBUG`: `False`
   - `DATABASE_URL`: paste the database's **Internal Database URL**. Keep the database and Web Service in the same Render region.
7. Deploy. After it starts, create an admin user using Render Shell: `python manage.py createsuperuser`.

The local SQLite database is intentionally not included in the deployment source archive. Existing local data does not automatically transfer to PostgreSQL. Uploaded media stored on the service filesystem is not durable across redeploys; use persistent/object storage if you need production uploads to persist.


## Production image uploads on Render

Render service filesystems are ephemeral unless a persistent disk is configured. This project supports Cloudinary for durable uploaded product images and café logos.

1. Create a Cloudinary account and copy its `CLOUDINARY_URL` from the dashboard.
2. In Render, open the BakeryHub Web Service → Environment → Add Environment Variable.
3. Add `CLOUDINARY_URL` as the key and paste the private Cloudinary URL as the value. Do not commit it to GitHub.
4. Redeploy the service. The app automatically switches uploaded media to Cloudinary when this variable exists.
5. Re-upload existing product images and café logos from the café dashboard; images previously saved on the Render filesystem are not automatically copied to Cloudinary.

The navbar displays a cart item count. Review forms allow a signed-in user to create or update one café review, and anonymous visitors are prompted to log in first.


## CaféConnect upgrade (incremental)

This package upgrades the existing BakeryHub codebase under the CaféConnect café-marketing concept while retaining the current marketplace models and workflows. It adds owner-scoped campaign management, a marketing analytics overview, coupon and marketing-event database models, Django admin registration, and migration `0002_marketing_tools.py`.

### Apply the upgrade locally

1. Activate your existing virtual environment and install requirements: `python -m pip install -r requirements.txt`.
2. Configure `.env` / environment variables as described above. Never commit real secrets.
3. Run `python manage.py check`.
4. Run `python manage.py migrate`.
5. Run `python manage.py runserver` and sign in with a café-owner account.
6. Open `/marketing/campaigns/` and `/marketing/analytics/`.

### Scope and honest implementation notes

The current cart, orders, products, shops, reviews, offers, login and owner dashboard remain the base application. Campaign creation and owner-scoped analytics pages are included. Coupon records are modelled and available in Django admin, but coupon redemption is not yet connected to checkout. Marketing event models are present; automatic event collection must be connected to relevant page/click actions before analytics can show real activity. This is an incremental upgrade, not a claim that every item in the CaféConnect master specification is already implemented. QR generation, newsletter delivery, automated AI integration and additional customer/owner workflows remain subsequent implementation tasks.

### Cloudinary security

Configure a valid `CLOUDINARY_URL` as a server-side environment variable in Render. Do not put credentials in templates or commit them. Rotate any Cloudinary API secret previously shared in chat. Existing image files stored on the Render local filesystem are not automatically uploaded to Cloudinary; verify and migrate image assets separately.


## CaféConnect café showcase data

To populate the showcase with five demo cafés and 50 sample menu items (espresso, cappuccino, lattes, frappés, bubble tea, fruit tea, cold brew, sandwiches and desserts), run:

```powershell
python manage.py migrate
python manage.py seed_demo
```

Demo café-owner accounts use usernames `demo_cafe_reserve`, `demo_roastroom`, `demo_bubblebay`, `demo_mocha`, and `demo_cafecorner`; the demonstration password is `CafeDemo123!`. Customer demo account: `demo_customer` / `CustomerDemo123!`. These accounts and passwords are for local demonstration only; change or remove them before deploying publicly. The showcase menu entries are sample content, not an official Starbucks menu or affiliation.


**Demo data warning:** `python manage.py seed_demo` resets shop-related demo data, including existing shops, products, offers, orders, reviews and marketing records. Back up `db.sqlite3` first. The example menu is inspired by common coffeehouse offerings and is not an official Starbucks menu or affiliation.

## Café photography upgrade

The demo seed command assigns bundled local café and menu images to showcase records. Run `python manage.py seed_demo` to reset the demo storefronts and populate four café showcases with coffeehouse-style menus and local image assets. This command deletes existing shop/product/order/review demo data; back up your database first. The sample menus are independently written and are not an official Starbucks menu or affiliation.

## Render recovery: automatically restore the four café showcases

This deployment version fixes the two causes of an empty live catalogue:

1. The Render start command applies Django migrations before starting Gunicorn, avoiding errors such as `no such table: marketplace_shop`.
2. `ensure_demo_data` safely adds or refreshes the four showcase cafés and their 48 menu items. It uses `update_or_create` and does **not** delete orders, customers, reviews, existing shops, or unrelated products. The old `seed_demo` command is now a safe alias.
3. Café and menu showcase photos are bundled in `static/images/` and resolved through Django's static-file storage. The demo photos do not rely on Render's temporary `/media/` filesystem or on Cloudinary.

### Required Render settings

In **Render → your Web Service → Settings**:

- **Build Command:** `bash build.sh`
- **Start Command:** `python manage.py migrate --noinput && python manage.py ensure_demo_data && gunicorn config.wsgi:application`

In **Environment**, keep the `DATABASE_URL` that belongs to the existing Render PostgreSQL database. Do not replace it with a new database; the recovery command is non-destructive. Set `DEBUG=False` and a strong `SECRET_KEY` if they are not already present.

Cloudinary is not required for the bundled café/product showcase photos. For persistent images uploaded by café owners, set the environment variable named `CLOUDINARY_URL` to a valid Cloudinary URL that starts with `cloudinary://`. The value must not include the literal text `CLOUDINARY_URL=`. If a secret previously appeared in a chat or screenshot, rotate it in Cloudinary before updating Render.

After saving settings, manually trigger **Manual Deploy → Deploy latest commit**. In the deploy logs, look for the `CaféConnect showcase ready: 4 cafés, 48 menu items` message. Visiting the live homepage and `/shops/` should then display the cafés and bundled photos.
