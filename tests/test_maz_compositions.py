import time
from functools import partial
from maz.compositions import retry_until, waiting

def test_retryer():

    retryer = retry_until(
        function=partial(
            next, 
            iter([0,0,1,2,3])
        ),
        retries=3,
        condition=lambda j: j == 1,
    )

    assert retryer() == 1

    retryer = retry_until(
        function=partial(
            next, 
            iter([0,0,1,2,3])
        ),
        retries=2,
        condition=lambda j: j == 1,
    )

    assert retryer() == 0

def test_timeout():

    waiting_fn = waiting(
        lambda x: x+1,
        1.1,
    )

    start_time = time.time()
    assert waiting_fn(3) == 4
    total_time = time.time()-start_time
    assert total_time > 1