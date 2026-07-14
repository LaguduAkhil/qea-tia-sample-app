# QEA TIA Sample App

Sample e-commerce backend used to test the GenieQ Test Impact Analysis (TIA) pipeline.

## Modules

| Module | File | Description |
|---|---|---|
| Payment | `src/payment.py` | Payment processing, refunds, status |
| Auth | `src/auth.py` | Token generation and validation |
| Checkout | `src/checkout.py` | Checkout flow, coupons, tax |
| Cart | `src/cart.py` | Cart management, bulk discounts |

## Run tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Branch strategy (for TIA demo)

| Branch | Change | Expected test impact |
|---|---|---|
| `main` | Baseline | 1 pre-existing failure in `test_cart.py::test_empty_cart_discount` |
| `feature/payment-update` | Retry logic + return format changed | 2 new payment failures + 1 checkout failure (cross-module) |
| `feature/auth-refactor` | Token validation tightened | 1 new auth failure |
| `feature/bugfix-checkout` | Null-check fix | All pass — clean merge |
| `feature/cart-discount` | Discount calculation changed | 2 new cart failures (1 auto-fixable) + pre-existing |
