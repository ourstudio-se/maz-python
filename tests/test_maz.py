import maz
import operator

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