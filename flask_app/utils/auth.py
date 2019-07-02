import hashlib


def md5_key(password):
    md5 = hashlib.md5()
    md5.update(bytes(password, encoding="utf8"))
    return md5.hexdigest()