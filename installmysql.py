#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月21日

@version         v1.0.0 

@copyright       Sugarguo

File             install.py

'''


import os
import sys
sys.path.insert(0,'ext_lib')
import MySQLdb
from werkzeug.security import generate_password_hash

DB_FILE_PATH = os.environ.get('DEV_DATABASE_URL')
#DB_FILE_PATH = 'mysql://root:123456@127.0.0.1/db_flask_blog_dev'
SHOW_SQL = False#True


if DB_FILE_PATH[:8] == 'mysql://':
    DB_FILE_PATH = DB_FILE_PATH[8:]
else:
    print "db error! please check"
    exit()



dburl = DB_FILE_PATH.split("@")

dbhost = dburl[1].split(":")[0]

dbuser = dburl[0].split(":")[0]

dbpasswd = dburl[0].split(":")[1]

dbport = dburl[1].split(":")[1].split("/")[0]

db = dburl[1].split(":")[1].split("/")[1]


print dbuser, dbpasswd, dbhost, dbport, db


def get_conn(dbuser, dbpasswd, dbhost, dbport, db):
    conn = MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpasswd,db=db,port=int(dbport))
    print('Mysql in :[{}]'.format(DB_FILE_PATH))
    return conn

def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()

def close_all(conn, cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if cu is not None:
            cu.close()

def run_sql(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        if SHOW_SQL:
            print('Done sql:[{}]'.format(sql))
        cu.execute(sql)
        conn.commit()
        print('    __SQL...Success!\n')
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))


sqlfile_name = raw_input("Please input sql file name:\n")
sqlfile = file(sqlfile_name,'r')
sqlstr = sqlfile.read()
sqlfile.close()


conn = get_conn(dbuser, dbpasswd, dbhost, dbport, db)

print "Create DB!\n"
sqllist = sqlstr.split(";")

for index,itemsql in enumerate(sqllist):
    print index,itemsql
    if index == len(sqllist) - 1:
        pass
    else:
        run_sql(conn, itemsql + ";")

user_name = raw_input("Please input user name:\n")
user_password = raw_input("Please input user password:\n")
user_email = raw_input("Please input user email:\n")

insuser_password = generate_password_hash(user_password)
sqluser = "INSERT INTO users (id,username, password_hash, email, work_status,submit_status) VALUES (0,'%s','%s','%s',0,0);" % (user_name, insuser_password, user_email)
run_sql(conn, sqluser)


'''
try:
    conn=MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpasswd,db=db,port=int(dbport))
    cur=conn.cursor()
    cur.execute(sqluser)
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
'''

print "\n\nWell Done! Please use\n\ngunicorn --config gunicorn.conf runserver:app\n\nrun the project!"

