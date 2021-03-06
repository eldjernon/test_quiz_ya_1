from typing import Dict, Iterable
from itertools import chain
from collections import defaultdict

import multiprocessing as mp


def agg(*args: Iterable[Dict]) -> Dict:
    """
    Аггрегируем сумму значений по ключам
    :param args:
    :return: dict, ключ: агрерированная сумма
    """
    aggregate_state = defaultdict(int)
    for row in chain(*args):
        for key, value in row.items():
            aggregate_state[key] += value
    return aggregate_state


def agg_mp(*args: Iterable[Dict], result, lock):
    """
    Обертка над аггрерирующей функцией для форка
    :param args:
    :param result: список в shared memory
    :param lock: блокировка
    :return: target функцию
    """
    def _agg_mp():
        aggregate_state = defaultdict(int)
        for row in chain(*args):
            for key, value in row.items():
                aggregate_state[key] += value

        lock.acquire()
        result.append(aggregate_state)
        lock.release()

    return _agg_mp


def agg_multiprocess(*gens: Iterable[Dict]):
    """
    Аггрегируем сумму значений по ключам, вычисления проводим в отдельных процессах
    :param gens:
    :return: dict, ключ: агрерированная сумма
    """
    manager = mp.Manager()
    result = manager.list()
    lock = manager.Lock()
    processes = []

    for gen in gens:
        processes.append(mp.Process(target=agg_mp(gen, result=result, lock=lock)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
        
    return agg(result)

