import inspect
import logging
import os
from datetime import datetime
from main import Dir
from colorama import Fore


def info(text):
    """
    日志格式：[INFO]当前时间年月日时分秒--代码路径:代码行数--打印信息
    颜色：绿色
    写入文件：文件路径+ log +文件名
    :param text: 打印的信息
    :return:
    """
    stack = inspect.stack()
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]  # 获取当前时间
    code_path = f'{os.path.basename(stack[1].filename)}:{stack[1].lineno}'
    content = f'[INFO]{formatted_time}--{code_path}--{text}'
    print(Fore.LIGHTGREEN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')


def error(text):
    """
    日志格式：[ERROR]当前时间年月日时分秒--代码路径:代码行数--打印信息
    颜色：红色
    写入文件：文件路径+ log +文件名
    :param text: 打印的信息
    :return:
    """
    stack = inspect.stack()
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]  # 获取当前时间
    code_path = f'{os.path.basename(stack[1].filename)}:{stack[1].lineno}'
    content = f'[ERROR]{formatted_time}--{code_path}--{text}'
    print(Fore.LIGHTRED_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')
    with open(file=Dir + '\\logs\\' + f'{str_time}_error.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')


def step(text):
    """
    日志格式：[STEP]当前时间年月日时分秒--代码路径:代码行数--打印信息
    颜色：红色
    写入文件：文件路径+ log +文件名
    :param text: 打印的信息
    :return:
    """
    stack = inspect.stack()
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]  # 获取当前时间
    code_path = f'{os.path.basename(stack[1].filename)}:{stack[1].lineno}'
    content = f'[STEP]{formatted_time}--{code_path}--{text}'
    print(Fore.LIGHTCYAN_EX + content)
    str_time = datetime.now().strftime("%Y%m%d")
    with open(file=Dir + '\\logs\\' + f'{str_time}_info.log', mode='a', encoding='utf-8') as f:
        f.write(content + '\n')
