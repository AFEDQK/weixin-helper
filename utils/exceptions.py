import json


import json


class KnownException(Exception):
    def __init__(self, code, msg=""):
        self.code = code
        self.msg = msg
        self.errors = {}


class InputNotFound(KnownException):
    def __init__(self, text):
        self.errors = {}
        # 404 Not Found
        self.code = 404
        self.msg = f'输入文本不存在 "{text}"'
