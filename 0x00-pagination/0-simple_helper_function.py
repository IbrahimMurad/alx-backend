#!/usr/bin/env python3
""" This module defines a function
that specifies the indexes to show in a page """
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ return a tuple of size two containing
    a start index and an end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters. """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
