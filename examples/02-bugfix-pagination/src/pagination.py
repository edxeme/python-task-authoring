"""Pagination helpers for list-based collections.

Backs the page-size widget of an internal admin API. Reported bug:
``total_pages`` returns the wrong value whenever the item count is not an
exact multiple of ``per_page`` — the last, partial page is unreachable.
"""

from __future__ import annotations


def paginate(items: list, page: int = 0, per_page: int = 25) -> tuple[list, int]:
    """Return ``(items_on_page, total_pages)`` for 0-based *page*.

    Raises ``ValueError`` for negative pages or non-positive page sizes.
    Pages beyond the last item simply yield an empty list.
    """
    if per_page <= 0:
        raise ValueError("per_page must be positive")
    if page < 0:
        raise ValueError("page must be >= 0")
    total = total_pages(len(items), per_page)
    start = page * per_page
    return items[start : start + per_page], total


def total_pages(n_items: int, per_page: int) -> int:
    """Number of pages needed to show *n_items* with *per_page* per page."""
    if per_page <= 0:
        raise ValueError("per_page must be positive")
    return n_items // per_page  # BUG: truncates the final partial page
