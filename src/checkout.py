"""Checkout flow module."""

from src.payment import process_payment


def checkout(cart_items: list, payment_method: str, user_id: str) -> dict:
    if not cart_items:
        raise ValueError("Cart is empty")
    if not user_id:
        raise ValueError("user_id is required")
    total = sum(item.get("price", 0) * item.get("qty", 1) for item in cart_items)
    payment = process_payment(total, payment_method)
    return {
        "order_id": f"ORD-{user_id}-001",
        "total": total,
        "payment": payment,
        "status": "confirmed",
    }


def apply_coupon(cart_total: float, coupon_code: str) -> float:
    coupons = {"SAVE10": 0.10, "SAVE20": 0.20}
    discount = coupons.get(coupon_code, 0)
    return round(cart_total * (1 - discount), 2)


def calculate_tax(amount: float, rate: float = 0.18) -> float:
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return round(amount * rate, 2)
