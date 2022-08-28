import random
import string


def generate_token(size=100):
    return ''.join([random.choice(string.digits+string.ascii_letters) for _ in range(size)])
