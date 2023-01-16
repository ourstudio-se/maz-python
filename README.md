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
When you want to fix a parameter in a function, you could just use the `functools.partial`. However, that doesn't support fixing a positional argument on a specific index, which are quite common later on when you want to build complex compositions. Here you can use the `maz.partialpos` instead
```python
>>> import maz
>>> def add(x,y): return x+y
>>> add_two = maz.partialpos(add, {1:2}) # fixing argument for index 1 to 2 (y=2)
>>> add_two(3)
>>> 5
```

### Other functionalities
To support more complex compositions we've added some special functions such as
```python
import maz
import operator
import itertools

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

# "starfilter" just as itertools.starmap but a filter instead
# Example, filter tuples who's sum is greater than 4 
next(
    maz.starfilter(
        maz.compose(
            lambda i: i > 4,
            add
        ), 
        itertools.product(range(3), range(3,6))
    )
) # >>> (0,5)

# "constant" returns a function which, no matter the argument, returns a constant value.
cnst_fn = maz.constant(True)
cnst_fn() # >>> True
cnst_fn(cnst_fn()) # >>> True

```
