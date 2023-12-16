import hashlib


def generate_short_link(original_link):
    return hashlib.shake_256(original_link.encode()).hexdigest(6) + "/"
