from .base import Mongo

class ZhibuDb(object):
    def __init__(self, db_name):
        self.db = Mongo(db_name=db_name)

    # def insert_user(self, obj):
    #     return self.db.insert_one(
    #         {
    #             'username': obj.username(),
    #             'nickname': obj.nickname(),
    #             'data_id': obj.get_data_id(),
    #             'gender': obj.get_gender(),
    #             'followees_num': obj.get_followees_num(),
    #             'followers_num': obj.get_followers_num(),
    #             'asks_num': obj.get_asks_num(),
    #             'answers_num': obj.get_answers_num(),
    #             'collections_num': obj.get_collections_num(),
    #             'agree_num': obj.get_agree_num(),
    #             'thanks_num': obj.get_thanks_num(),
    #             'profile_num': obj.get_profile_vote_num(),
    #             'fav_num': obj.get_profile_fav_num(),
    #             'fav_share': obj.get_profile_fav_share(),
    #             'carrer_exps': obj.get_carrer_exps(),
    #             'citys': obj.get_citys(),
    #             'eduction_exps': obj.get_eduction_exps(),
    #             'topics_num': obj.get_topics_num(),
    #         }
    #     )

    def insert_user(self, obj):
        return self.db.insert_one(obj)

    def user_topics(self, username, topic):
        return self.db.insert_one({
            'username': username,
            'name': topic.name,
            'url': topic.url
        })

    def topic(self):
        pass


    def collection(self, obj):
        return self.db.insert_one(
            {
                'name': obj.get_name(),
                'username': obj.creator.username(),
            }
        )

    def question(self, username, obj):
        return self.db.insert_one(
            {
                'title': obj.title(),
                'username': username,
                'detail': obj.get_detail(),
                'topic': obj.get_topics(),
            }
        )

