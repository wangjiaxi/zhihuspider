from __future__ import absolute_import
import gevent
import redis
import threading
import socketserver
import json
import logging
import socket

from http.server import BaseHTTPRequestHandler

from gevent.queue import Queue
from spider.zhihu import *
from trans.socketserver import ThreadedTCPServer
from db.zhuhu_db import ZhibuDb
from db.base import Mongo
tasks = Queue
mongo_zh = ZhibuDb('zhihu')

conn = Mongo(db_name='zhihu')
user_db = conn.db['user']

BASE_URL = 'https://www.zhihu.com/people/hugo/'
base_user = UserDetail('https://www.zhihu.com/people/hugo/')

user_has_saved = set()
user_as_parent = set(['bugissomewhere', 'Blue7', 'yan-xiao-chuan-77', 'yinshoufu', 'melodyrosy', 'zhuang-dian-89', 'ganyu-25', 'kqx1987', 'liu-xin-77-43-38', '-yu-25'])
user_as_parent_used = set()

class Master:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.request_handler = None
        self.server = None

    def build(self):
        self.server = ThreadedTCPServer((self.host, self.port), self.request_handler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        # print(dir(server_thread))
        server_thread.daemon = True
        server_thread.start()
        self.server.serve_forever()

    def server_address(self):
        if not self.server:
            self.build()
        return self.server.server_address


    def shutdown(self):
        if self.server:
            return self.server.shutdown()
        return self.server

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            accept = self.accept()
            if accept:
                try:
                    data = json.loads(accept)
                except Exception as e:
                    print(data)
                    logging.error(e)

                if data['status'] == 0:
                    user = user_as_parent.pop()
                    user_as_parent_used.add(user)
                    logging.warning("send user %s to slave" % user)
                    self.send(user.encode())
                elif data['status'] == 1:
                    logging.warning("check repeat user : %s" % data['username'])
                    if data['username'] in user_has_saved:
                        self.send("1".encode())
                    else:
                        self.send("0".encode())
                elif data['status'] == 2:
                    # mongo_zh.insert_user(data)
                    logging.warning("*" * 40)
                    logging.warning(self.cur_thread().name)
                    logging.warning("*" * 40)
                    logging.warning("saved user: %s" % data['detail']['nickname'])
                    user_db.insert_one(data['detail'])
                    logging.warning(user_has_saved)
                    logging.warning(user_as_parent)
                    logging.warning(user_as_parent_used)
                    user = data['detail']['username']
                    user_has_saved.add(user)
                    if user not in user_as_parent_used:
                        user_as_parent.add(data['detail']['username'])
            else:
                break

    def send(self, response):
        return self.request.sendall(response)

    def accept(self):
        return self.request.recv(1024).decode('utf-8')

    def cur_thread(self):
        return threading.current_thread()



# master = Master()
# for user in base_user.get_followees():
#     tasks.put(user.user_url)
#
# def run():
#     for task in tasks:
#         sender, recived = master.accept()
#         task.put(recived)
#         master.send(sender, task.put())
#
import time

if __name__ == '__main__':
    host = None
    port = None
    master = Master()
    master.request_handler = ThreadedTCPRequestHandler
    master.build()

