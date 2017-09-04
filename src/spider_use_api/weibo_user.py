# -*- coding: utf-8 -*-

from get_api_client import ApiClient


def get_uids():
    uids = []
    with open('../../docs/uid.txt') as fp:
        for line in fp:
            uids.append(line.strip())
    return uids

class WeiboUser():
    
    def __init__(self, uid, client):
        self.client = client

        self.uid = uid

    def get_user_data(self):
        self.get_user_show()
        self.get_user_timeline()
        self.get_friendships_friends_ids()

    def get_user_show(self):
        user_show =  self.client.users.show.get(uid = self.uid)
        
        self.name = user_show['name']
        self.screen_name = user_show['screen_name']
        self.gender = user_show['gender'] 
        self.description = user_show['description']
        self.created_at = user_show['created_at']
        
        self.friends_count = user_show['friends_count']
        self.statuses_count = user_show['statuses_count']
        self.followers_count = user_show['followers_count']
        self.bi_followers_count = user_show['bi_followers_count'] 
        self.favourites_count = user_show['favourites_count']
        
        self.province = user_show['province']
        self.city = user_show['city']
        self.location = user_show['location']
         
        self.verified = user_show['verified']
        self.verified_reason = user_show['verified_reason']
        self.credit_score = user_show['credit_score'] 
    
    def get_friendships_friends_ids(self):
        print self.client.friendships.friends.ids.get(uid = self.uid)
        
    def get_user_timeline(self):
        print 
        
if __name__ == '__main__':
    uids = get_uids()
    client = ApiClient.get_client(ApiClient())
    for uid in uids:
        u = WeiboUser(uid, client)
        u.get_user_data()

