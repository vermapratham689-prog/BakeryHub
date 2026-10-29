from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import (
    Shop, Category, Product, Offer, Order, OrderItem, Review,
    Campaign, Coupon, MarketingEvent,
)

# Demonstration menu inspired by common international coffeehouse offerings.
# This is not an official Starbucks menu or affiliated with Starbucks.
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
    help = "Reset demo marketplace data and create four café showcases with coffeehouse-style menus. Destructive to existing shop/order demo data."

    def handle(self, *args, **options):
        # This command is intentionally a showcase reset: clear old bakery demo content
        # and its dependent records, while preserving Django user accounts.
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Review.objects.all().delete()
        MarketingEvent.objects.all().delete()
        Campaign.objects.all().delete()
        Coupon.objects.all().delete()
        Offer.objects.all().delete()
        Product.objects.all().delete()
        Shop.objects.all().delete()
        Category.objects.all().delete()

        category_names = sorted({item[2] for cafe in CAFE_DATA for item in cafe["products"]})
        categories = {}
        for index, name in enumerate(category_names):
            slug = name.lower().replace("&", "and").replace(" ", "-").replace("/", "-")
            # Ensure a unique slug if categories have similarly named labels.
            base_slug = slug
            suffix = 2
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            category, _ = Category.objects.get_or_create(name=name, defaults={"slug": slug})
            categories[name] = category

        for cafe in CAFE_DATA:
            owner, _ = User.objects.get_or_create(
                username=cafe["username"], defaults={"email": cafe["email"]}
            )
            owner.email = cafe["email"]
            owner.set_password("CafeDemo123!")
            owner.save()
            cafe_image = {
                "Café Reserve": "cafe_reserve.jpg",
                "Daily Grind Café": "daily_grind.jpg",
                "Frappé House": "frappe_house.jpg",
                "Boba & Brew Café": "boba_brew.jpg",
            }.get(cafe["name"], "cafe_reserve.jpg")
            shop = Shop.objects.create(
                owner=owner, name=cafe["name"], description=cafe["description"],
                address=cafe["address"], phone=cafe["phone"],
                logo=f"shop_logos/{cafe_image}",
            )
            for name, description, category_name, price in cafe["products"]:
                lower_name = name.lower()
                if "espresso" in lower_name or "americano" in lower_name or "cortado" in lower_name:
                    image_name = "espresso.jpg"
                elif "cappuccino" in lower_name or "matcha latte" in lower_name or "matcha green tea" in lower_name:
                    image_name = "cappuccino.jpg" if "matcha" not in lower_name else "matcha_frappe.jpg"
                elif "caramel macchiato" in lower_name:
                    image_name = "caramel_macchiato.jpg"
                elif "cold brew" in lower_name:
                    image_name = "cold_brew.jpg"
                elif "iced" in lower_name or "misto" in lower_name:
                    image_name = "iced_latte.jpg"
                elif "frapp" in lower_name or "blended" in lower_name or "java chip" in lower_name:
                    image_name = "mocha_frappe.jpg" if "mocha" in lower_name or "chocolate" in lower_name else "caramel_frappe.jpg"
                elif "tea" in lower_name or "boba" in lower_name or "bubble" in lower_name or "refresher" in lower_name or "mango" in lower_name:
                    image_name = "matcha_frappe.jpg"
                elif "croissant" in lower_name:
                    image_name = "croissant.jpg"
                elif "sandwich" in lower_name or "grilled cheese" in lower_name:
                    image_name = "sandwich.jpg"
                elif "brownie" in lower_name or "cookie" in lower_name or "puff" in lower_name:
                    image_name = "mocha_frappe.jpg"
                elif "mocha" in lower_name or "chocolate" in lower_name:
                    image_name = "mocha_frappe.jpg"
                else:
                    image_name = "latte.jpg"
                Product.objects.create(
                    shop=shop, name=name, description=description,
                    category=categories[category_name], price=Decimal(price), available=True,
                    image=f"products/{image_name}",
                )
            offer_title, offer_description, discount = cafe["offer"]
            Offer.objects.create(
                shop=shop, title=offer_title, description=offer_description,
                discount_percent=discount, active=True,
            )

        customer, _ = User.objects.get_or_create(
            username="demo_customer", defaults={"email": "customer@example.test"}
        )
        customer.set_password("CustomerDemo123!")
        customer.save()
        self.stdout.write(self.style.SUCCESS("CaféConnect demo data ready: four cafés, 48 menu items and four offers."))
        self.stdout.write("Demo café owners: demo_cafe_reserve, demo_daily_grind, demo_frappe_house, demo_boba_brew")
        self.stdout.write("Demo owner password: CafeDemo123!")
        self.stdout.write("Demo customer: demo_customer / CustomerDemo123!")
        self.stdout.write(self.style.WARNING("WARNING: This command deletes existing shops, products, offers, orders, reviews and marketing records. Back up your database first."))
