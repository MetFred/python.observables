#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ObservableValue

@Author: Paul Hempel
@Date:   09.04.2022
"""
from observables.Observable import Observable


class ObservableValue(Observable):
    """
    A simple Observable holding a single value with the following features:
        - allow observing before and after value setting
        - allow binding to other ObservableValues synchronizing their values
        - the callbacks (before and after) gets the following parameters:
            + the instance of the calling ObservableValue
            + the old value before change
            + the new value after change
    """

    @staticmethod
    def bind(obs1, obs2):
        """
        Binds the two ObervableValues obs1 and obs2 together starting with obs2.bind_to(obd1) so obs1 value will be
        initially set to obs2!

        Args:
            obs1:   ObservableValue (the value of this observable will be set in obs2 after bind!)
            obs2:   ObservableValue
        """
        obs2.bind_to(obs1)
        obs1.bind_to(obs2)

    @staticmethod
    def unbind(obs1, obs2):
        """
        Unbinds the two ObervableValues obs1 and obs2 by calling their unbind_from methods.

        Args:
            obs1:   ObservableValue
            obs2:   ObservableValue
        """
        obs1.unbind_from(obs2)
        obs2.unbind_from(obs1)

    def __init__(self, initial_value=None):
        """
        Creates a new ObservableValue allowing you to set its initial value.

        Args:
            initial_value: the initial value (default None)
        """
        Observable.__init__(self)
        self._value = initial_value
        self._bindingMap = {}

    def set(self, new_value):
        """
        Sets the value and informing all registered observers before and after the value changes.

        Args:
            new_value:  The new value
        """
        if self._value == new_value:
            return
        old_value = self._value
        self._call_before_observers(self, old_value, new_value)
        self._value = new_value
        self._call_after_observers(self, old_value, new_value)

    def get(self):
        """
        Returns the actual value.

        Returns:
            the actual value
        """
        return self._value

    def bind_to(self, observable):
        """
        Bind this Observable to the given one so that the value of the ObservableValue will always by synchronized
        with the value of the given one. This will be applied by observing the given ObservableValue and set its own
        value after change events.

        Args:
            observable: ObservableValue
        """
        if not isinstance(observable, ObservableValue):
            raise TypeError("ObservableValue can only bind to other ObservableValues!")
        self._bindingMap[observable] = lambda _1, _2, n: self.set(n)
        observable.add_after_observer(self._bindingMap[observable])
        self.set(observable.get())

    def unbind_from(self, observable):
        """
        Unbind this Observable from the given one so that the value of the ObservableValue will no longer by
        synchronized with the value of the given one. This will be applied by stop observing the given ObservableValue.

        Args:
            observable: ObservableValue
        """
        if observable not in self._bindingMap:
            raise AttributeError("ObservableValue cannot unbind from an observable it was not bound to before!")
        self.remove_after_observer(self._bindingMap[observable])
        del(self._bindingMap[observable])


if __name__ == "__main__":
    o1 = ObservableValue(1)
    o1.add_after_observer(print)

    o1.set(2)
    o1.set(2)
    o1.set(3)

    print(o1.get())

    o2 = ObservableValue("a")
    o2.add_after_observer(print)
    ObservableValue.bind(o1, o2)



