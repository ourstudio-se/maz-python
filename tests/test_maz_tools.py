from maz.tools import reverse_otm_dict

def test_reverse_otm_dict():
    d = {
        "a": [1,2,3],
        "b": [2,3,4],
        "c": [3,4,5],
    }
    actual = reverse_otm_dict(d)
    expected = {
        1: frozenset({"a"}),
        2: frozenset({"a", "b"}),
        3: frozenset({"a", "b", "c"}),
        4: frozenset({"b", "c"}),
        5: frozenset({"c"}),
    }
    assert actual == expected