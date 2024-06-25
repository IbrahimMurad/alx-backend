#!/usr/bin/env python3
""" This module defines a class that inherits from BaseCaching
And works as a caching system. """
from base_caching import BaseCaching
from typing import Any


class LIFOCache(BaseCaching):
    """ caching system class
    """

    def put(self, key: Any, item: Any) -> None:
        """ reimplements put method from the parent class
        by Adding an item in the cache
        """
        if key and item:
            self.cache_data.update({key: item})
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                last_in_key = list(self.cache_data.keys())[-2]
                self.cache_data.pop(last_in_key)
                print("DISCARD: {}".format(last_in_key))

    def get(self, key: Any) -> Any:
        """ reimplements get method from the parent class
        by Getting an item by key
        """
        return self.cache_data.get(key, None)
