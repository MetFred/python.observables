#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ObservableList

@Author: Paul Hempel
@Date:   09.04.2022
"""
from utils.observables.Observable import Observable


class ObservableList(list, Observable):
    """
    A simple list Observable allowing to observe changes of any item.
    The callbacks (before and after) will get the following parameters:
        + the instance of the calling ObservableList
        + the operation that is used for the change
          (one of append, insert, modify, delete, clear, extend, reverse or sort)
        + the index of the element which changes
        + the old value of the property before change
        + the new value of the property after change
    """

    APPEND = "append"
    INSERT = "insert"
    MODIFY = "modify"
    DELETE = "delete"
    CLEAR = "clear"
    EXTEND = "extend"
    REVERSE = "reverse"
    SORT = "sort"

    def __init__(self, seq=()):
        list.__init__(self, seq)
        Observable.__init__(self)

    def append(self, value):
        """
        Appends a single value to the end of the ObservableList.

        Args:
            value:  The value to append
        """
        index = len(self)
        self._call_before_observers(self, ObservableList.APPEND, index, None, value)
        list.append(self, value)
        self._call_after_observers(self, ObservableList.APPEND, index, None, value)

    def clear(self):
        """
        Remove all items of this ObservableList.
        (CAUTION: This will call the callbacks only once with operation "clear" instead of single "delete" calls!)
        """
        self._call_before_observers(self, ObservableList.CLEAR, None, None, None)
        list.clear(self)
        self._call_after_observers(self, ObservableList.CLEAR, None, None, None)

    def extend(self, iterable):
        """
        Appends all elements of the given iterable to the ObservableList.

        Args:
            iterable:   any iterable
        """
        index = len(self)
        self._call_before_observers(self, ObservableList.EXTEND, index, None, iterable)
        list.extend(self, iterable)
        self._call_after_observers(self, ObservableList.EXTEND, index, None, iterable)

    def insert(self, index, value):
        """
        Inserts a value at the given index. The index of all elements starting from the given index will be increment by
        one.
        CAUTION: This cannot be used to append new elements!

        Args:
            index:  The index to insert
            value:  The value to insert
        """
        old_value = self[index] if index < len(self) else None
        self._call_before_observers(self, ObservableList.INSERT, index, old_value, value)
        list.insert(self, index, value)
        self._call_after_observers(self, ObservableList.INSERT, index, old_value, value)

    def pop(self, index=-1):
        """
        Removes the value at given index returning the value at this position.

        Args:
            index:  The index to remove (default -1, last element)

        Returns:
            The value at given index.
        """
        old_value = self[index]
        self._call_before_observers(self, ObservableList.DELETE, index, old_value, None)
        result = list.pop(self, index)
        self._call_after_observers(self, ObservableList.DELETE, index, old_value, None)
        return result

    def remove(self, value):
        """
        Removes the first occurence of the given value.

        Args:
            value:  The value to remove
        """
        index = self.index(value)
        self._call_before_observers(self, ObservableList.DELETE, index, value, None)
        list.remove(self, value)
        self._call_after_observers(self, ObservableList.DELETE, index, value, None)

    def reverse(self):
        """
        Reverse the order of the ObservableList in-place.
        """
        self._call_before_observers(self, ObservableList.REVERSE, None, None, None)
        list.reverse(self)
        self._call_after_observers(self, ObservableList.REVERSE, None, None, None)

    def sort(self, key=None, reverse=False):
        """
        Sort the ObservableList in-place.
        CAUTION: To hold same count of callback parameters and to bring some information to observers the last
        two parameters of the callback will be the used key for sorting and the reverse value! Index will be None.

        Args:
            key:        Optional function to map the values to a key for sorting
            reverse:    If True the order will be descending else ascending (default False)
        """
        self._call_before_observers(self, ObservableList.SORT, None, key, reverse)
        list.sort(self, key=key, reverse=reverse)
        self._call_after_observers(self, ObservableList.SORT, None, key, reverse)

    def __repr__(self):
        return f"ObservableList({list.__repr__(self)[1:-1]})"

    def __setitem__(self, index, value):
        old_value = self[index]
        if old_value == value:
            return
        self._call_before_observers(self, ObservableList.MODIFY, index, old_value, value)
        list.__setitem__(self, index, value)
        self._call_after_observers(self, ObservableList.MODIFY, index, old_value, value)

    def __delitem__(self, index):
        old_value = self[index]
        self._call_before_observers(self, ObservableList.DELETE, index, old_value, None)
        dict.__delitem__(self, index)
        self._call_after_observers(self, ObservableList.DELETE, index, old_value, None)


if __name__ == "__main__":
    ol = ObservableList()
    ol.add_after_observer(print)
    ol.append("a")
    ol.extend(["b", 3, "d"])
    ol.insert(1, "c")
    ol.pop(-1)
    ol[1] = "foobar"
    ol[1:] = "foo"
    ol.remove("a")
    ol.reverse()
    ol.sort(key=lambda v: str(v))
    ol.clear()
