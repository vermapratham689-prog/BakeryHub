"""Template context helpers for shared navigation UI."""

def cart_summary(request):
    """Expose a safe cart quantity count to every template."""
    cart = request.session.get("cart", {})
    count = 0
    if isinstance(cart, dict):
        for quantity in cart.values():
            try:
                count += max(0, int(quantity))
            except (TypeError, ValueError):
                continue
    return {"cart_item_count": count}
