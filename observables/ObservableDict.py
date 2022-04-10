#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ObservableDict

@Author: Paul Hempel
@Date:   09.04.2022
"""
from observables.Observable import Observable


class ObservableDict(dict, Observable):
    """
    A simple dictionary Observable allowing to observe changes of any item.
    The callbacks (before and after) will get the following parameters:
        + the instance of the calling ObservableDict
        + the operation that is used for the change (one of create, modify, delete or clear)
        + the key of the item which changes
        + the old value of the property before change
        + the new value of the property after change
    """

    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"
    CLEAR = "clear"

    def __init__(self, seq=None, **kwargs):
        if seq:
            dict.__init__(self, seq, **kwargs)
        else:
            dict.__init__(self, **kwargs)
        Observable.__init__(self)

    def clear(self):
        """
        Remove all items of this ObservableDict.
        (CAUTION: This will call the callbacks only once with operation "clear" instead of single "delete" calls!)
        """
        self._call_before_observers(self, ObservableDict.CLEAR, None, None, None)
        dict.clear(self)
        self._call_after_observers(self, ObservableDict.CLEAR, None, None, None)

    def pop(self, key, default=None):
        """
        Removes the item related to key and return its value or the given default value if item not found.

        Args:
            key:        The key of the item to pop
            default:    The value returned if no item found (default: None)

        Returns:
            The value of the item related to key or the default value if no item found.
        """
        old_value = self[key]
        self._call_before_observers(self, ObservableDict.DELETE, key, old_value, None)
        result = dict.pop(self, key, default)
        self._call_after_observers(self, ObservableDict.DELETE, key, old_value, None)
        return result

    def popitem(self):
        """
        Removes the last item found in the ObservableDict (should be the last putted item) and returns a tuple with
        the key and the value related to that item.

        Returns:
            A tuple with the popped key and the value of the item related to this key
        """
        key, old_value = list(self.items())[-1]
        self._call_before_observers(self, ObservableDict.DELETE, key, old_value, None)
        dict.popitem(self)
        self._call_after_observers(self, ObservableDict.DELETE, key, old_value, None)
        return key, old_value

    def update(self, data=None, **kvargs):
        """
        Take all items first from data and then from **kvargs and put them to this ObservableDict. So this will call
        the observers on every put operation it does!

        Args:
            data:       dict or list of tuples
            **kvargs:   additional key-value-pairs
        """
        if not data:
            return
        if isinstance(data, dict):
            for k in data.keys():
                self[k] = data[k]
            return
        else:
            for k,v in data:
                self[k] = v
        for k in kvargs:
            self[k] = kvargs[k]

    def __repr__(self):
        return f"ObservableDict({dict.__repr__(self)[1:-1]})"

    def __setitem__(self, key, value):
        exists = key in self
        operation = ObservableDict.MODIFY if exists else ObservableDict.CREATE
        old_value = self[key] if exists else None
        if old_value == value and operation == ObservableDict.MODIFY:
            return
        self._call_before_observers(self, operation, key, old_value, value)
        dict.__setitem__(self, key, value)
        self._call_after_observers(self, operation, key, old_value, value)

    def __delitem__(self, key):
        old_value = self[key]
        self._call_before_observers(self, ObservableDict.DELETE, key, old_value, None)
        dict.__delitem__(self, key)
        self._call_after_observers(self, ObservableDict.DELETE, key, old_value, None)


if __name__ == "__main__":
    od = ObservableDict()

    od["a"] = 5

    od.add_after_observer(print)

    od["a"] = 5
    od["a"] = 6
    od["b"] = 7

    del(od["a"])

    od.pop("b")

    od.update({"foo": 3, "bar": 5})

    od.popitem()

    od.clear()
