#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Observable

@Author: Paul Hempel
@Date:   09.04.2022
"""


class Observable:
    """
    A base class for anything that should allow you to observe something.
    """

    def __init__(self):
        self._beforeObserverList = []
        self._afterObserverList = []

    def add_before_observer(self, callback):
        """
        Adds a new observer that will call the given callback just before some event.

        Args:
            callback:   a callable
        """
        self._beforeObserverList.append(callback)

    def add_after_observer(self, callback):
        """
        Adds a new observer that will call the given callback just after some event.

        Args:
            callback:   a callable
        """
        self._afterObserverList.append(callback)

    def remove_before_observer(self, callback):
        """
        Removes an already added before-observer identified by its callback.

        Args:
            callback:   a callable
        """
        self._beforeObserverList.remove(callback)

    def remove_after_observer(self, callback):
        """
        Removes an already added after-observer identified by its callback.

        Args:
            callback:   a callable
        """
        self._afterObserverList.remove(callback)

    def _call_before_observers(self, *args, **kvargs):
        """
        This can be called to inform all added before-observers by calling their callback method with the given args and
        kvargs.

        Args:
            *args:      args given to the callback
            **kvargs:   kvargs given to the callback
        """
        for callback in self._beforeObserverList:
            callback(*args, **kvargs)

    def _call_after_observers(self, *args, **kvargs):
        """
        This can be called to inform all added after-observers by calling their callback method with the given args and
        kvargs.

        Args:
            *args:      args given to the callback
            **kvargs:   kvargs given to the callback
        """
        for callback in self._afterObserverList:
            callback(*args, **kvargs)


if __name__ == "__main__":
    pass
