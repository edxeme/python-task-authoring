# 02 · Bug fix — off-by-one in `total_pages`

The admin API's paginator reports `total_pages` wrongly whenever the item
count is not an exact multiple of `per_page`. A customer with **21 items at
10 per page** sees **2 pages instead of 3** — the last, partial page is
unreachable in the UI.

## Your task

Fix the bug in `src/pagination.py` so the suite in `tests/` passes.

Constraints:

- Do not change any public signature.
- All other tests must stay green (no regression fixes that break valid paths).
- Keep the fix minimal; explain the root cause in your own words.

## Reproduce

```sh
docker build -t pta-02 . && docker run --rm pta-02   # RED: 2 failed
# or locally: python -m pytest tests/ -v
```

## Solution

`solution/` — the golden patch (`solution.patch`, apply with
`git apply examples/02-bugfix-pagination/solution/solution.patch` from the
repo root) and `EXPLANATION.md` with the root-cause analysis and why the
fix avoids `math.ceil`.
