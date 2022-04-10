#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ObservableObject

@Author: Paul Hempel
@Date:   09.04.2022
"""
from observables.Observable import Observable


class ObservableObject(Observable):
    """
    A complex Observable allowing to observe changes of any public attribute.
    The callbacks (before and after) will get the following parameters:
        + the instance of the calling ObservableObject
        + the operation that is used for the change (one of create, modify, delete)
        + the name of the property which changes
        + the old value of the property before change
        + the new value of the property after change
    """

    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"

    def __init__(self):
        Observable.__init__(self)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            return Observable.__setattr__(self, key, value)
        exists = hasattr(self, key)
        operation = ObservableObject.MODIFY if exists else ObservableObject.CREATE
        old_value = getattr(self, key) if exists else None
        if old_value == value and operation == ObservableObject.MODIFY:
            return
        self._call_before_observers(self, operation, key, old_value, value)
        Observable.__setattr__(self, key, value)
        self._call_after_observers(self, operation, key, old_value, value)

    def __delattr__(self, key):
        if key.startswith("_"):
            return Observable.__delattr__(self, key)
        old_value = getattr(self, key)
        self._call_before_observers(self, ObservableObject.DELETE, key, old_value, None)
        Observable.__delattr__(self, key)
        self._call_after_observers(self, ObservableObject.DELETE, key, old_value, None)


if __name__ == "__main__":
    oo = ObservableObject()

    oo.text = "a"
    oo.add_after_observer(print)
    oo.text = "a"
    oo.text = "b"
    oo.newOne = 4

    del oo.newOne
