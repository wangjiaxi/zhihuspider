import socket
import os
import threading
import socketserver

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class GoUpstairs:
    def countWays(self, n):
        # write code here
        base = [[1,1],[1,0]]
        surplus = [[1,0],[0,1]]     #初始为单位矩阵
        while n > 1:
            if n % 2  == 1:
                surplus = self.multimat(surplus,base)
                n = n - 1
            else:
                base = self.multimat(base,base)
                n = n >> 1          # n /2
        res = self.multimat(base,surplus)
        return res[0][0] %1000000007

    def multimat(self,a,b):
        result = [[0,0],[0,0]]
        for i in range(len(a)):
            for j in range(len(b)):
                for k in range(len(result)):
                    result[i][j] += a[i][k]*b[k][j]%1000000007
        return result

import  tornado
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
