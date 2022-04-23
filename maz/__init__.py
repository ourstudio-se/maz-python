import functools

# functional composition functions
def sorted_pos(iterable, key=None) -> iter:

    """
        Since python's "sorted" does not support positional
        argument and one requirement is that a pure function should
        always allow positional arguments, then here's a forwarding
        function.

        Return:
            iterable
    """

    return sorted(iterable, key=key)

def cached_execution(cache: dict, key: str, function: callable, *args, **kwargs) -> tuple:
    
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

def starzip(iterable: list):

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

        Return:
            callable
    """

    def wrapper(*args, fn=function, pas=positional_arguments, **kwargs):
        nargs = list(args)
        for i, pa in pas:
            nargs.insert(i, pa)
        return fn(*nargs, **kwargs)
    return wrapper

def compose_pair(f, g):

    """
        Composes new function h = f(g(x)), from
        f and g.

        Example:
            >>> inc = lambda x: x+1
            >>> double = lambda x: x*2
            >>> h = compose_pair(double, inc)
            >>> h(1)
            >>> 4

        Return:
            Callable
    """
    def composed(*args, f=f, g=g, **kwargs):
        return f(g(*args, **kwargs))

    return composed

def compose(*functions):

    """
        Sequence composite functions of `functions`.
        E.g. let fns be a list of functions [f, g, h] and
        compose(fns) would then represent lambda x : f(g(h(x)))

        Example:
            >>> inc = lambda x: x+1
            >>> double = lambda x: x*2
            >>> f = compose(inc, double, inc)
            >>> f(2)
            >>> 7

        Return:
            function
    """

    return functools.reduce(compose_pair, functions)

def indexing(lst: list, index_item, default = None):

    """
        Indexing function, taking a list and what to
        index, as such lst[index_item]. If index_item
        not in lst, then default is returned.
    """

    try:
        return lst[index_item]
    except:
        return default

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