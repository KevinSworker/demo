# -*- coding: utf-8 -*-

import hashlib
import os
import time

def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    if os.path.isfile(file_name):
        # 文件是存在的
        while True:
            if file_is_openState(file_name):
                return general_md5(file_name)
            else:
                time.sleep(0.2)

def general_md5(file_name):
    m = hashlib.md5()   #创建md5对象
    with open(file_name, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()

def get_str_md5(content):
    """
    计算字符串md5
    :param content:
    :return:
    """
    m = hashlib.md5(content) #创建md5对象
    return m.hexdigest()

def file_is_openState(file_path):
    try:
        with open(file_path, "r") as f:
            return True
    except Exception as e:
        return False

if __name__ == '__main__':
    print(get_file_md5(r'D:\work\同步文件夹\新建文件夹 (4)\新建 文本文档.txt'))