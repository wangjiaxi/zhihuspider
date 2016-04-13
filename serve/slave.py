import socket
import gevent
import logging
import json
import codecs
import gevent.monkey
# from gevent import socket
# gevent.monkey.patch_socket()
reader = codecs.getreader("utf-8")


from spider.zhihu import *
from db.base import Mongo

user_base_url = 'https://www.zhihu.com/people/%s'
task_url = ""

class Slave:
    def __init__(self, ip='locahost', port=8888):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.ip, self.port))
        except ConnectionRefusedError as e:
            logging.error(e)

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
        self.conn = Mongo(db_name='zhihu')

    def has_repeat_user(self, obj):
        self.slave.send(json.dumps({'status': 1, 'username': obj.username()}))
        accept = self.slave.accept().decode('utf-8')
        logging.warning("accepted: %s" % accept)
        if accept.isdigit():
            return int(accept)
        return 0

    def user_topics(self, obj):
        pass

    def rigint_user(self, obj):
        try:
            obj.get_agree_num()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def user_questions(self, obj):
        pass

    def user_answers(self, obj):
        return obj.get_answers()

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

    def get_task_user(self, task_url=None):
        if not task_url:
            self.slave.send(json.dumps({'status': 0}))
            task_url = self.slave.accept().decode('utf-8')
            print(task_url * 10)
            if task_url == "" or not task_url:
                return None
        return UserDetail(user_base_url % task_url)

    def redis_cache(self):
        pass


    def save_answer(self, obj):

        answer = {

        }

    def save_ask(self, obj, username):
        ask = {
            'url': obj.url,
            'username': username,
            'title': obj.get_title(),
            'answers_num': obj.get_answers_num(),
            'followers_num': obj.get_followers_num(),
            'topics': obj.get_topics(),
            'visit_times': obj.get_visit_times(),
        }
        col_ask = self.conn.db['ask']
        col_ask.insert_one(ask)

    def save_topic(self, obj, username):
        topic = {
            'name': obj.name,
            'topic_id': obj.id,
            'username': username,
        }
        col_topic = self.conn.db['topic']
        col_topic.insert_one(topic)

    def run(self):
        """
        :argument status
            0: get_user
            1: check_user_repeat
            2 send_user_info
        :return:
        """
        while True:
            while True:
                task_user = self.get_task_user()
                if task_user is None:
                    return
                elif self.rigint_user(task_user):
                    break
            for user in task_user.get_followees():
                print(user.username())
                username = user.username()
                if not self.has_repeat_user(user):
                    user_detail = self.user_detail(user)
                    logging.warning(user_detail)
                    self.slave.send(json.dumps({'status': 2, 'detail': user_detail}))
                    # for tasks in [ self.user_answers(user),]:
                        # cache user's topic , answers  and questions
                        # for result in tasks:
                            # print(result)
                            # self.redis_cache(result)

                    for ask in user.get_asks():
                        print("save_ask of %s" % username)
                        self.save_ask(ask, username)

                    for topic in user.get_topics():
                        print("save_topic of %s" % username)
                        self.save_topic(topic, username)


def task(ip, port, i):
    print(str(i) * 50)
    slave = Slave(ip, port)
    scarpy = Scarpy(slave)
    scarpy.run()
    # print(slave.accept())

if __name__ == '__main__':
    ip = 'localhost'
    port = 8888
    slave = Slave(ip, port)
    scarpy = Scarpy(slave)
    # scarpy.run()
    threads = [gevent.spawn(task, ip, port, i) for i in range(3)]
    gevent.joinall(threads)
    # task(ip, port)
