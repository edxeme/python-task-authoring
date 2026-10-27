# Root cause & fix — off-by-one in `total_pages`

## Root cause

`total_pages` used floor division:

```python
return n_items // per_page
```

Floor division answers *"how many **full** pages fit?"* — but the API
contract is *"how many pages are needed to show every item?"*. Whenever
`n_items` is not an exact multiple of `per_page`, the final partial page is
truncated: 21 items at 10 per page → `21 // 10 == 2`, and the third page
(the one holding item 21) becomes unreachable in the UI.

## Failing tests first

The verifier pinned the contract before the fix:

- `test_total_pages_partial_last_page` — `total_pages(21, 10) == 3` (RED)
- `test_total_pages_single_item` — `total_pages(1, 25) == 1` (RED)

Everything else (exact multiples, empty collections, slicing, validation)
was already green — the fix must not disturb them.

## The fix

```python
return -(-n_items // per_page)
```

Ceiling division via the double-negation idiom: it rounds **up** to the
next page whenever there is a remainder, and is a no-op for exact
multiples.

### Why not `math.ceil(n_items / per_page)`?

`math.ceil` is the readable textbook answer, but it takes a **float**:
`n_items / per_page` is true division. For item counts beyond 2⁵³ the
quotient cannot represent every integer, and `math.ceil` can return a
wrong page count. Pagination sits on hot paths with unbounded page sizes
in admin tools (exports, "show all"); the integer-only idiom is exact for
arbitrarily large inputs and adds no import. Readability cost is paid once
by the comment above it.

## Regression check

Suite result before → after:

- task state: 7 passed, 2 failed (the two contract tests)
- patched: **9 passed** — no other behavior moved
