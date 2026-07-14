"""Tests for payment module."""

import pytest
from src.payment import process_payment, refund_payment, get_payment_status


def test_process_payment_success():
    result = process_payment(100.0, "card")
    assert result["status"] == "success"
    assert result["amount"] == 100.0


def test_process_payment_upi():
    result = process_payment(250.0, "upi")
    assert result["status"] == "success"
    assert result["method"] == "upi"


def test_process_payment_invalid_method():
    with pytest.raises(ValueError, match="Unsupported payment method"):
        process_payment(100.0, "crypto")


def test_process_payment_zero_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        process_payment(0, "card")


def test_process_payment_max_retries():
    result = process_payment(100.0, "card", retries=3)
    assert result["status"] == "failed"
    assert result["reason"] == "max_retries_exceeded"


def test_refund_payment():
    result = refund_payment("TXN-001", 50.0)
    assert result["status"] == "refunded"
    assert result["transaction_id"] == "TXN-001"


def test_refund_invalid_id():
    with pytest.raises(ValueError, match="transaction_id is required"):
        refund_payment("", 50.0)


def test_get_payment_status():
    status = get_payment_status("TXN-001")
    assert status == "success"
