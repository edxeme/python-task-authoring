"""Verifier suite — RED until the off-by-one in ``total_pages`` is fixed."""

import pytest

from src.pagination import paginate, total_pages


def test_total_pages_exact_multiple():
    assert total_pages(20, 10) == 2


def test_total_pages_partial_last_page():
    # 21 items at 10 per page need 3 pages, not 2.
    assert total_pages(21, 10) == 3


def test_total_pages_single_item():
    assert total_pages(1, 25) == 1


def test_total_pages_empty_collection():
    assert total_pages(0, 10) == 0


def test_paginate_returns_slice_and_total():
    items = list(range(21))
    page_items, total = paginate(items, page=2, per_page=10)
    assert page_items == [20]
    assert total == 3


def test_paginate_out_of_range_page_is_empty():
    page_items, total = paginate(list(range(20)), page=5, per_page=10)
    assert page_items == []
    assert total == 2


def test_paginate_first_page_default():
    page_items, total = paginate(list(range(45)), per_page=10)
    assert page_items == list(range(10))
    assert total == 5


@pytest.mark.parametrize("per_page", [0, -3])
def test_invalid_per_page_is_rejected(per_page):
    with pytest.raises(ValueError, match="per_page"):
        total_pages(10, per_page)


def test_negative_page_is_rejected():
    with pytest.raises(ValueError, match="page"):
        paginate(list(range(10)), page=-1)
