from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from marketplace.models import Shop, Category, Product, Offer

User = get_user_model()

CAFE_DATA = [
    {
        "username": "demo_cafe_reserve", "email": "reserve@example.test",
        "name": "Café Reserve",
        "description": "A premium coffee bar for espresso classics, signature lattes, cold brew and café sandwiches.",
        "address": "Model Town, Ludhiana", "phone": "9876543210",
        "offer": ("First Sip", "15% off selected coffee drinks (demo promotion).", 15),
        "products": [
            ("Espresso", "Rich espresso with a smooth crema.", "Hot Coffee", "110.00"),
            ("Caffè Americano", "Espresso balanced with hot water.", "Hot Coffee", "140.00"),
            ("Cappuccino", "Espresso, steamed milk and airy foam.", "Hot Coffee", "180.00"),
            ("Caffè Latte", "Espresso with silky steamed milk.", "Hot Coffee", "190.00"),
            ("Flat White", "Espresso with finely textured milk.", "Hot Coffee", "200.00"),
            ("Caramel Macchiato", "Vanilla milk, espresso and caramel drizzle.", "Signature Coffee", "240.00"),
            ("Caffè Mocha", "Espresso, chocolate and steamed milk.", "Signature Coffee", "230.00"),
            ("Vanilla Latte", "Classic latte with vanilla flavour.", "Signature Coffee", "220.00"),
            ("Cold Brew", "Slow-steeped coffee served over ice.", "Cold Coffee", "210.00"),
            ("Iced Americano", "Espresso and chilled water over ice.", "Cold Coffee", "160.00"),
            ("Classic Grilled Cheese Sandwich", "Toasted bread with melted cheese.", "Food", "190.00"),
            ("Spinach & Corn Sandwich", "Grilled sandwich with spinach, corn and cheese.", "Food", "210.00"),
        ],
    },
    {
        "username": "demo_daily_grind", "email": "dailygrind@example.test",
        "name": "Daily Grind Café",
        "description": "Your everyday stop for brewed coffee, refreshing iced drinks, teas and quick savoury bites.",
        "address": "Sarabha Nagar, Ludhiana", "phone": "9876543211",
        "offer": ("Daily Coffee Deal", "10% off selected brewed coffee (demo promotion).", 10),
        "products": [
            ("Pike-Style Brewed Coffee", "Balanced medium-roast brewed coffee; independently named menu item.", "Brewed Coffee", "130.00"),
            ("Caffè Misto", "Fresh brewed coffee topped with steamed milk.", "Brewed Coffee", "160.00"),
            ("Cortado", "Espresso softened with a small amount of warm milk.", "Hot Coffee", "170.00"),
            ("Hazelnut Latte", "Espresso and steamed milk with hazelnut flavour.", "Hot Coffee", "220.00"),
            ("White Chocolate Mocha", "Espresso with white chocolate and steamed milk.", "Signature Coffee", "250.00"),
            ("Iced Latte", "Espresso and milk served chilled.", "Cold Coffee", "200.00"),
            ("Vanilla Sweet Cream Cold Brew", "Cold brew with a lightly sweet cream topping.", "Cold Coffee", "240.00"),
            ("Iced Peach Tea", "Chilled tea with peach flavour.", "Tea & Refreshers", "170.00"),
            ("Matcha Latte", "Green tea matcha blended with milk.", "Tea & Refreshers", "230.00"),
            ("Hot Chocolate", "Creamy chocolate drink topped with foam.", "Tea & Refreshers", "190.00"),
            ("Paneer Tikka Sandwich", "Toasted sandwich with paneer tikka filling.", "Food", "230.00"),
            ("Butter Croissant", "Flaky, buttery croissant.", "Bakery Snacks", "140.00"),
        ],
    },
    {
        "username": "demo_frappe_house", "email": "frappehouse@example.test",
        "name": "Frappé House",
        "description": "Blended coffee, creamy frappés, iced refreshers and sweet café treats.",
        "address": "Feroze Gandhi Market, Ludhiana", "phone": "9876543212",
        "offer": ("Blended Bliss", "12% off selected blended drinks (demo promotion).", 12),
        "products": [
            ("Coffee Frappé", "Ice-blended coffee with a creamy finish.", "Frappés", "250.00"),
            ("Caramel Frappé", "Blended coffee with caramel flavour and drizzle.", "Frappés", "270.00"),
            ("Mocha Frappé", "Coffee blended with chocolate.", "Frappés", "270.00"),
            ("Java Chip Frappé", "Coffee, chocolate chips and ice blended together.", "Frappés", "290.00"),
            ("Vanilla Cream Frappé", "Vanilla-flavoured creamy ice-blended drink.", "Frappés", "250.00"),
            ("Chocolate Cream Frappé", "Chocolate and milk blended with ice.", "Frappés", "270.00"),
            ("Strawberry Cream Frappé", "Strawberry-flavoured creamy blended drink.", "Frappés", "260.00"),
            ("Iced Brown Sugar Latte", "Espresso, milk and brown sugar over ice.", "Cold Coffee", "240.00"),
            ("Iced White Mocha", "Iced espresso and milk with white chocolate.", "Cold Coffee", "250.00"),
            ("Mango Smoothie", "Mango blended into a cool, smooth drink.", "Refreshers", "220.00"),
            ("Chocolate Chip Cookie", "Cookie with chocolate chips.", "Snacks", "100.00"),
            ("Chocolate Brownie", "Rich chocolate brownie square.", "Snacks", "150.00"),
        ],
    },
    {
        "username": "demo_boba_brew", "email": "bobabrew@example.test",
        "name": "Boba & Brew Café",
        "description": "A modern tea and coffee spot for matcha, iced tea, refreshers, bubble tea and light bites.",
        "address": "BRS Nagar, Ludhiana", "phone": "9876543213",
        "offer": ("Tea Time", "10% off selected teas and refreshers (demo promotion).", 10),
        "products": [
            ("Matcha Green Tea Latte", "Smooth matcha with milk, served hot or iced.", "Tea & Matcha", "230.00"),
            ("Chai Tea Latte", "Spiced tea blended with steamed milk.", "Tea & Matcha", "190.00"),
            ("English Breakfast Tea", "Classic black tea served hot.", "Tea & Matcha", "130.00"),
            ("Mint Citrus Tea", "Refreshing tea with mint and citrus notes.", "Tea & Matcha", "160.00"),
            ("Strawberry Acai-Style Refresher", "Fruit-forward iced refresher; independent menu item.", "Refreshers", "220.00"),
            ("Mango Dragonfruit-Style Refresher", "Bright tropical fruit refresher served chilled.", "Refreshers", "230.00"),
            ("Classic Milk Bubble Tea", "Milk tea with chewy tapioca pearls.", "Bubble Tea", "210.00"),
            ("Brown Sugar Bubble Tea", "Milk tea with brown sugar syrup and pearls.", "Bubble Tea", "240.00"),
            ("Mango Bubble Tea", "Mango tea with tapioca pearls.", "Bubble Tea", "220.00"),
            ("Iced Matcha Latte", "Matcha and milk served over ice.", "Tea & Matcha", "240.00"),
            ("Tomato Mozzarella Sandwich", "Toasted sandwich with tomato, cheese and herbs.", "Food", "240.00"),
            ("Potato & Cheese Puff", "Crisp savoury puff with potato and cheese.", "Snacks", "130.00"),
        ],
    },
]

class Command(BaseCommand):
    help = "Safely add/update the four CaféConnect showcase cafés and 48 menu items without deleting existing records."

    def _category(self, name):
        existing = Category.objects.filter(name=name).first()
        if existing:
            return existing
        base_slug = slugify(name) or "menu"
        slug = base_slug
        suffix = 2
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        category, _ = Category.objects.get_or_create(name=name, defaults={"slug": slug})
        return category

    def _owner(self, cafe):
        base = cafe["username"]
        username = base
        suffix = 1
        while True:
            owner = User.objects.filter(username=username).first()
            if owner is None:
                owner = User.objects.create_user(
                    username=username, email=cafe["email"], password=None
                )
                owner.set_unusable_password()
                owner.save(update_fields=["password"])
                return owner
            # Reuse an unused demo owner, or an owner already attached to this café.
            existing_shop = Shop.objects.filter(owner=owner).first()
            if existing_shop is None or existing_shop.name == cafe["name"]:
                if not owner.email:
                    owner.email = cafe["email"]
                    owner.save(update_fields=["email"])
                return owner
            suffix += 1
            username = f"{base}_showcase{suffix}"

    @staticmethod
    def _product_image(name):
        lower = name.lower()
        if "caramel macchiato" in lower:
            return "caramel_macchiato.jpg"
        if any(word in lower for word in ("espresso", "americano", "cortado")):
            return "espresso.jpg"
        if "cappuccino" in lower:
            return "cappuccino.jpg"
        if "boba" in lower or "bubble tea" in lower:
            return "cafe_boba.jpg"
        if "matcha" in lower:
            return "matcha_frappe.jpg"
        if "refresher" in lower or "mango" in lower:
            return "iced_caramel.jpg"
        if "tea" in lower:
            return "cafe_brew.jpg"
        if "cold brew" in lower:
            return "cold_brew.jpg"
        if "iced" in lower or "misto" in lower:
            return "iced_latte.jpg"
        if "frapp" in lower or "blended" in lower or "java chip" in lower:
            return "mocha_frappe.jpg" if "mocha" in lower or "chocolate" in lower else "caramel_frappe.jpg"
        if "croissant" in lower:
            return "croissant.jpg"
        if "sandwich" in lower or "grilled cheese" in lower:
            return "sandwich.jpg"
        if any(word in lower for word in ("brownie", "cookie", "puff")):
            return "mocha_frappe.jpg"
        if "mocha" in lower or "chocolate" in lower:
            return "cafe_mocha.jpg"
        if "boba" in lower:
            return "cafe_boba.jpg"
        if "caramel" in lower:
            return "iced_caramel.jpg"
        if "coffee" in lower:
            return "cafe_brew.jpg"
        return "latte.jpg"

    @transaction.atomic
    def handle(self, *args, **options):
        categories = {}
        for cafe in CAFE_DATA:
            for _, _, category_name, _ in cafe["products"]:
                if category_name not in categories:
                    categories[category_name] = self._category(category_name)

        created_shops = 0
        created_products = 0
        updated_products = 0
        for cafe in CAFE_DATA:
            # Prefer an existing shop with the exact name, preserving its PK and linked orders.
            shop = Shop.objects.filter(name=cafe["name"]).first()
            if shop is None:
                owner = self._owner(cafe)
                shop = Shop.objects.filter(owner=owner).first()
                if shop is not None and shop.name != cafe["name"]:
                    # Never repurpose an unrelated shop belonging to an existing user.
                    owner = self._owner({**cafe, "username": f"{cafe['username']}_fresh"})
                    shop = Shop.objects.filter(owner=owner, name=cafe["name"]).first()
                if shop is None:
                    shop = Shop.objects.create(owner=owner, name=cafe["name"])
                    created_shops += 1

            logo = {
                "Café Reserve": "cafe_reserve.jpg",
                "Daily Grind Café": "daily_grind.jpg",
                "Frappé House": "frappe_house.jpg",
                "Boba & Brew Café": "boba_brew.jpg",
            }.get(cafe["name"], "cafe_reserve.jpg")
            shop.name = cafe["name"]
            shop.description = cafe["description"]
            shop.address = cafe["address"]
            shop.phone = cafe["phone"]
            # The image filter maps these bundled paths to /static, so Render needs no media disk.
            shop.logo = f"shop_logos/{logo}"
            shop.save()

            for name, description, category_name, price in cafe["products"]:
                defaults = {
                    "description": description,
                    "category": categories[category_name],
                    "price": Decimal(price),
                    "available": True,
                    "image": f"products/{self._product_image(name)}",
                }
                product, created = Product.objects.update_or_create(
                    shop=shop, name=name, defaults=defaults
                )
                if created:
                    created_products += 1
                else:
                    updated_products += 1

            offer_title, offer_description, discount = cafe["offer"]
            Offer.objects.update_or_create(
                shop=shop, title=offer_title,
                defaults={
                    "description": offer_description,
                    "discount_percent": discount,
                    "active": True,
                },
            )

        shop_count = Shop.objects.filter(name__in=[c["name"] for c in CAFE_DATA]).count()
        product_count = Product.objects.filter(
            shop__name__in=[c["name"] for c in CAFE_DATA]
        ).count()
        self.stdout.write(self.style.SUCCESS(
            f"CaféConnect showcase ready: {shop_count} cafés, {product_count} menu items "
            f"({created_shops} cafés and {created_products} products added; "
            f"{updated_products} existing menu items refreshed)."
        ))
        self.stdout.write("Existing customers, orders, reviews, and unrelated shops/products were not deleted.")
