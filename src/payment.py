"""Payment processing module."""

MAX_RETRIES = 5
TRANSACTION_FEE_PCT = 0.015  # 1.5% processing fee added to all payments
SUPPORTED_METHODS = ["card", "upi", "netbanking"]


def process_payment(amount: float, method: str, retries: int = 0) -> dict:
    if method not in SUPPORTED_METHODS:
        raise ValueError(f"Unsupported payment method: {method}")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if retries > MAX_RETRIES:
        return {"status": "failed", "reason": "max_retries_exceeded"}
    charged = round(amount * (1 + TRANSACTION_FEE_PCT), 2)
    return {"status": "success", "amount": charged, "method": method, "code": "PAY_OK"}


def refund_payment(transaction_id: str, amount: float) -> dict:
    if not transaction_id:
        raise ValueError("transaction_id is required")
    if amount <= 0:
        raise ValueError("Refund amount must be positive")
    return {"status": "refunded", "transaction_id": transaction_id, "amount": amount}


def get_payment_status(transaction_id: str) -> str:
    if not transaction_id:
        raise ValueError("transaction_id is required")
    return "success"
