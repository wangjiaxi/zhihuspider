from zhihu import User, UserDetail
user = UserDetail("https://www.zhihu.com/people/hualong-mei/about")
t = user.get_followees()
# user.get_followees_num()
print(user.get_user_id())
print(user.get_data_id())
print(user.get_gender())
print(user.get_followees_num())
print(user.get_followers_num())
print(user.get_agree_num())
print(user.get_thanks_num())
print(user.get_asks_num())
print(user.get_answers_num())
print(user.get_collections_num())
print(user.get_profile_vote_num())
print(user.get_profile_thank_num())
print(user.get_profile_fav_num())
print(user.get_profile_fav_share())
t = user.get_carrer_exps()

for i in t:
    print(i)

