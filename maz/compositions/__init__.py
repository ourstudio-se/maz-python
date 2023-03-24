
from dataclasses import dataclass
from typing import Callable, Any
from time import sleep

@dataclass
class Retryer:

    """
        Calls input function until condition is met
        or number of retries equals `retries`.
    """

    retries:        int
    condition:      Callable[[Any], bool]

    def __call__(self, function, *args, **kwargs):

        ntry = 0
        result = function(*args, **kwargs)
        while not self.condition(result) and ntry < self.retries:
            result = function(*args, **kwargs)
            ntry += 1

        return result


@dataclass
class ExecuteAndTimeout:

    """
        Calls function then suspends execution of the current
        thread for the given number of seconds (timeout).
    """

    fn:         Callable[[Any], Any]
    timeout:    float
    
    def __call__(self, *args, **kwargs):    
        result = self.fn(*args, **kwargs)
        sleep(self.timeout)
        return result



@dataclass
class Property:

    """
        Names a given function
    """

    name: str
    fn: Callable[[Any], Any]

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.fn(args, kwds)