"""Order pricing rules — legacy module scheduled for refactor.

Behavior is locked by ``tests/test_pricing.py`` (characterization suite).
The task: refactor for readability without changing any externally
observed result.
"""

from __future__ import annotations


def price_order(order: dict) -> float:
    """Compute the final price in USD for an order dict."""
    total = 0.0
    items = order.get("items", [])
    if items:
        for item in items:
            qty = item.get("qty", 1)
            price = item.get("unit_price", 0.0)
            if qty > 0:
                total += qty * price
            else:
                raise ValueError(f"invalid quantity {qty!r}")
    else:
        raise ValueError("order has no items")

    subtotal = total
    customer = order.get("customer") or {}
    tier = customer.get("tier", "standard")
    if tier == "gold":
        discount = 0.15
    else:
        if tier == "silver":
            discount = 0.10
        else:
            if tier == "standard":
                discount = 0.0
            else:
                raise ValueError(f"unknown tier {tier!r}")

    if subtotal > 1000.0:
        discount = max(discount, 0.05)

    return round(subtotal * (1 - discount), 2)
