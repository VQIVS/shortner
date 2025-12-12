"""Base62 encoding for short URL generation"""

import random
import string

BASE62_CHARS = string.digits + string.ascii_letters  # 0-9a-zA-Z


def encode_base62(number: int) -> str:
    """Encode a number to base62 string"""
    if number == 0:
        return BASE62_CHARS[0]
    
    encoded = []
    while number > 0:
        encoded.append(BASE62_CHARS[number % 62])
        number //= 62
    
    return "".join(reversed(encoded))


def decode_base62(encoded: str) -> int:
    """Decode a base62 string to a number"""
    result = 0
    for char in encoded:
        result = result * 62 + BASE62_CHARS.index(char)
    return result


def generate_short_code(length: int = 6) -> str:
    """Generate a random base62 short code of specified length"""
    return "".join(random.choice(BASE62_CHARS) for _ in range(length))
