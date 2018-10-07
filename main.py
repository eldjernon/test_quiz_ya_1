from typing import Dict, Iterable
from itertools import chain
from collections import defaultdict

import multiprocessing as mp


def agg(*args: Iterable[Dict]):
    aggregate_state = defaultdict(int)
    for row in chain(*args):
        key, value = row.popitem()
        aggregate_state[key] += value
    return aggregate_state


def agg_mp(*args: Iterable[Dict], result, lock):

    def _agg_mp():
        aggregate_state = defaultdict(int)
        for row in chain(*args):
            key, value = row.popitem()
            aggregate_state[key] += value

        lock.acquire()
        result.update(aggregate_state)
        lock.release()

    return _agg_mp


def agg_multiprocess(*gens: Iterable[Dict]):
    manager = mp.Manager()
    result = manager.dict()
    lock = manager.Lock()
    processes = []

    for gen in gens:
        processes.append(mp.Process(target=agg_mp(gen, result=result, lock=lock)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    return {**result}
