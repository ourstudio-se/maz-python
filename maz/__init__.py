import functools
import typing
import operator
import itertools

# functional composition functions
def sorted_pos(iterable, key=None) -> typing.Iterable:

    """
        Since python's "sorted" does not support positional
        argument and one requirement is that a pure function should
        always allow positional arguments, then here's a forwarding
        function.

        Return:
            iterable
    """

    return sorted(iterable, key=key)


def cached_execution(cache: dict, key: str, function: typing.Callable, *args, **kwargs) -> tuple:
    """
        If key is in cache, cache[key] is returned, else
        function is executed and its result stored in cache.

        Example:
            Inputs: 
                cache = {"a": 1}
                key = "b"
                function = lambda x: x+1
                args = [1]

            Ouput:
                ({"a": 1, "b": 2}, 2)

        Return:
            tuple: (cache,)
    """
    if not key in cache:
        cache[key] = function(*args,**kwargs)

    return cache, cache[key]


def starzip(iterables: list):

    """
        Calls zip with `iterable` as positional
        arguments, as such -> zip(*iterable)
    """

    return zip(*iterables)


def pospartial(function, positional_arguments):

    """
        `pospartial` is a complementing function to functools.partial, where
        one can say which positional argument should be hardcoded into function.
        Usually, this is solved by instead setting a keyword argument and thus
        indirectly setting a certain argument but some python functions doesn't take
        any keyword arguments.

        Example, let say you want to compile y=32 and z=19 on function f(x,y,z) = x+y+z.
        Then you simply do
            _f = pospartial(
                function=f,
                positional_arguments=[
                    (1, 32),
                    (2, 19),
                ]
            )

        and later run _f as:
            res = _f(23)
        which yield
            res == 23+32+19 == 74

        Returns
        -------
            out : Callable
    """

    def wrapper(*args, fn=function, pas=positional_arguments, **kwargs):
        nargs = list(args)
        for i, pa in pas:
            nargs.insert(i, pa)
        return fn(*nargs, **kwargs)
    return wrapper


class compose_pair:
    """
        Composes new function h = f(g(x)), from
        f and g.

        Example:
            >>> inc = lambda x: x+1
            >>> double = lambda x: x*2
            >>> h = compose_pair(double, inc)
            >>> h(1)
            >>> 4

        Returns
        -------
            out : Callable
    """

    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __call__(self, *args, **kwargs):
        return self.f(
            self.g(*args, **kwargs)
        )


class compose:

    """
        Sequence composite functions of `functions`.
        E.g. let fns be a list of functions [f, g, h] and
        compose(fns) would then represent lambda x : f(g(h(x)))

        Examples
        --------
            >>> inc = lambda x: x+1
            >>> double = lambda x: x*2
            >>> f = compose(inc, double, inc)
            >>> f(2)
            7

        Returns
        -------
            out : Callable
    """

    def __init__(self, *functions):
        self.fn = functools.reduce(compose_pair, functions)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class fnmap:

    """
        Runs an iterable of functions with same arguments.
        Returns an iterable of result from each of the functions.

        Examples
        --------
            >>> fn = fnmap(lambda x: x+1, lambda x: x+2)
            >>> list(fn(3))
            [4, 5]

            >>> def add_one(x): return x+1
            >>> def mul_two(x): return x*2
            >>> fn = fnmap(add_one, mul_two)
            >>> list(fn(x=3))
            [4, 6]

        Returns
        -------
            out : Callable
    """

    def __init__(self, *functions):
        self.functions = functions
    
    def __call__(self, *args, **kwargs):
        return map(
            lambda fn: fn(*args, **kwargs),
            self.functions
        )


def indexing(lst: list, index_item):

    """
        Indexing function, taking a list and what to
        index, as such lst[index_item].
    """
    return lst[index_item]


def invoke(fn, args: list = [], kwargs: dict = {}):

    """
        Invokes function fn with positional arguments in args and
        keyword arguments in kwargs.

        Example:
            >>> invoke(add, [1, 2])
            >>> 3

        Return:
            Any
    """

    return fn(*args, **kwargs)


def invoke_star(fn, *args, **kwargs):
    """
        Invokes function fn with positional arguments in args and
        keyword arguments in kwargs.

        Example:
            >>> invoke(add, 1, 2)
            >>> 3

        Return:
            Any
    """
    return invoke(fn, args, kwargs)


def args2list(*args):
    return args


def kwargs2dict(**kwargs):
    return kwargs

class fnexcept:

    """
        Wrapping a raising function to return the exception
        as the second item in a tuple.

        Examples
        --------
            >>> def raising(a: int):
            ...     if a > 2:
            ...         raise Exception("not allowed")
            ...     return a+1
            >>> raising_wrapper = fnexcept(raising, lambda: 0)
            >>> raising_wrapper(3)
            0

            >>> def raising(a: int):
            ...     if a > 2:
            ...         raise Exception("not allowed")
            ...     return a+1
            >>> raising_wrapper = fnexcept(raising, lambda: 0)
            >>> raising_wrapper(2)
            2

        Returns
        -------
            out : Callable
    """

    def __init__(self, raising_function, handler_function):
        self.raising_function = raising_function
        self.handler_function = handler_function

    def __call__(self, *args, **kwargs) -> typing.Any:
        try:
            return self.raising_function(
                *args,
                **kwargs
            )
        except Exception as e:
            return self.handler_function(*args, **kwargs)


class filter_map_concat:

    """

        Takes three functions as input and returns a filter, map and concat function composition.
        First the first predicate function is applied to all elements where for the one elements yielding
        true will then propagate on to the second function. The one elements yielding false will propagate to 
        the second function. At the end, all elements are concatenated into a new iterator where order is kept.

              output
                |
                |
        concat  x ----o  (order is kept)
                |     |
                |     |
         map T  x     x  map F
                |     |
                |     |
        filter  o --- o
                |
                |  
              input

        Parameters
        ----------
            filter_predicate : Callable[[Any], bool]
                A predicate function taking `Any` object as input and outputs a bool

            tmap_function : Callable[[Any], Any]
                A function mapping the one object's that yielded TRUE from filter_predicate to another object. As default there's a dummy function that just returns the same object.

            fmap_function : Callable[[Any], Any]
                A function mapping the one object's that yielded FALSE from filter_predicate to another object. As default there's a dummy function that just returns the same object.

        Returns
        -------
            out : Callable[[Iterator[Any]], Iterator[Any]]

    """

    def __init__(
        self, 
        filter_predicate: typing.Callable[[typing.Any], bool],
        tmap_function: typing.Callable[[typing.Any], typing.Any] = lambda x: x,
        fmap_function: typing.Callable[[typing.Any], typing.Any] = lambda x: x,
    ):
        self.filter_predicate = filter_predicate
        self.tmap_function = tmap_function
        self.fmap_function = fmap_function

    def __call__(self, objects: typing.Iterable[typing.Any]) -> typing.Iterable[typing.Any]:
        return map(
            operator.itemgetter(1),
            sorted(
                itertools.chain(
                    map(
                        lambda x: (x[0], self.tmap_function(x[1])),
                        filter(
                            compose(
                                self.filter_predicate,
                                operator.itemgetter(1),
                            ),
                            enumerate(objects)
                        ),
                    ),
                    
                    map(
                        lambda x: (x[0], self.fmap_function(x[1])),
                        filter(
                            compose(
                                operator.not_,
                                self.filter_predicate,
                                operator.itemgetter(1),
                            ),
                            enumerate(objects)
                        ),
                    )
                ),
                key=operator.itemgetter(0),
            )
        )