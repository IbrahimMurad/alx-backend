#!/usr/bin/env python3
""" This module defines a function
that specifies the indexes to show in a page """
import csv
import math
from typing import List, Mapping, Tuple


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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Mapping:
        """ returns a dictionary containing the following key-value pairs:

            page_size:      the length of the returned dataset page
            page:           the current page number
            data:           the dataset page (equivalent to return from previous task)
            next_page:      number of the next page, None if no next page
            prev_page:      number of the previous page, None if no previous page
            total_pages:    the total number of pages in the dataset as an integer """
        requested_data = self.get_page(page, page_size)
        return {
            "page_size": len(requested_data),
            "page": page,
            "data": requested_data,
            "next_page": page + 1 if len(self.get_page(page + 1, page_size)) > 0 else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": len(self.dataset()) // page_size
                            + (1 if len(self.dataset()) % page_size > 0 else 0)
        }
