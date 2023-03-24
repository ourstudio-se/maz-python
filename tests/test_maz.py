import functools
import maz
import operator
import pytest


def test_compose():
    def inc(x): return x + 1
    add_three = maz.compose(inc, inc, inc)
    assert add_three(4) == 7

    part_mul = functools.partial(operator.mul, 3)
    part_div = functools.partial(
        operator.truediv,
        2
    )
    composed = maz.compose(part_div, part_mul, operator.add)

    expected = 1/6
    actual = composed(2, 2)
    assert actual == expected


def test_pospartial():
  
    def add(x, y): 
        return x + y
   
    add_two = maz.pospartial(add, [(1, 2)])
    assert add_two(3) == 5
   
    def f(x, y, z):
        return x + y + z

    _f = maz.pospartial(f, [(1, 32), (2, 19)])
    assert _f(23) == 74


def test_invoke():
    def add(x, y):
        return x + y
    assert maz.invoke(add, [1, 2]) == 3


def test_invoke_star():
    def add(x, y):
        return x + y
    assert maz.invoke_star(add, 1, 2) == 3


def test_sorted_pos():
    lst = [[2, 1], [1, 0], [3, 0]]
    maz.sorted_pos(lst, operator.itemgetter(0)) == [[1, 0], [2, 1], [3, 0]]


def test_compose_pair():

    def f(a, b):
        return a+b

    def g(x):
        return x*3

    a, b, x = 1, 2, 3
    expected = (a+b)*x
    composed = maz.compose_pair(g, f)
    actual = composed(a, b)
    assert actual == expected


def test_fnmap():

    fn = maz.fnmap(lambda x: x + 1, lambda x: x + 2)
    assert list(fn(3)) == [4, 5]

    def add_one(x): return x + 1
    def mul_two(x): return x * 2
    fn = maz.fnmap(add_one, mul_two)
    assert list(fn(x=3)) == [4, 6]


def test_fnexcept():

    def raising(a: int):
        if a > 2:
            raise Exception("not allowed")
        return a+1

    raising_wrapper = maz.fnexcept(raising, lambda _: 0)
    assert raising_wrapper(3) == 0
    assert raising_wrapper(2) == 3


def test_filter_concat():

    class Var:
        def __init__(self, id: str, n: int):
            self.id = id
            self.n = n
        
        def __eq__(self, o):
            return (self.id == o.id) and (self.n == o.n)

    items = iter([
        Var("a", 1),
        Var("b", 2),
        Var("c", 3),
        Var("d", 4),
        Var("e", 5),
    ])

    fmc_fn = maz.filter_map_concat(
        lambda x: x.n > 2,
        lambda x: Var(x.id, x.n+1),
        lambda x: Var(x.id, x.n-1)
    )
    actual = list(fmc_fn(items))
    expected = [
        Var("a", 0),
        Var("b", 1),
        Var("c", 4),
        Var("d", 5),
        Var("e", 6),
    ]
    assert actual == expected

def test_ifttt_function():

    class Var:
        def __init__(self, id: str, n: int):
            self.id = id
            self.n = n
        
        def __eq__(self, o):
            return (self.id == o.id) and (self.n == o.n)

    items = [
        Var("a", 1),
        Var("b", 2),
        Var("c", 3),
        Var("d", 4),
        Var("e", 5),
    ]

    actual = list(
        map(
            maz.ifttt(
                lambda x: x.n > 2,
                lambda x: Var(x.id, x.n+1),
                lambda x: Var(x.id, x.n-1)
            ),
            items
        )
    )
    expected = [
        Var("a", 0),
        Var("b", 1),
        Var("c", 4),
        Var("d", 5),
        Var("e", 6),
    ]
    assert actual == expected

def test_partialpos():

    def f(a,b,c,d=1):
        return 1*a + 2*b + 3*c + 4*d

    assert maz.partialpos(f, {1:2, 2:2})(1,2) == 1*1 + 2*2 + 3*2 + 4*2
    assert maz.partialpos(f, {1:2, 2:2})(1)   == 1*1 + 2*2 + 3*2 + 4*1
    assert maz.partialpos(f, {1:2, 3:3})(1,3) == 1*1 + 2*2 + 3*3 + 4*3

    def f(a,b):
        return a+b

    assert maz.partialpos(f, {1: 2})(1) == 3
    assert maz.partialpos(f, {1: 2})(1,2) == 3

    with pytest.raises(Exception):
        assert maz.partialpos(f, {"1":2})(1)

    with pytest.raises(Exception):
        assert maz.partialpos(f, {1:2})()

def test_starfilter():

    assert list(
        maz.starfilter(
            lambda x,y: x+y >= 4,
            [(1,2),(2,3),(3,4),(4,5)]
        )
    ) == [(2,3),(3,4),(4,5)]

def test_constant():

    cnst_fn = maz.constant(True)
    assert cnst_fn(0) == True
    assert cnst_fn("hello") == True
    assert cnst_fn(lambda x: x+1) == True
