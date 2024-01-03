import sqlite3 as sl
from sqlite3 import Error, IntegrityError


def create_connection(db_file):
    conn = None
    try:
        conn = sl.connect(db_file)
    except Error as e:
        print(e)
    except Exception as e:
        print(e)
    return conn


def insert_user(conn, task):
    sql = '''INSERT INTO Users(u_user_id,u_chat_id) values (?,?)'''

    cur = conn.cursor()
    try:
        cur.execute(sql, task)
    except IntegrityError:
        return None
    conn.commit()