"""Tests for cart module."""

import pytest
from src.cart import add_item, remove_item, get_cart_total, apply_bulk_discount


def test_add_item():
    cart = add_item([], {"id": "P1", "price": 50.0, "qty": 1})
    assert len(cart) == 1


def test_add_item_no_id():
    with pytest.raises(ValueError, match="Item must have an id"):
        add_item([], {"price": 50.0})


def test_remove_item():
    cart = [{"id": "P1", "price": 50.0, "qty": 1}, {"id": "P2", "price": 30.0, "qty": 2}]
    result = remove_item(cart, "P1")
    assert len(result) == 1
    assert result[0]["id"] == "P2"


def test_get_cart_total():
    cart = [{"id": "P1", "price": 50.0, "qty": 2}, {"id": "P2", "price": 30.0, "qty": 1}]
    assert get_cart_total(cart) == 130.0


def test_get_cart_total_empty():
    assert get_cart_total([]) == 0.0


def test_bulk_discount_5_items():
    cart = [{"id": f"P{i}", "price": 20.0, "qty": 1} for i in range(5)]
    assert apply_bulk_discount(cart) == 90.0


def test_bulk_discount_3_items():
    cart = [{"id": f"P{i}", "price": 20.0, "qty": 1} for i in range(3)]
    assert apply_bulk_discount(cart) == 57.0


# PRE-EXISTING BROKEN TEST — wrong expected value, was never fixed in main
def test_empty_cart_discount():
    result = apply_bulk_discount([])
    assert result == 5.0  # Bug: should be 0.0, intentionally wrong to simulate pre-existing failure
