
import logging
class NetworkError(Exception):
    def __init__(self, message):
        self.message = message if isinstance(message. str) and not message else "网络异常"
        logging.error(self.message)

class LoginPasswordError(Exception):
    def __init__(self, message):
        self.message = message if isinstance(message. str) and not message else "帐号密码错误"
        logging.error(self.message)

class UserProhibitError(Exception):
    def __init__(self, message):
        self.message = message if isinstance(message. str) and not message else "用户被禁止"
        logging.error(self.message)

class AccountError(Exception):
    def __init__(self, message):
        self.message = message if isinstance(message. str) and not message else "账户类型错误"
        logging.error(self.message)

