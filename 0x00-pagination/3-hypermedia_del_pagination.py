#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict
from bs4 import element


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """_summary_

        Args:
            index (int, optional): the index of the first element in the page.
            Defaults to None.
            page_size (int, optional): the size of the page.
            Defaults to 10.

        Returns:
            Dict: a dictionary with the following key-value pairs:
                index: the current start index of the return data
                next_index: the next index to query with.
                None if end of dataset
                page_size: the current page size
                data: the current dataset page
        """
        assert index < len(self.__indexed_dataset)
        requested_data = []
        i = 0
        next_index = index
        while i < page_size:
            element = self.__indexed_dataset.get(next_index)
            if element:
                requested_data.append(element)
                i += 1
            next_index += 1
        return {
            'index': index,
            'next_index': next_index
            if list(self.__indexed_dataset.keys())[-1] >= index + page_size
            else None,
            'page_size': len(requested_data),
            'data': requested_data
        }
