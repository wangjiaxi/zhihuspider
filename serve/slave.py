
from spider.zhihu import *

task_url = ""

task_user = UserDetail(task_url)

class Slave:
    def __init__(self):
        pass

    def connect(self):
        pass

    def send(self):
        pass

    def accept(self):
        pass


def has_repeat_user(user):
    pass

def user_topics(user):
    pass

def user_questions(user):
    pass

def user_answers(user):
    pass

def user_detail(user):
    pass

def redis_cache():
    pass

slave = Slave()

def run():
    while True:
        for user in task_user.get_followees():
            if not has_repeat_user(user):
                user_detail = user_detail(user)
                slave.send(user_detail)
                for tasks in [user_topics(user), user_answers(user), user_questions(user)]:
                    # cache user's topic , answers  and questions
                    for result in tasks:
                        redis_cache(result)
        task_user = slave.accept()
        if not task_user:
            break
