from typing import Dict, Iterable, Any, FrozenSet
from itertools import starmap, groupby, repeat, chain

def reverse_otm_dict(data: Dict[Any, Iterable[Any]]) -> Dict[Any, FrozenSet[Any]]:

    """
        Reverses a dictionary with one-to-many relationship.
        Example:
            {
                "a": [1,2,3],
                "b": [2,3,4],
                "c": [3,4,5],
            }
            =>
            {
                1: frozenset({"a"}),
                2: frozenset({"a", "b"}),
                3: frozenset({"a", "b", "c"}),
                4: frozenset({"b", "c"}),
                5: frozenset({"c"}),
            }

        Args:
            data: Dictionary with one-to-many relationship.
        
        Returns:
            Reversed dictionary with one-to-may relationship.
    """
    return dict(
        starmap(
            lambda k, v: (
                k, 
                set(
                    map(
                        lambda x: x[1],
                        v
                    )
                )
            ),
            groupby(
                sorted(
                    chain(
                        *starmap(
                            lambda k, vs: list(zip(
                                vs,
                                repeat(k),
                            )),
                            data.items(),
                        )
                    ),
                ),
                key=lambda x: x[0],
            )
        )
    )
