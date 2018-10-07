from typing import AnyStr
import pytest
from main import agg, agg_multiprocess


def gen(key: AnyStr, length: int = 10):
    for i in range(length):
        yield {key: 1 if i % 2 else -1}


@pytest.fixture(params=[10**2, 10**3, 10**6], ids=["10^2", "10^3", "10^6"])
def get_gens(request):
    pow_ = request.param
    src_a = gen("key_a", pow_)
    src_b = gen("key_b", pow_)
    src_c = gen("key_c", pow_)
    return src_a, src_b, src_c


answer = {'key_a': 0, 'key_b': 0, 'key_c': 0}


def test_singleprocess(get_gens):
    assert agg(*get_gens) == answer, "Bad result"


def test_multiprocess(get_gens):
    assert agg_multiprocess(*get_gens) == answer, "Bad result"
