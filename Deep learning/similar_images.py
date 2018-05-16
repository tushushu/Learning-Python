# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 15:19:12 2018

@author: Administrator
"""
import numpy as np
from PIL import Image
import re

pattern = re.compile("^.+\.(png|jpg|jpeg|bmp|gif)$")


def is_image(filename):    
    return filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))

# 没有endswith方法快
def is_image_re(filename, pattern):
    return re.fullmatch(pattern, filename)

# 没有.convert("L")方法快
def convert_L(mat):
    return mat[:,:,0] * 299 / 1000 + mat[:,:,1] * 587 / 1000 + mat[:,:,2] * 114 / 1000

def get_diff(image, hash_size=8):
	if hash_size < 2:
		raise ValueError("Hash size must be greater than or equal to 2")
	pixels = np.asarray(image.resize((hash_size+1, hash_size)).convert("L"))
	# 第1~n列与第0~n-1列进行比较
	diff = pixels[:, 1:] > pixels[:, :-1]
	return diff

# 网上的原始代码，191 µs
def d_hash1(diff, hash_size=8):
    decimal_value = 0
    hash_string = ""
    k = hash_size - 1
    for index, value in enumerate(diff.flatten()):    
        if value:  # value为0, 不用计算, 程序优化        
            decimal_value += value * (2 ** (index % hash_size))   
        if index % hash_size == k:  # 每8位的结束        
            hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))  # 不足2位以0填充。0xf=>0x0f        
            decimal_value = 0
    return hash_string

# 第一版优化，190 µs
def d_hash2(diff):
    hash_string = ""
    for row in diff:
        decimal_value = 0
        for index, value in enumerate(row):
            # 为了节约时间，value为False不用计算
            if value:    
                decimal_value += value * (2 ** index)
        # 不足2位以0填充，0xf=>0x0f 
        hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))       
    return hash_string

# 第二版优化，93.2 µs
def d_hash3(diff):
    hash_string = ""
    for row in diff:
        decimal_value = (2 ** np.where(row)[0]).sum()
        # 不足2位以0填充，0xf=>0x0f 
        hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))       
    return hash_string

# 第三版优化，90 µs
def d_hash4(diff):
    hash_string = ''
    for row in diff:
        decimal_value = (2 ** np.where(row)[0]).sum()
        # 不足2位以0填充，0xf=>0x0f 
        hash_string += hex(decimal_value)[2:].rjust(2, "0")
    return hash_string

# 16进制最大长度与hash_size的关系
def max_hex_len(hash_size):
    row = np.array([True] * hash_size)
    return len(hex((2 ** np.where(row)[0]).sum())) - 2

# 正式版
def d_hash(image, hash_size=8):
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")
    if hash_size % 8:
        raise ValueError("Hash size must be a multiple of 8")
    max_hex_len = hash_size // 4
    pixels = np.asarray(image.resize((hash_size+1, hash_size)).convert("L"))
    # 第1~n列与第0~n-1列进行比较
    diff = pixels[:, 1:] > pixels[:, :-1]
    # 计算哈希值
    hash_string = ''
    for row in diff:
        decimal_value = (2 ** np.where(row)[0]).sum()
        # 不足2位以0填充，0xf=>0x0f 
        hash_string += hex(decimal_value)[max_hex_len:].rjust(max_hex_len, "0")
    return hash_string

# 计算汉明距离
def get_hamming_distance(d_hash1, d_hash2):
    difference = (int(d_hash1, 16)) ^ (int(d_hash2, 16))
    return bin(difference).count("1")

# 计算图像差异
def get_similarity(diff1, diff2):
    return np.mean(diff1 == diff2)

image = Image.open(r"C:\Users\Public\Pictures\Sample Pictures\shamo.jpg")
image1 = Image.open(r"C:\Users\Public\Pictures\Sample Pictures\shamo1.jpg")
image2 = Image.open(r"C:\Users\Public\Pictures\Sample Pictures\flower.jpg")

print(get_diff(image))
print(get_diff(image1))

hash_string = d_hash(image, hash_size=32)
hash_string1 = d_hash(image1, hash_size=32)
hash_string2 = d_hash(image2, hash_size=32)

print(get_hamming_distance(hash_string, hash_string1))
print(get_hamming_distance(hash_string, hash_string2))

diff = get_diff(image, hash_size=8)
diff1 = get_diff(image1, hash_size=8)
diff2 = get_diff(image2, hash_size=8)
print(get_similarity(diff, diff1))
print(get_similarity(diff, diff2))

pixles = np.asarray(image.resize(image1.size).convert("L"))
pixles1 = np.asarray(image1.convert("L"))
diff = pixles[:, 1:] > pixles[:, :-1]
diff1 = pixles1[:, 1:] > pixles1[:, :-1]
np.mean(diff == diff1)
a = pixles[0]
b = pixles1[0]
c = a[:-1] > a[1:]
d = b[:-1] > b[1:]


"""
改进版
"""
image = Image.open(r"C:\Users\Public\Pictures\Sample Pictures\shamo.jpg")
image1 = Image.open(r"C:\Users\Public\Pictures\Sample Pictures\shamo1.jpg")
hash_size = 8
pixels = np.asarray(image.resize((hash_size+1, hash_size)))
pixels.shape
(pixels[:, 1:] > pixels[:, :-1]).shape
diff = pixels[:, 1:] > pixels[:, :-1]

pixels1 = np.asarray(image1.resize((hash_size+1, hash_size)))
diff1 = pixels1[:, 1:] > pixels1[:, :-1]
