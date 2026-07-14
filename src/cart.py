"""Cart management module."""


def add_item(cart: list, item: dict) -> list:
    if not item.get("id"):
        raise ValueError("Item must have an id")
    cart.append(item)
    return cart


def remove_item(cart: list, item_id: str) -> list:
    return [i for i in cart if i.get("id") != item_id]


def get_cart_total(cart: list) -> float:
    return sum(item.get("price", 0) * item.get("qty", 1) for item in cart)


def apply_bulk_discount(cart: list) -> float:
    total = get_cart_total(cart)
    # Discount tiers: 5% for 3+ items, 10% for 5+ items
    if len(cart) >= 5:
        return round(total * 0.85, 2)
    if len(cart) >= 3:
        return round(total * 0.92, 2)
    return total

