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
import sqlite3
from werkzeug.security import generate_password_hash


DB_FILE_PATH = os.environ.get('DEV_DATABASE_URL')
#DB_FILE_PATH = 'mysql://root:123456@127.0.0.1/db_flask_blog_dev'
SHOW_SQL = False#True


if DB_FILE_PATH[:10] == 'sqlite:///':
    DB_FILE_PATH = DB_FILE_PATH[10:]
else:
    pass


def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('Sqlite in :[{}]'.format(path))
        return conn
    else:
        conn = None
        print('Mem Sqlite :[:memory:]')
        return sqlite3.connect(':memory:')

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

conn = get_conn(DB_FILE_PATH)

print "Create DB!\n"
sqllist = sqlstr.split(";")

for index,itemsql in enumerate(sqllist):
    if index == len(sqllist) - 1:
        pass
    else:
        run_sql(conn, itemsql + ";")

user_name = raw_input("Please input user name:\n")
user_password = raw_input("Please input user password:\n")
user_email = raw_input("Please input user email:\n")

insuser_password = generate_password_hash(user_password)

print "INSERT users!\n"
sqluser = "INSERT INTO users (id,username, password_hash, email) VALUES (0,'%s','%s','%s');" % (user_name, insuser_password, user_email)
#conn = get_conn(DB_FILE_PATH)
run_sql(conn, sqluser)



print "\n\nWell Done! Please use\n\ngunicorn --config gunicorn.conf runserver:app\n\nrun the project!"

