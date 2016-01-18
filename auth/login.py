
import requests
import re
import json, platform, random, os
import logging

from http import cookiejar
from functools import wraps
requests = requests.Session()
requests.cookies = cookiejar.LWPCookieJar(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../cookies'))
try:
    requests.cookies.load(ignore_discard=True)
except:
    pass

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

try:
    from ConfigParser import ConfigParser

except ImportError:
    from configparser import ConfigParser

logIN_URL = "https://www.zhihu.com/login/email"

def get_login_info(filename):
    config = ConfigParser()
    config.read(filename)
    email = config.get('info', 'email')
    password = config.get('info', 'password')
    return email, password

class Auth:
    def __init__(self, email=None, password=None, *args, **kwargs):
        self.email = email
        self.password = password
        self.cookies = None

    def login_form(self):
        if not re.match(r"^\S+\@\S+\.\S+$", self.email):
            raise AccountError("帐号类型错误")

        form = {"email":self.email, "password": self.password, "remember_me": True }
        form['_xsrf'] = self.get_xsrf()
        form['captcha'] = self.download_captcha()
        logging.warning(form)
        return form

    def get_xsrf(self):
        url = "http://www.zhihu.com/"
        r = requests.get(url)
        if int(r.status_code) != 200:
            raise NetworkError("验证码请求失败")
        results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
        if len(results) < 1:
            logging.info(u"提取XSRF 代码失败")
            return None
        return results[0]

    def download_captcha(self):
        url = "http://www.zhihu.com/captcha.gif"
        r = requests.get(url, params={"r": random.random()})
        logging.warning(r.cookies)
        self.cookies = r.cookies
        if int(r.status_code) != 200:
            raise NetworkError(u"验证码请求失败")
        image_name = u"verify." + r.headers['content-type'].split("/")[1]
        open(image_name, "wb").write(r.content)
        """
            System platform: https://docs.python.org/2/library/platform.html
        """
        logging.info(u"正在调用外部程序渲染验证码 ... ")
        if platform.system() == "Linux":
            logging.info(u"Command: xdg-open %s &" % image_name )
            os.system("xdg-open %s &" % image_name )
        elif platform.system() == "Darwin":
            logging.info(u"Command: open %s &" % image_name )
            os.system("open %s &" % image_name )
        elif platform.system() == "SunOS":
            os.system("open %s &" % image_name )
        elif platform.system() == "FreeBSD":
            os.system("open %s &" % image_name )
        elif platform.system() == "Unix":
            os.system("open %s &" % image_name )
        elif platform.system() == "OpenBSD":
            os.system("open %s &" % image_name )
        elif platform.system() == "NetBSD":
            os.system("open %s &" % image_name )
        elif platform.system() == "Windows":
            os.system("%s" % image_name )
        else:
            logging.info(u"我们无法探测你的作业系统，请自行打开验证码 %s 文件，并输入验证码。" % os.path.join(os.getcwd(), image_name) )
        captcha_code = input("请输入验证码: ", )
        return captcha_code

    def login(self):
        if self.is_login() == True:
            logging.warning(u"你已经登录过咯")
            return True
        url = logIN_URL
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/",
            'X-Requested-With': "XMLHttpRequest"
        }
        payload = self.login_form()
        r = requests.post(url, data=payload, headers=headers)
        logging.warning(self.cookies)
        logging.warning(r.cookies)
        r.cookies = self.cookies
        logging.warning(r.cookies)
        logging.warning(r.cookies)
        if int(r.status_code) != 200:
            raise NetworkError(u"表单上传失败!")
    
        if r.headers['content-type'].lower() == "application/json":
            try:
                # 修正  justkg 提出的问题: https://github.com/egrcc/zhihu-python/issues/30
                result = json.loads(r.content.decode())
            except Exception as e:
                logging.error(u"JSON解析失败！")
                logging.error(e)
                logging.debug(r.content)
                result = {}
            if result["r"] == 0:
                logging.warning(u"登录成功！")
                requests.cookies.save()
                return {"result": True}
            elif result["r"] == 1:
                logging.warning(u"登录失败！")
                return {"error": {"code": int(result['errcode']), "message": result['msg'], "data": result['data'] } }
            else:
                logging.warning(u"表单上传出现未知错误: \n \t %s )" % (str(result)))
                return {"error": {"code": -1, "message": u"unknow error"}}
        else:
            logging.warning(u"无法解析服务器的响应内容: \n \t %s " % r.text)
            return {"error": {"code": -2, "message": u"parse error"}}


    def is_login(self):
        url = "https://www.zhihu.com/settings/profile"
        r = requests.get(url, allow_redirects=False)
        status_code = int(r.status_code)
        if status_code == 301 or status_code == 302:
            # 未登录
            return False
        elif status_code == 200:
            return True
        else:
            logging.warning(u"网络故障")
            return None

def login_required(email=None, password=None):
    def Decorator(f):
        @wraps(f)
        def wapper(*args, **kwargs):
            auth = Auth(email, password)
            if auth.is_login():
                return f(*args, **kwargs)
            else:
                auth.login()
        return wapper
    return Decorator

if __name__ == "__main__":
    email, password = get_login_info('../config.ini')
    auth = Auth(email=email, password=password)
    print(auth.login())
