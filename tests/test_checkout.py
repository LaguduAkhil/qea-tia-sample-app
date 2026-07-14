"""Tests for checkout module."""

import pytest
from src.checkout import checkout, apply_coupon, calculate_tax


def test_checkout_success():
    cart = [{"id": "P1", "price": 100.0, "qty": 2}]
    result = checkout(cart, "card", "user123")
    assert result["status"] == "confirmed"
    assert result["total"] == 200.0


def test_checkout_empty_cart():
    with pytest.raises(ValueError, match="Cart is empty"):
        checkout([], "card", "user123")


def test_checkout_no_user():
    cart = [{"id": "P1", "price": 50.0, "qty": 1}]
    with pytest.raises(ValueError, match="user_id is required"):
        checkout(cart, "card", "")


def test_apply_coupon_save10():
    result = apply_coupon(100.0, "SAVE10")
    assert result == 90.0


def test_apply_coupon_save20():
    result = apply_coupon(100.0, "SAVE20")
    assert result == 80.0


def test_apply_coupon_invalid():
    result = apply_coupon(100.0, "INVALID")
    assert result == 100.0


def test_calculate_tax_default():
    assert calculate_tax(100.0) == 18.0


def test_calculate_tax_custom_rate():
    assert calculate_tax(200.0, 0.05) == 10.0


def test_calculate_tax_negative():
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        calculate_tax(-50.0)
