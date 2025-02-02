import hashlib
import random
import re
import string


def generate_referral_code(username: str, string_len: int = 10) -> str:
    result_hash = hashlib.sha256(username.encode('utf-8'))
    hex_digest = result_hash.hexdigest()

    random.seed(hex_digest)
    
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for _ in range(string_len))


def is_string_alphanumeric(input_str: str) -> bool:
    return re.fullmatch(r'^[a-zA-Z0-9]+$', input_str)

def is_string_alphanumeric_white_space(input_str: str) -> bool:
    return re.fullmatch(r'^[a-zA-Z0-9 ]+$', input_str)