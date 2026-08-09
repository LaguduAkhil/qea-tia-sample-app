"""
Complex payment tests — dict-equality, structural, and integration assertions
that require LLM reasoning to fix when the payment module changes.
"""
import pytest
from src.payment import (
    process_payment,
    refund_payment,
    get_payment_status,
    SUPPORTED_METHODS,
    MAX_RETRIES,
)


def test_process_payment_full_response_structure():
    """Exact dict equality — fails when new fields are added or removed."""
    result = process_payment(100.0, "card")
    assert result == {"status": "success", "amount": 100.0, "method": "card"}


def test_process_payment_no_extra_fields():
    """Response must not contain transaction_id or currency."""
    result = process_payment(250.0, "upi")
    assert "transaction_id" not in result
    assert "currency" not in result


def test_process_payment_netbanking_is_supported():
    """netbanking must be in SUPPORTED_METHODS — fails if removed."""
    assert "netbanking" in SUPPORTED_METHODS
    result = process_payment(500.0, "netbanking")
    assert result["status"] == "success"
    assert result["method"] == "netbanking"


def test_process_payment_fails_at_retries_3():
    """MAX_RETRIES=2 means retries=3 > 2 triggers failure path."""
    result = process_payment(100.0, "card", retries=3)
    assert result == {"status": "failed", "reason": "max_retries_exceeded"}


def test_process_payment_succeeds_at_exact_max_retries():
    """retries=MAX_RETRIES is NOT over the limit — must succeed."""
    result = process_payment(100.0, "card", retries=MAX_RETRIES)
    assert result["status"] == "success"


def test_refund_exact_response_structure():
    """Exact 3-key dict — fails when reason or other fields are added."""
    result = refund_payment("TXN-ABC-001", 75.0)
    assert result == {
        "status": "refunded",
        "transaction_id": "TXN-ABC-001",
        "amount": 75.0,
    }


def test_process_payment_retries_as_positional_arg():
    """Passes retries as 3rd positional argument — breaks when currency is inserted before it."""
    result = process_payment(200.0, "card", 0)
    assert result["status"] == "success"
    assert result["amount"] == 200.0


def test_checkout_payment_field_matches_process_payment():
    """Integration: checkout() payment field must exactly match process_payment() response."""
    from src.checkout import checkout
    order = checkout(
        [{"id": "P1", "price": 100.0, "qty": 1}], "card", "user42"
    )
    assert order["payment"] == {"status": "success", "amount": 100.0, "method": "card"}
    assert order["total"] == 100.0
    assert order["status"] == "confirmed"
