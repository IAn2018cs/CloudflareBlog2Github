# coding=utf-8
import base64
import os
import random
import string
import time
from datetime import datetime
from os import PathLike
from typing import AnyStr


def resolve_relative_path(file: PathLike[AnyStr], path: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(file), path))


def get_timestamp() -> int:
    """
    获取毫秒时间戳
    :return: 毫秒
    """
    t = time.time()
    return int(round(t * 1000))


def generate_random_id(length=10):
    characters = string.ascii_letters + string.digits  # 包含所有字母（大写和小写）和数字
    id = ''.join(random.choice(characters) for _ in range(length))  # 随机选择字符
    return id


def get_base64_image(path) -> str:
    with open(path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data)  # base64编码
        return base64_data.decode('utf-8')


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_current_data():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")
    return formatted_date


def get_current_datatime():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())


def get_image_temp_path() -> str:
    temp_image_path = resolve_relative_path(__file__, '../temp_image/')
    create_path(temp_image_path)
    return temp_image_path


def split_list_with_min_length(original_list: list, min_length: int) -> list[list]:
    if min_length <= 0:
        raise "Error: Minimum length must be a positive number."

    length = len(original_list)

    # Calculate the number of sublists that can be created
    num_sublists = (length + min_length - 1) // min_length  # Use ceiling division

    # Initialize the starting index and result list
    start = 0
    result = []

    for i in range(num_sublists):
        # For the last sublist, include all remaining elements
        if i == num_sublists - 1:
            result.append(original_list[start:])
        else:
            # Append elements to each of the other sublists
            result.append(original_list[start:start + min_length])
            start += min_length

    return result


def save_txt_to_file(file_path: str, content: str):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def format_time(seconds):
    """将秒数格式化为更易读的形式"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)} 小时 {int(minutes)} 分钟 {int(seconds)} 秒"
    elif minutes > 0:
        return f"{int(minutes)} 分钟 {int(seconds)} 秒"
    else:
        return f"{int(seconds)} 秒"


def is_valid_str(value) -> bool:
    if value is None:
        return False
    v = str(value).strip().replace("\n", "").lower()
    return v not in ["", "null", "nil", "none", "nan"]
