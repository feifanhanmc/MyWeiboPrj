import MySQLdb


def test():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    
    sql = """SELECT * FROM RAW_USER"""
    cursor.execute(sql)
    print len(cursor.fetchall())
    db.close()   

test()