# 04 · Refactor — legacy pricing to guard clauses, behavior unchanged

`src/pricing.py` is a legacy module with deeply nested conditionals. Its
behavior is locked by the characterization suite in `tests/` — the suite
must be green **before and after** your change.

## Your task

Refactor `price_order` for readability and safety:

- Replace the nested tier logic with guard clauses (early raises).
- Make the tier → discount mapping table-driven.
- Keep every externally observed result identical: same returns, same
  exception types, same exception messages.
- Do not change the function signature.

## Reproduce

```sh
docker build -t pta-04 . && docker run --rm pta-04   # GREEN (baseline)
# or locally: python -m pytest tests/ -v
```

## Solution

`solution/` — the golden patch (`solution.patch`) and `EXPLANATION.md`
arguing equivalence point by point: why the suite cannot tell the
difference between old and new implementations.
