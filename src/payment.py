"""Payment processing module — v2 with multi-currency and transaction tracking."""
import uuid

MAX_RETRIES = 3
SUPPORTED_METHODS = ["card", "upi", "wallet"]
VALID_CURRENCIES = ["INR", "USD", "EUR", "GBP"]


def process_payment(amount: float, method: str, currency: str = "INR", retries: int = 0) -> dict:
    if method not in SUPPORTED_METHODS:
        raise ValueError(f"Unsupported payment method: {method}")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if currency not in VALID_CURRENCIES:
        raise ValueError(f"Unsupported currency: {currency}")
    if retries > MAX_RETRIES:
        return {"status": "failed", "reason": "max_retries_exceeded", "retries_attempted": retries}
    return {
        "status": "success",
        "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
        "amount": amount,
        "method": method,
        "currency": currency,
    }


def refund_payment(transaction_id: str, amount: float, reason: str = "customer_request") -> dict:
    if not transaction_id:
        raise ValueError("transaction_id is required")
    if amount <= 0:
        raise ValueError("Refund amount must be positive")
    return {
        "status": "refunded",
        "transaction_id": transaction_id,
        "amount": amount,
        "reason": reason,
    }


def get_payment_status(transaction_id: str, payments_db: dict = None) -> str:
    if not transaction_id:
        raise ValueError("transaction_id is required")
    if payments_db and transaction_id in payments_db:
        return payments_db[transaction_id].get("status", "unknown")
    return "success"
