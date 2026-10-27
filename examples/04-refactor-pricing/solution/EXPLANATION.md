# Refactor equivalence argument — `price_order`

The refactor changes **structure only**. Here is the point-by-point
argument that the characterization suite cannot distinguish old from new.

## 1. Empty / missing items

Legacy: `if items: ... else: raise ValueError("order has no items")`.
Refactor: `if not items: raise ...` — a guard clause with identical
message. `{"items": []}` and `{}` both take the same raise either way.

## 2. Quantity validation

Legacy accumulated items with `qty > 0` and raised on the first non-positive
one; the refactor raises **before** adding (`if qty <= 0: raise`). In both
versions earlier items are summed before the raise, the exception type is
`ValueError`, and the message is `f"invalid quantity {qty!r}"` — the caller
cannot observe the difference. Note the inverted condition: guard clauses
express the *error* path first, removing one indentation level.

## 3. Tier resolution

The legacy ladder (`if gold / else if silver / else if standard / else
raise`) becomes a lookup in `_TIER_DISCOUNTS` plus one membership guard:

- Known tiers: same discount, same float literals (0.15 / 0.10 / 0.0), so
  the arithmetic is bit-for-bit identical — table-driven does not change
  the numbers, only the mapping's shape.
- Unknown tier: same `ValueError(f"unknown tier {tier!r}")` message, and it
  still fires **after** the subtotal loop, exactly like the legacy code.

The missing-`customer` case (`order.get("customer") or {}`) and the
missing-`tier` default (`"standard"`) are preserved verbatim.

## 4. Bulk floor

`max(discount, 0.05)` for `subtotal > 1000.0` is unchanged, with the magic
numbers named (`_BULK_THRESHOLD`, `_BULK_FLOOR`). The strict `>` boundary
is load-bearing: at exactly 1000.00 there is no bulk discount
(`test_bulk_boundary_at_exactly_1000_no_bulk_discount` pins it).

## 5. The dead assignment

Legacy computed `subtotal = total` — an alias with no behavior. The
refactor accumulates directly into `subtotal`. Removing dead assignments
is safe by definition and is exactly the kind of noise the characterization
suite exists to protect while deleting.

## 6. What the suite proves

15 characterization tests, green before and after: returns for every tier,
the bulk floor, the boundary, rounding, all four error paths. Any
observable drift would have turned the suite red — the refactor's safety
is the suite's job, not the author's confidence.
