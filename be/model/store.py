# import logging
# import os
# import sqlite3 as sqlite
# import psycopg2
#
#
#
# class Store:
#     database: str
#
#     def __init__(self, db_path):
#         #self.database = os.path.join(db_path, "be.db")
#         self.database = psycopg2.connect(
#             host='127.0.0.1',
#             user='postgres',
#             password='Haiyu7512',
#             database='bookstore',
#             #post ='5432'
#         )
#         self.init_tables()
#
#     def init_tables(self):
#         try:
#             conn = self.get_db_conn()
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user ("
#                 "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
#                 "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user_store("
#                 "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS store( "
#                 "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
#                 " PRIMARY KEY(store_id, book_id))"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order( "
#                 "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order_detail( "
#                 "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
#                 "PRIMARY KEY(order_id, book_id))"
#             )
#
#             conn.commit()
#         except sqlite.Error as e:
#             logging.error(e)
#             conn.rollback()
#
#     def get_db_conn(self) -> sqlite.Connection:
#         return sqlite.connect(self.database)
#
#
# database_instance: Store = None
#
#
# def init_database(db_path):
#     global database_instance
#     database_instance = Store(db_path)
#
#
# def get_db_conn():
#     global database_instance
#     return database_instance.get_db_conn()
# import logging
# import os
# import psycopg2
#
#
# class Store:
#     database: str
#
#     # def __init__(self, db_path):
#     #     self.database = os.path.join(db_path, "be.db")
#
#     def __init__(self, db_path):
#         self.database = os.path.join(db_path, "be.db")
#         self.init_tables()
#
#     def init_tables(self):
#         try:
#             conn = self.get_db_conn()
#             cursor = conn.cursor()
#
#             cursor.execute(
#                 "CREATE TABLE IF NOT EXISTS users ("
#                 "user_id VARCHAR(1024) PRIMARY KEY, password VARCHAR(1024) NOT NULL, "
#                 "balance INTEGER NOT NULL, token VARCHAR(1024), terminal VARCHAR(1024));"
#             )
#
#             cursor.execute(
#                 "CREATE TABLE IF NOT EXISTS user_store("
#                 "user_id VARCHAR(1024), store_id VARCHAR(1024), PRIMARY KEY(user_id, store_id));"
#             )
#
#             # cursor.execute(
#             #     """
#             #     CREATE TABLE IF NOT EXISTS store(
#             #         store_id VARCHAR(255),
#             #         book_id VARCHAR(255),
#             #         tags VARCHAR(255),
#             #         book_info TEXT,
#             #         pictures BYTEA,
#             #         id VARCHAR(255),
#             #         title TEXT,
#             #         author TEXT,
#             #         publisher TEXT,
#             #         original_title TEXT,
#             #         translator TEXT,
#             #         pub_year VARCHAR(255),
#             #         pages INTEGER,
#             #         price INTEGER,
#             #         binding TEXT,
#             #         isbn VARCHAR(255),
#             #         author_intro TEXT,
#             #         book_intro TEXT,
#             #         content TEXT,
#             #         stock_level INTEGER,
#             #         PRIMARY KEY (store_id, book_id)
#             #     )
#             #     """
#             # )
#             cursor.execute(
#                             "CREATE TABLE IF NOT EXISTS store( "
#                             "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
#                             " PRIMARY KEY(store_id, book_id))"
#                         )
#
#             cursor.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order ("
#                 "order_id VARCHAR(1024) PRIMARY KEY, "
#                 "store_id VARCHAR(1024), "
#                 "user_id VARCHAR(1024), "
#                 "book_status INTEGER, "
#                 "order_time TIMESTAMP)"
#             )
#
#             cursor.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order_detail( "
#                 "order_id VARCHAR(1024), book_id VARCHAR(1024), count INTEGER, price INTEGER,  "
#                 "PRIMARY KEY(order_id, book_id))"
#             )
#
#             cursor.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order_paid( "
#                 "order_id VARCHAR(1024), store_id VARCHAR(1024), user_id VARCHAR(1024), "
#                 "book_status INTEGER, price INTEGER, "
#                 "PRIMARY KEY(order_id, user_id))"
#             )
#
#             conn.commit()
#         except psycopg2.Error as e:
#             logging.error(e)
#             conn.rollback()
#
#     # def get_db_conn(self) -> psycopg2.extensions.connection:
#     #     self.database = psycopg2.connect(
#     #         host='127.0.0.1',
#     #         user='root',
#     #         password=
#     #         database='bookstore'
#     #     )
#     #
#     #     return self.database
#     def get_db_conn(self) -> psycopg2.extensions.connection:
#
#
#         conn = psycopg2.connect(
#             host='127.0.0.1',
#             user='postgres',
#             password='Haiyu7512',
#             database='bookstore'
#         )
#
#         return conn
#
#
# database_instance: Store = None
#
# def init_database(db_path):
#     global database_instance
#     database_instance = Store(db_path)
#
# def get_db_conn():
#     global database_instance
#     return database_instance.get_db_conn()
import logging
import os
import pymysql


class Store:
    database: str

    def __init__(self, db_path):
        self.init_tables()

    def init_tables(self):
        try:
            cur = self.get_db_conn()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS `user`(
                    user_id VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL,
                    balance INT NOT NULL,
                    token TEXT,
                    terminal TEXT
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS store(
                    store_id VARCHAR(255),
                    book_id VARCHAR(255),
                    book_info LONGTEXT,
                    stock_level INT,
                    PRIMARY KEY(store_id, book_id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_store(
                    user_id VARCHAR(255),
                    store_id VARCHAR(255),
                    PRIMARY KEY(user_id, store_id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS new_order(
                    order_id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255),
                    store_id VARCHAR(255),
                    status INT,
                    deadline DATETIME
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS new_order_detail(
                    order_id VARCHAR(255),
                    book_id VARCHAR(255),
                    count INT,
                    price INT,
                    PRIMARY KEY(order_id, book_id)
                )
            """)
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS history_order(
                                order_id VARCHAR(255) PRIMARY KEY,
                                user_id VARCHAR(255),
                                store_id VARCHAR(255),
                                status INT,
                                paid_time DATETIME
                            )
                        """)

            cur.connection.commit()
        except pymysql.Error as e:
            logging.error(e)
            cur.connection.rollback()

    def get_db_conn(self):
        db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, database='bookstore')
        return db.cursor()


database_instance: Store = None


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()