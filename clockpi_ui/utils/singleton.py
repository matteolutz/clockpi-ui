# Source - https://stackoverflow.com/a
# Posted by Paul Manta, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-18, License - CC BY-SA 3.0

from typing import Generic, Optional, Type, TypeVar

T = TypeVar("T")


class Singleton(Generic[T]):
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated: Type[T]):
        self._decorated: Type[T] = decorated
        self._instance: Optional[T] = None

    def instance(self) -> T:
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """

        if self._instance is None:
            self._instance = self._decorated()
        return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
