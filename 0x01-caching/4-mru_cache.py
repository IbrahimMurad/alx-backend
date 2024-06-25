#!/usr/bin/env python3
""" This module defines a class that inherits from BaseCaching
And works as a caching system. """
from base_caching import BaseCaching
from typing import Any


class MRUCache(BaseCaching):
    """ caching system class
    """

    def __init__(self):
        """ Instantiate """
        super().__init__()
        self.usage_counter = 0
        self.element_usage = {}

    def put(self, key: Any, item: Any) -> None:
        """ reimplements put method from the parent class
        by Adding an item in the cache
        """
        if key and item:
            self.cache_data.update({key: item})
            self.element_usage.update({key: self.usage_counter})
            self.usage_counter += 1
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                mru_key = sorted(
                    self.element_usage.items(),
                    key=lambda item: item[1],
                    reverse=True
                    )[1][0]
                self.cache_data.pop(mru_key)
                self.element_usage.pop(mru_key)
                print("DISCARD: {}".format(mru_key))

    def get(self, key: Any) -> Any:
        """ reimplements get method from the parent class
        by Getting an item by key
        """
        element = self.cache_data.get(key, None)
        if element:
            self.element_usage.update({key: self.usage_counter})
            self.usage_counter += 1
        return element
