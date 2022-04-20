# {success: true, message: "success",data: {...}}
from typing import Any


class BaseResult(object):
    success: bool
    message: str
    data: Any

    def __init__(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data
