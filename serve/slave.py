import socket
import gevent
import logging
import json
import codecs

reader = codecs.getreader("utf-8")


from spider.zhihu import *


user_base_url = 'https://www.zhihu.com/people/%s'
task_url = ""

try:
    task_user = UserDetail(task_url)
except:
    task_user = None

class Slave:
    def __init__(self, ip='locahost', port=8888):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    def send(self, message):
        self.sock.sendall(message.encode('utf-8'))

    def accept(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

class Scarpy(object):
    def __init__(self, slave):
        self.slave = slave
        self.slave.connect()
    def has_repeat_user(self, obj):
        self.slave.send(json.dumps({'status': 1, 'username': obj.username() }))
        accept = self.slave.accept().decode('utf-8')
        print("accepted: %s" % accept)
        return int(0)

    def user_topics(self, obj):
        pass

    def user_questions(self, obj):
        pass

    def user_answers(self, obj):
        pass

    def user_detail(self, obj):
        return {
                'username': obj.username(),
                'nickname': obj.nickname().decode('utf-8'),
                'data_id': obj.get_data_id(),
                'gender': obj.get_gender(),
                'followees_num': obj.get_followees_num(),
                'followers_num': obj.get_followers_num(),
                'asks_num': obj.get_asks_num(),
                'answers_num': obj.get_answers_num(),
                'collections_num': obj.get_collections_num(),
                'agree_num': obj.get_agree_num(),
                'thanks_num': obj.get_thanks_num(),
                'profile_num': obj.get_profile_vote_num(),
                'fav_num': obj.get_profile_fav_num(),
                'fav_share': obj.get_profile_fav_share(),
                'carrer_exps': obj.get_carrer_exps(),
                'citys': obj.get_citys(),
                'eduction_exps': obj.get_eduction_exps(),
                'topics_num': obj.get_topics_num(),
            }

    def redis_cache(self):
        pass


    def run(self):
        """
        :argument status
            0: get_user
            1: check_user_repeat
            2 send_user_info
        :return:
        """
        task_url = ""
        while True:
            if not task_url:
                self.slave.send(json.dumps({'status': 0}))
                task_user_url = self.slave.accept().decode('utf-8')
                print("accept task_user %s" % task_user_url)
                if not task_user_url:
                    break
                task_user = UserDetail(user_base_url % task_user_url)
            else:
                task_user = UserDetail(task_url)
                task_url = None

            for user in task_user.get_followees():
                print(user.username())
                if not self.has_repeat_user(user):
                    user_detail = self.user_detail(user)
                    print(user_detail)
                    self.slave.send(json.dumps({'status': 2, 'detail': user_detail}))
                    # for tasks in [self.user_topics(user), self.ser_answers(user), self.user_questions(user)]:
                    #     cache user's topic , answers  and questions
                    #     for result in tasks:
                    #         self.redis_cache(result)

def task(ip, port):
    slave = Slave(ip, port)
    try:
        slave.connect()
    except Exception as e:
        logging.warning(e)
    print("send hello")
    slave.send("hello")
    # gevent.sleep()
    print(slave.accept())


if __name__ == '__main__':
    ip = 'localhost'
    port = 8888
    slave = Slave(ip, port)
    scarpy = Scarpy(slave)
    scarpy.run()
    # threads = [gevent.spawn(scarpy.run()) for i in range(10)]
    # gevent.joinall(threads)
    # task(ip, port)
