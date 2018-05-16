import io
import sys
from time import time
from concurrent.futures import ProcessPoolExecutor


def get_words(path):
    """[summary]

    Arguments:
        path {str} -- filepath/filname

    Returns:
        list -- e.g. ["微信", "微星"]
    """
    f = open(path, encoding="utf-8")
    return f.read().split(",")


def get_clean_words(words):
    """[summary]
    If word b includes word a, then delete word b
    Arguments:
        words {list} -- e.g. ["你好", "再见", "你好啊"]

    Returns:
        list -- ["你好", "再见"]
    """
    words.sort(key=len)
    res = []
    tmp = []
    while words:
        target = words.pop(0)
        res.append(target)
        while words:
            word = words.pop(0)
            if target not in word:
                tmp.append(word)
        tmp, words = words, tmp
    return res


def get_dict(words):
    """[summary]

    Arguments:
        words {list} -- e.g. ["微信", "微星", "成人片", "成人论坛"]

    Returns:
        dict -- e.g. {'微': {'信', '星'}, '成': {'人'{'片': {}, '论':{'坛'}}}}
    """
    dic = {}
    for word in words:
        current_dic = dic
        for c in word:
            if not current_dic.get(c):
                current_dic[c] = {}
            current_dic = current_dic[c]
    return dic


def find_word(target, dic):
    """[summary]

    Arguments:
        target {str} -- user message
        dic {dict} -- e.g. {'微': {'信', '星'}, '成': {'人'{'片': {}, '论':{'坛'}}}}

    Returns:
        bool -- if target is found in dic
    """
    n = len(target)
    for i in range(n):
        j = 0
        sub_dic = dic
        while i + j < n:
            c = target[i+j]
            if sub_dic.get(c) is None:
                break
            else:
                sub_dic = sub_dic[c]
                if sub_dic == {}:
                    return True
                else:
                    j += 1
    return False


def parallel_find_word(target, dic, executor):
    """[summary]

    Arguments:
        target {str} -- user message
        dic {dict} -- e.g. {'微': {'信', '星'}, '成': {'人'{'片': {}, '论':{'坛'}}}}
        executor {Executor} -- existance of ProcessPoolExecutor, ThreadPoolExecutor

    Returns:
        str -- a sub string found in target string
    """
    return executor.submit(find_word, target, dic).result()


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


def test():
    # test get_words
    print("test get_words")
    words = get_words(path)
    print(words)

    # test get_dic
    print("test get_dic")
    words = ['迷幻药', '迷幻藥', '迷昏口', '迷昏药', '迷昏藥', '迷魂香', '迷魂药',
             '迷魂藥', '迷奸粉', '迷奸药', '迷情粉', '迷情水', '迷情药', '迷药', '迷藥', '谜奸药']
    dic = get_dict(words)
    print(dic)

    # test find_word
    print("test find_word")
    print(find_word("迷幻", dic))
    print(find_word("微信", dic))
    print(find_word("迷幻药", dic))
    print(find_word("我要送你迷幻药，好吗？", dic))

    # test parallel_find_word
    print("test parallel_find_word")
    multi_process = ProcessPoolExecutor()
    n_iter = 1000
    target = """捐赠仪式后，同行的体彩志愿者与孩子们开展了欢乐的游戏互动，
                陈旧的场地、简陋的条件，没有阻挡大家参与游戏的热情，孩子们个个玩的十分投入、
                我要送你迷幻药，好吗？
                兴趣十足，掌声、笑声、欢呼声荡漾在整个大院里。"""
    print(parallel_find_word(target, dic, multi_process))
    print(func_runtime(parallel_find_word, n_iter, target, dic, multi_process))

    # test get_clean_words(words)
    print("test get_clean_words")
    words = ["你好", "再见", "你好啊"]
    print(get_clean_words(words))


if __name__ == "__main__":
    # Set the encoding of stdout as uft8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    path = "D:/Soyoung/training/Other/words.txt"
    test()
