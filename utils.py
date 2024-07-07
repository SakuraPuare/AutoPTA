
import re


def is_email(data: str) -> bool:
    if re.match(r"[^@]+@[^@]+\.[^@]+", data):
        return True
    return False


def is_cn_phone(data: str) -> bool:
    if re.match(r"^1[3-9]\d{9}$", data):
        return True
    return False
