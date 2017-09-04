# -*- coding: utf-8 -*-

import MySQLdb
from get_api_client import ApiClient
class SaveUserData():
    def __init__(self):
        self.db = self.connect_db()
#         self.init_db()
#         self.user_data = GetUserData().get_user_data()
#         self.save_user_data()
        self.disconnect_db()
        
    
    def connect_db(self):
        db = MySQLdb.connect('localhost', 'root', 'han8528520258', 'myweiboprj')
        return db

    
    def init_db(self):
        
        return 
    
    def save_user_data(self):
        return
    
    def disconnect_db(self):
        self.db.close()

if __name__ == '__main__':
    u = SaveUserData()