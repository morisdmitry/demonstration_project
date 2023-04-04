from datetime import datetime
import string
import random


def timestamp_now() -> int:
    return datetime.now().timestamp() * 1000


def id_generate(length):
    char_set = string.ascii_uppercase + string.digits
    return "".join(random.choice(char_set) for _ in range(length))
