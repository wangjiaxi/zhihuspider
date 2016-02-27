import gevent
import redis
from gevent.queue import Queue

from spider.zhihu import *

tasks = Queue
BASE_URL = 'https://www.zhihu.com/people/hugo/'
base_user = UserDetail('https://www.zhihu.com/people/hugo/')

class Master:
    def __init__(self):
        pass

    def connect(self):
        pass

    def send(self, reciver, content):
        pass

    def accept(self):
        pass

master = Master()
for user in base_user.get_followees():
    tasks.put(user.user_url)

def run():
    for task in tasks:
        sender , recived = master.accept()
        task.put(recived)
        master.send(sender, task.put())
