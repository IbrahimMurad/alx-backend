#!/usr/bin/env python3
""" This module defines a function
that specifies the indexes to show in a page """
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ return a tuple of size two containing
    a start index and an end index
    corresponding to the range of indexes to return in a list
    for those particular pagination parameters. """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ finds the correct indexes to paginate the dataset correctly
        and return the appropriate page of the dataset
        based on the page and page_size parameters. """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        range = index_range(page, page_size)
        data = self.dataset()
        if len(data) / page_size < page:
            return []
        return data[range[0]:range[1]]
