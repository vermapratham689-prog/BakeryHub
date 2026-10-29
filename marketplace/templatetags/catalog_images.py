"""Template helpers for bundled demo photos that must work on local and hosted builds."""
from pathlib import Path
from django import template

register = template.Library()

PRODUCT_IMAGES = {
    "caramel_frappe.jpg", "latte.jpg", "caramel_macchiato.jpg",
    "vanilla_iced_latte.jpg", "espresso.jpg", "matcha_frappe.jpg",
    "iced_latte.jpg", "cappuccino.jpg", "cafe_roast.jpg", "sandwich.jpg",
    "mocha_frappe.jpg", "java_chip.jpg", "cafe_brew.jpg", "cafe_mocha.jpg",
    "cold_brew.jpg", "croissant.jpg", "cafe_boba.jpg", "iced_caramel.jpg",
}
CAFE_IMAGES = {"frappe_house.jpg", "daily_grind.jpg", "cafe_reserve.jpg", "boba_brew.jpg"}

@register.filter
def catalog_image(image_field, kind="product"):
    """Use packaged static photos for bundled demo assets; uploaded files keep their storage URL."""
    if not image_field:
        return ""
    name = Path(str(getattr(image_field, "name", ""))).name
    if kind == "cafe" and name in CAFE_IMAGES:
        return f"/static/images/cafes/{name}"
    if kind == "product" and name in PRODUCT_IMAGES:
        return f"/static/images/products/{name}"
    try:
        return image_field.url
    except (ValueError, AttributeError):
        return ""
