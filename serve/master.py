import gevent
import redis
import threading
import socketserver

from gevent.queue import Queue

from spider.zhihu import *
from trans.socketserver import ThreadedTCPServer
tasks = Queue
BASE_URL = 'https://www.zhihu.com/people/hugo/'
base_user = UserDetail('https://www.zhihu.com/people/hugo/')

class Master:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8888
        self.request_handler = None
        self.server = None

    def build(self):
        self.server = ThreadedTCPServer((self.host, self.port), self.request_handler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

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
        data = self.accept()
        print(dir(self.cur_thread()))
        response = "%s reviced %s :" % (self.cur_thread().getName(), data)
        response = response.encode()
        self.send(response)

    def send(self, response):
        return self.request.sendall(response)

    def accept(self):
        return str(self.request.recv(1024), 'ascii')

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
if __name__ == '__main__':
    pass