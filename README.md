# MAZ
*A functional programming package.*

### Install
```
pip install maz
```

### Main usage
##### Function composition
You can use `maz` to compose function calls such that they call one another in a series. 
**NOTE:** functions are called from right to left.
```python
>>> import maz
>>> inc = lambda x: x+1
>>> add_three = maz.compose(inc,inc,inc)
>>> add_three(4)
>>> 7
```

##### Partial function
When you want to fix a parameter in a function, you could just use the `functools.partial`. However, that doesn't support fixing a positional argument on a specific index, which are quite common later on when you want to build complex compositions. Here you can use the `maz.pospartial` instead
```python
>>> import maz
>>> def add(x,y): return x+y
>>> add_two = maz.pospartial(add, [(1,2)]) # meaning fix argument on index 1 with the value 2
>>> add_two(3)
>>> 5
```

### Other functionalities
To support more complex compositions we've added some special functions such as
```python
import maz
import operator

# "indexing" function - since only way to index a list in python is to do lst[x]
lst = [2,1,3]
maz.indexing(lst, 0) # >>> 2

# "invoke" function - a function calling other functions
def add(x,y): 
    return x+y

maz.invoke(add, [1,2]) # >>> 3
maz.invoke_star(add, 1, 2) # >>> 3

# "fnmap" function will compute all input functions in a 
# series with same given arguments 
fn = maz.fnmap(add, add, add)
fn(1,2) # >>> [3, 3, 3]

# "ifttt" returns a new function that checks the input somehow
# then does something depending on the result from the check
fn = maz.ifttt(
    # if x is greater than 3,
    lambda x: x > 3,
    # then subtract 1 from x
    lambda x: x - 1,
    # else add 1 to x
    lambda x: x + 1
)
fn(3) # >>> 4
fn(4) # >>> 3

```
