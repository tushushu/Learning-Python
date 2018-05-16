# -*- coding: utf-8 -*-
"""
@Author: liutienan 
@Date: 2018-05-11 14:45:53 
@Last Modified by: liutienan 
@Last Modified time: 2018-05-11 14:45:53 
"""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from numpy.random import randint
from time import time


def find(sub_str, target_str):
    """[summary]

    Arguments:
        sub_str {str} -- substring
        target_str {str} -- target string

    Returns:
        bool -- if substring is found in target string
    """

    return sub_str in target_str


def rand_str(size):
    """[summary]

    Arguments:
        size {int} -- size of string

    Returns:
        str -- string with random characters of A-Z
    """

    return ''.join(map(chr, randint(low=65, high=90, size=size)))


def serial_func(sub_strs, target_str):
    """[summary]

    Arguments:
        sub_strs {list} -- a list of substrings
        target_str {str} -- target string

    Returns:
        str -- a sub string found in target string
    """

    for sub_str in sub_strs:
        if find(sub_str, target_str):
            return sub_str


def parallel_func(sub_str, target_str, executor):
    """[summary]

    Arguments:
        sub_strs {list} -- a list of substrings
        target_str {str} -- target string
        executor {Executor} -- existance of ProcessPoolExecutor, ThreadPoolExecutor

    Returns:
        str -- a sub string found in target string
    """

    return executor.submit(serial_func, sub_str, target_str)


def func_runtime(func, n_iter, *args):
    """[summary]

    Arguments:
        func {function object} -- the function to test
        n_iter {int} -- number of iterations

    Returns:
        str -- test result
    """

    start = time()
    for _ in range(n_iter):
        func(*args)
    runtime = (time() - start) / n_iter
    return "Average %.5fs in %d loops" % (runtime, n_iter)


if __name__ == "__main__":
    # generate target string and substring list
    target_str = rand_str(1000)
    n = 1200
    sub_strs = [rand_str(10) for _ in range(n)]
    # get executor existance
    multi_process = ProcessPoolExecutor()
    multi_thread = ThreadPoolExecutor()
    # how many times to execute test functions
    n_iter = 10000

    # print test results
    print(func_runtime(serial_func, n_iter, sub_strs, target_str))
    print(func_runtime(parallel_func, n_iter, sub_strs, target_str, multi_process))
    print(func_runtime(parallel_func, n_iter, sub_strs, target_str, multi_thread))
