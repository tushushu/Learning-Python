# -*- coding: utf-8 -*-
"""
@Author: liutienan
@Date: 2018-06-08 10:18:22
@Last Modified by: liutienan
@Last Modified time: 2018-06-08 10:18:22
"""
"""
如何安装Pypy?
1. 用Anaconda创建pypy环境 conda create -n pypy python=3.5
2. 下载安装文件 wget https://bitbucket.org/pypy/pypy/downloads/pypy3-v6.0.0-linux64.tar.bz2
3. 解压文件 tar -xf pypy3-v6.0.0-linux64.tar.bz2
4. 将文件夹拷贝在~/anaconda3/envs/pypy/文件中把目录拷贝进去，如果目录名相同则合并目录。
5. 激活pyppy环境 source activate pypy
注：mac、windows下的pypy安装方法类似，注意win32位的pypy可以在64位的win7上运行。
"""
from time import time
from math import ceil
from random import randint
from pyspark.sql.functions import col, rand
from pyspark.sql.types import IntegerType
from pyspark.sql.session import SparkSession


def fib(n):
    """[summary]
    Calculate Nth Fibonacci sequence value
    Arguments:
        n {int}

    Returns:
        int
    """
    if n == 0 or n == 1:
        return n
    que = [0, 1]
    while n > 1:
        que.append(que.pop(0) + que[0])
        n -= 1
    return que[1]


def merge_sort(arr):
    n = len(arr)
    que = []
    item_len = 1
    while item_len < n:
        pair_len = item_len * 2
        n_pair = ceil(n / pair_len)
        # divide problem to sub-problem, iterate each pair
        for k in range(n_pair):
            low = i = k * pair_len
            # check array length
            if k == n_pair - 1:
                mid = j = min(low + item_len, n)
                high = n
            else:
                mid = j = low + item_len
                high = low + pair_len
            # merge: append smaller element
            while i < mid and j < high:
                if arr[i] < arr[j]:
                    que.append(arr[i])
                    i += 1
                else:
                    que.append(arr[j])
                    j += 1
            # if one item is empty, append all the elements of the other
            que.extend(arr[j:high] if i == mid else arr[i:mid])
        # swap
        que, arr = [], que
        # increase sub-problem length
        item_len *= 2
    return arr


def group_sum_max(df):
    return df.groupby("id").agg({"val": "sum"}).agg({""})


def unit_test(fn, X, Y, n_iter=100000):
    """[summary]
    Correctness and performance testing
    Arguments:
        fn {function} -- function to test
        X {iterable} -- a series of input
        Y {iterable} -- expected results

    Keyword Arguments:
        n_iter {int} -- number of iterations (default: {100000})
    """

    print("Test %s:" % fn.__name__)
    # Correctness
    assert all(y0 == y for y0, y in zip(map(fn, X), Y)), "Test not passed!"
    print("Test passed!")
    # Performance
    start = time()
    for _ in range(n_iter):
        for x in X:
            fn(x)
    print("Time elapsed %.3f\n" % (time()-start))


if __name__ == "__main__":
    # # Test fib
    # X = range(1, 11)
    # Y = [1, 1, 2, 3, 5, 8, 13, 21, 34]
    # unit_test(fib, X, Y)

    # # Test merge-sort
    # X = []
    # Y = []
    # for _ in range(1000):
    #     L = randint(0, 1000)
    #     row = [randint(0, 20) for _ in range(L)]
    #     X.append(row)
    #     Y.append(sorted(row))
    # unit_test(merge_sort, X, Y, n_iter=1)

    # Test spark
    spark = SparkSession.builder.appName("test_pypy").getOrCreate()
    df = spark.range(0, 10**4).withColumn('id', (col('id') /
                                                 10**3).cast('integer')).withColumn('val', rand())
    df.cache()
    df.show()
    res = group_sum_max(df)
    res.show()
