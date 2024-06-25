#!/usr/bin/env python3
""" This module defines a class that inherits from BaseCache
And adds or modifies some features. """
from base_caching import BaseCaching
from typing import Any


class BasicCache(BaseCaching):
    """ implements put and get methods """

    def put(self, key: Any, item: Any) -> None:
        """ reimplements put method from the parent class
        by Adding an item in the cache
        """
        if key and item:
            self.cache_data.update({key: item})

    def get(self, key: Any) -> Any:
        """ reimplements get method from the parent class
        by Getting an item by key
        """
        return self.cache_data.get(key, None)
