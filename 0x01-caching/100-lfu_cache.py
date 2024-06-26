#!/usr/bin/env python3
""" This module defines a class that inherits from BaseCaching
And works as a caching system. """
from base_caching import BaseCaching
from typing import Any


class LFUCache(BaseCaching):
    """ caching system class
    """

    def __init__(self):
        """ Instantiate """
        super().__init__()

        # elment_usage to track the usage of each key
        self.element_usage = {}

    def put(self, key: Any, item: Any) -> None:
        """ reimplements put method from the parent class
        by Adding an item in the cache
        """
        # if key or item is none do nothing
        if key and item:
            self.cache_data.update({key: item})
            # if key is not in element_usage, put the value to 0 else increment  
            usage = self.element_usage.get(key, None)
            if usage is None:
                self.element_usage.update({key: 0})
            else:
                self.element_usage[key] += 1

            # if the cache passes the limit, sort element_usage by value in ascending order
            # pass the first element if it is the new element
            # get the first key as the least frequent used key and drop it
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                usage_sorted = sorted(
                    self.element_usage.items(),
                    key=lambda item: item[1],
                    reverse=False
                    )
                lfu_key = usage_sorted[0][0]
                if key == lfu_key:
                    lfu_key = usage_sorted[1][0]
                self.cache_data.pop(lfu_key)
                self.element_usage.pop(lfu_key)
                print("DISCARD: {}".format(lfu_key))

    def get(self, key: Any) -> Any:
        """ reimplements get method from the parent class
        by Getting an item by key
        """
        element = self.cache_data.get(key, None)
        # increase the usage counter of this key
        if element:
            self.element_usage[key] += 1
        return element
