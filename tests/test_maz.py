import maz
import operator
import functools

def test_compose():
    inc = lambda x: x+1
    add_three = maz.compose(inc,inc,inc)
    assert add_three(4) == 7

def test_pospartial():
    def add(x,y): return x+y
    add_two = maz.pospartial(add, [(1,2)])
    assert add_two(3) == 5

def test_indexing():
    lst = [2,1,3]
    assert maz.indexing(lst,0) == 2

def test_invoke():
    def add(x,y):
        return x+y
    assert maz.invoke(add, [1,2]) == 3

def test_invoke_star():
    def add(x,y):
        return x+y
    assert maz.invoke_star(add, 1, 2) == 3

def test_sorted_pos():
    lst = [[2,1], [1,0], [3,0]]
    maz.sorted_pos(lst, operator.itemgetter(0)) == [[1,0], [2,1], [3,0]]

def test_compose_pair():

    def f(a, b):
        return a+b

    def g(x):
        return x*3

    a,b,x = 1,2,3
    expected = (a+b)*x
    composed = maz.compose_pair(g, f)
    actual = composed(a,b)
    assert actual == expected

def test_compose():

    part_mul = functools.partial(operator.mul, 3)
    part_div = functools.partial(
        operator.truediv,
        2
    )
    composed = maz.compose(part_div, part_mul, operator.add)

    expected = 1/6
    actual = composed(2,2)
    assert actual == expected

def test_pospartial():

    def f(x,y,z):
        return x+y+z

    _f = maz.pospartial(f, [(1, 32), (2, 19)])
    assert _f(23) == 74

def test_fnmap():

    fn = maz.fnmap(lambda x: x+1, lambda x: x+2)
    assert list(fn(3)) == [4, 5]

    def add_one(x): return x+1
    def mul_two(x): return x*2
    fn = maz.fnmap(add_one, mul_two)
    assert list(fn(x=3)) == [4, 6]