import MySQLdb


def get_db_uids():
    db_uids = []
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj', charset="utf8")
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    sql = 'SELECT UID  FROM RAW_USER_TAG'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()
    
    return len(results)

print get_db_uids()


