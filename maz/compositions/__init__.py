from dataclasses import dataclass
from typing import Callable, Any
from time import sleep
from functools import partial
from maz import compose

class retry_until:

    """
        Calls input function until condition is met
        or number of retries equals `retries`.
    """

    def __init__(self, function, retries: int, condition: Callable[[Any], bool]):
        if retries < 1:
            raise ValueError(f"`retries` must be greater or equal to 1, got {retries}")

        self.function = function
        self.retries = retries
        self.condition = condition

    def __call__(self, *args, **kwargs):

        for i in range(self.retries):
            result = self.function(*args, **kwargs)
            if self.condition(result):
                return result

        return result

class waiting:
    
    """
        Returns a new function that when executed will wait `in_seconds` seconds 
        before executing the original function.
    """

    def __init__(self, function, in_seconds: float):
        self.function = function
        self.in_seconds = in_seconds

    def __call__(self, *args, **kwargs):
        sleep(self.in_seconds)
        return self.function(*args, **kwargs)

class named:

    """
        Returns an object with properties name and function.
    """

    name: str
    function: Callable[[Any], Any]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.function(args, kwds)