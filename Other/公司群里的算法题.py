# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 12:50:52 2018

@author: tushushu
"""

"""
命题：数组s包含重复元素，数组t包含重复元素，且比s多出一个元素x，求x
举例：s = [1, 7, 8, 8, 8, 8, 3], t = [1, 7, 8, 8, 8, 8, 8, 3]
解法：二分查找满足s[i] != t[i]的i的最小值，找不到则返回最后一个元素。
满足s[i] == t[i]时，需要考虑重复元素的情况
"""
import random, copy

# 二分法
def fun(s, t):
    low = 0
    high = len(s) - 1
    while low <= high:
        k = mid = (low + high) // 2
        print(low, mid, high)
        if s[mid] != t[mid]:
            high = mid - 1
        # 解决重复元素问题
        else:
            while k > low and s[k] == s[k-1] == t[k]:
                k -= 1
                print(k)
                if s[k] != t[k]:
                    break
            if s[k] != t[k]:
                high = mid - 1
            else:
                low = mid + 1
    return t[low]

# 线性查找
def fun1(s, t):
    n = len(s)
    for i in range(n):
        if s[i] != t[i]:
            return t[i]
    return t[n]


"""
随机生成长度为10000的包含重复元素的数组，插入一个随机数
二分查找的效率是线性查找的10倍左右
"""
def test():
    s = [random.randint(1, 100) for _ in range(10**5)]
    t = copy.copy(s)
    t.insert(random.randint(1, 10**5-1), random.randint(0, 100))
    return s, t

# 176 µs ± 420 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
%timeit fun(*test())
# 10 ms ± 256 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit fun1(*test())

"""
测试用例
"""
# 测试0
s = [1]
t = [1, 2]
print(fun(s, t) == fun1(s, t))

# 测试1
s = [1]
t = [2, 1]
print(fun(s, t) == fun1(s, t))

# 测试2
s = []
t = [2]
print(fun(s, t) == fun1(s, t))

# 测试3
s = [1, 3]
t = [2, 1, 3]
print(fun(s, t) == fun1(s, t))

# 测试4
s = [1, 3]
t = [1, 2, 3]
print(fun(s, t) == fun1(s, t))

# 测试5
s = [1, 3]
t = [1, 3, 2]
print(fun(s, t) == fun1(s, t))

# 测试6
s = [1, 7, 8, 3]
t = [9, 1, 7, 8, 3]
print(fun(s, t) == fun1(s, t))

# 测试7
s = [1, 7, 8, 3]
t = [1, 9, 7, 8, 3]
print(fun(s, t) == fun1(s, t))

# 测试8
s = [1, 7, 8, 3]
t = [1, 7, 9, 8, 3]
print(fun(s, t) == fun1(s, t))

# 测试9
s = [1, 7, 8, 3]
t = [1, 7, 8, 9, 3]
print(fun(s, t) == fun1(s, t))

# 测试10
s = [1, 7, 8, 3]
t = [1, 7, 8, 3, 9]
print(fun(s, t) == fun1(s, t))

# 测试11
s = [1, 7, 8, 8, 8, 8, 3]
t = [1, 7, 8, 8, 8, 8, 8, 3]
print(fun(s, t) == fun1(s, t))

# 测试12
s = [3, 3, 4, 4, 4]
t = [3, 3, 4, 4, 4, 4]
print(fun(s, t) == fun1(s, t))

# 测试13
s = [3, 3, 4, 4, 4]
t = [3, 3, 3, 4, 4, 4]
print(fun(s, t) == fun1(s, t))

# 测试14
s = [3, 3, 4, 4, 4, 5, 5, 3, 3, 3]
t = [3, 3, 4, 4, 6, 4, 5, 5, 3, 3, 3]
print(fun(s, t) == fun1(s, t))

# 测试15
s = [3, 3, 4, 4, 4, 5, 5, 3, 3, 3]
t = [3, 3, 4, 4, 4, 5, 6, 5, 3, 3, 3]
print(fun(s, t) == fun1(s, t))

# 测试16
s = [3, 3, 4, 4, 4, 5, 5, 3, 3, 3]
t = [6, 3, 3, 4, 4, 4, 5, 5, 3, 3, 3]
print(fun(s, t) == fun1(s, t))

# 测试17
s = []
t = [1]
print(fun(s, t) == fun1(s, t))

# 测试17
s = [1, 1, 1, 2, 3]
t = [1, 4, 1, 1, 2, 3]
print(fun(s, t) == fun1(s, t))

