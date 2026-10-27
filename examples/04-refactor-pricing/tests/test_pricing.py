"""Characterization suite — must stay green BEFORE and AFTER the refactor.

Every externally observed behavior of the legacy module is pinned here.
"""

import pytest

from src.pricing import price_order


def item(qty=1, unit_price=0.0):
    return {"qty": qty, "unit_price": unit_price}


def test_standard_tier_no_discount():
    order = {"items": [item(qty=2, unit_price=10.0)], "customer": {"tier": "standard"}}
    assert price_order(order) == 20.0


def test_gold_tier_gets_15_percent():
    order = {"items": [item(qty=2, unit_price=100.0)], "customer": {"tier": "gold"}}
    assert price_order(order) == 170.0


def test_silver_tier_gets_10_percent():
    order = {"items": [item(qty=4, unit_price=25.0)], "customer": {"tier": "silver"}}
    assert price_order(order) == 90.0


def test_missing_customer_is_standard():
    order = {"items": [item(qty=1, unit_price=50.0)]}
    assert price_order(order) == 50.0


def test_missing_tier_is_standard():
    order = {"items": [item(qty=1, unit_price=50.0)], "customer": {}}
    assert price_order(order) == 50.0


def test_bulk_subtotal_gets_at_least_5_percent():
    order = {"items": [item(qty=3, unit_price=400.0)], "customer": {"tier": "standard"}}
    # subtotal 1200 -> max(0.0, 0.05) -> 1200 * 0.95
    assert price_order(order) == 1140.0


def test_bulk_does_not_reduce_gold_discount():
    order = {"items": [item(qty=3, unit_price=400.0)], "customer": {"tier": "gold"}}
    assert price_order(order) == 1020.0


def test_bulk_boundary_at_exactly_1000_no_bulk_discount():
    order = {"items": [item(qty=1, unit_price=1000.0)], "customer": {"tier": "standard"}}
    assert price_order(order) == 1000.0


def test_result_is_rounded_to_cents():
    order = {"items": [item(qty=3, unit_price=3.33)], "customer": {"tier": "gold"}}
    # 9.99 * 0.85 = 8.4915 -> 8.49
    assert price_order(order) == 8.49


def test_missing_qty_defaults_to_one():
    order = {"items": [{"unit_price": 12.5}], "customer": {"tier": "standard"}}
    assert price_order(order) == 12.5


def test_missing_unit_price_defaults_to_zero():
    order = {"items": [{"qty": 2}], "customer": {"tier": "standard"}}
    assert price_order(order) == 0.0


def test_empty_items_raise():
    with pytest.raises(ValueError, match="no items"):
        price_order({"items": [], "customer": {"tier": "gold"}})


def test_missing_items_raise():
    with pytest.raises(ValueError, match="no items"):
        price_order({"customer": {"tier": "gold"}})


def test_nonpositive_qty_raises():
    order = {"items": [item(qty=0, unit_price=5.0)]}
    with pytest.raises(ValueError, match="invalid quantity"):
        price_order(order)


def test_unknown_tier_raises():
    order = {"items": [item(unit_price=5.0)], "customer": {"tier": "platinum"}}
    with pytest.raises(ValueError, match="unknown tier"):
        price_order(order)
