from datetime import datetime, timedelta

import pymysql
import uuid
import json
import logging
from be.model import db_conn
from be.model import error


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(
            self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            for book_id, count in id_and_count:

                query = ("SELECT book_id, stock_level, book_info FROM store ""WHERE store_id = %s AND book_id = %s;")

                # 执行查询
                params = (store_id, book_id)
                self.cursor.execute(query, params)
                row = self.cursor.fetchone()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                stock_level = row[1]
                book_info = row[2]
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)
                update_query = ("UPDATE store SET stock_level = stock_level - %s ""WHERE store_id = %s AND book_id = %s AND stock_level >= %s;")

                # 执行更新
                params = (count, store_id, book_id, count)
                self.cursor.execute(update_query, params)

                insert_query = ("INSERT INTO new_order_detail(order_id, book_id, count, price) ""VALUES(%s, %s, %s, %s);")

                # 执行插入
                params = (uid, book_id, count, price)
                self.cursor.execute(insert_query, params)
            current_time = datetime.now()
            deadline = current_time + timedelta(seconds=10)

            # SQL插入语句
            insert_query = ("INSERT INTO new_order(order_id, store_id, user_id, status, deadline) ""VALUES(%s, %s, %s, %s, %s);")

            # 执行插入
            params = (uid, store_id, user_id, 1, deadline)
            self.cursor.execute(insert_query, params)
            self.cursor.connection.commit()
            order_id = uid
        except pymysql.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:

            query = ("SELECT order_id, user_id, store_id, status, deadline ""FROM new_order WHERE order_id = %s;")

            # 执行查询
            params = (order_id,)
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            status = row[3]
            deadline=row[4]
            if deadline and deadline < datetime.now():
                # 如果 deadline 存在且小于当前时间，则删除订单
                self.cursor.execute("DELETE FROM new_order WHERE order_id = %s", (order_id,))

                insert_query = ("INSERT INTO history_order (order_id, user_id, store_id, status) ""VALUES (%s, %s, %s, %s);")

                # 执行插入
                params = (order_id, user_id, store_id, 0)
                self.cursor.execute(insert_query, params)
                self.cursor.connection.commit()
                return 518, "Order deleted due to expired deadline"

            # 查看status
            if status != 1:
                return 520, f"already paid order id {order_id}"  # 已支付的订单

            query = ("SELECT balance, password FROM user ""WHERE user_id = %s;")

            # 执行查询
            params = (buyer_id,)
            self.cursor.execute(query, params)

            # 获取查询结果的第一行
            row = self.cursor.fetchone()

            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            query = ("SELECT store_id, user_id FROM user_store ""WHERE store_id = %s;")
            # 执行查询
            params = (store_id,)
            self.cursor.execute(query, params)

            row = self.cursor.fetchone()


            seller_id = row[1]



            query = ("SELECT book_id, count, price FROM new_order_detail ""WHERE order_id = %s;")

            # 执行查询
            params = (order_id,)
            self.cursor.execute(query, params)

            total_price = 0
            for row in self.cursor:
                count = row[1]
                price = row[2]
                total_price = total_price + price * count

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            update_query = ("UPDATE user SET balance = balance - %s ""WHERE user_id = %s AND balance >= %s;")

            # 执行更新
            params = (total_price, buyer_id, total_price)
            self.cursor.execute(update_query, params)


            delete_query = "DELETE FROM new_order WHERE order_id = %s;"
            # 执行删除
            params = (order_id,)
            self.cursor.execute(delete_query, params)

            paid_time = datetime.now()

            # SQL插入语句
            insert_query = ("INSERT INTO history_order(order_id, user_id, store_id, status, paid_time) ""VALUES(%s, %s, %s, %s, %s);")

            # 执行插入
            params = (order_id, user_id, store_id, 2, paid_time)
            self.cursor.execute(insert_query, params)


            self.cursor.connection.commit()

        except pymysql.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:

            query = "SELECT password FROM user WHERE user_id = %s;"
            # 执行查询
            params = (user_id,)
            self.cursor.execute(query, params)

            row = self.cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()
            update_query = ("UPDATE user SET balance = balance + %s WHERE user_id = %s;")

            # 执行更新
            params = (add_value, user_id)
            self.cursor.execute(update_query, params)

            self.cursor.connection.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def receive_books(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            # Check if the user exists
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)

            # Check if the order exists
            self.cursor.execute("SELECT * FROM history_order WHERE order_id = %s", (order_id,))
            order = self.cursor.fetchone()
            if not order:
                return error.error_invalid_order_id(order_id)

            # Check user authorization
            self.cursor.execute("SELECT password FROM user WHERE user_id = %s", (user_id,))
            user_password=self.cursor.fetchone()

            if user_password[0] != password:
                return error.error_authorization_fail()

            # Check if the order belongs to the user
            if order[1] != user_id:
                return error.error_authorization_fail()

            # Check if the order status is 3 (assuming 3 represents "sent")
            if order[3] != 3:
                return 500, "Invalid order status"

            # Calculate total price
            total_price = 0
            self.cursor.execute("SELECT * FROM new_order_detail WHERE order_id = %s", (order_id,))
            order_details = self.cursor.fetchall()

            for order_doc in order_details:
                count = order_doc[2]
                price = order_doc[3]
                book_total = count * price
                total_price += book_total

            # Get seller_id from the store
            self.cursor.execute("SELECT * FROM user_store WHERE store_id = %s", (order[2],))
            seller_store=self.cursor.fetchone()
            print(type(seller_store))
            seller_id = seller_store[0]


            # Update seller's balance
            self.cursor.execute("UPDATE user SET balance = balance + %s WHERE user_id = %s", (total_price, seller_id))

            # Update order status to 4 (assuming 4 represents "received")
            self.cursor.execute(
                "UPDATE history_order SET status = %s WHERE order_id = %s",
                (4, order_id)
            )
            self.cursor.connection.commit()

        except pymysql.Error as e:
            logging.error("MySQL Error: {}".format(str(e)))
            return 500, "Internal Server Error"

        return 200, "OK"

    def cancel(self, user_id, order_id):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)

            # 检查订单是否存在于 new_order 表中
            query_order = "SELECT * FROM `new_order` WHERE order_id = %s"
            self.cursor.execute(query_order, (order_id,))
            order = self.cursor.fetchone()
            store_id=order[0]

            if order is None:
                return 518, error.error_invalid_order_id(order_id)

            # 检查订单状态是否可取消（例如，状态为 1 表示待处理）
            if order[3] != 1:
                return 521, error.error_order_status(order_id)

            # 将订单状态更新为已取消（例如，状态为 0）
            query_update_status = "UPDATE `new_order` SET status = 0 WHERE order_id = %s"
            self.cursor.execute(query_update_status, (order_id,))

            # 将取消的订单插入到 history_order 表中
            self.cursor.execute(
                "INSERT INTO history_order (order_id, user_id, store_id, status) VALUES (%s, %s, %s, %s)",
                (order_id, user_id, store_id, 0))

            # 从 new_order 表中删除订单
            query_delete_order = "DELETE FROM `new_order` WHERE order_id = %s"
            self.cursor.execute(query_delete_order, (order_id,))

            self.cursor.connection.commit()

        except pymysql.Error as e:
            print(f"Error executing SQL query: {e}")
            return 500, str(e)

        return 200, "ok"

    def search_history_order(self, user_id):
        try:
            # 检查用户是否存在
            if not self.user_id_exist(user_id):
                return 513, "non exist user_id", []

            result = []

            # 使用 pymysql 执行查询
            query = "SELECT order_id, store_id, status, paid_time FROM history_order WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            rows = self.cursor.fetchall()

            for row in rows:
                print(row[1])
                order_data = {
                    "order_id": row[0],
                    "store_id": row[1],
                    "status": row[2],
                    "paid_time": row[3]
                }
                result.append(order_data)

        except pymysql.Error as e:
            return 529, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []

        return 200, "ok", result

# import psycopg2
# import uuid
# import json
# import logging
# from be.model import db_conn
# from be.model import error
#
# class Buyer(db_conn.DBConn):
#     def __init__(self):
#         db_conn.DBConn.__init__(self)
#
#     def new_order(
#         self, user_id: str, store_id: str, id_and_count: [(str, int)]
#     ) -> (int, str, str):
#         order_id = ""
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id) + (order_id,)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id) + (order_id,)
#             uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
#
#             for book_id, count in id_and_count:
#                 cursor = self.conn.execute(
#                     "SELECT book_id, stock_level, book_info FROM store "
#                     "WHERE store_id = %s AND book_id = %s;",
#                     (store_id, book_id),
#                 )
#                 row = cursor.fetchone()
#                 if row is None:
#                     return error.error_non_exist_book_id(book_id) + (order_id,)
#
#                 stock_level = row[1]
#                 book_info = row[2]
#                 book_info_json = json.loads(book_info)
#                 price = book_info_json.get("price")
#
#                 if stock_level < count:
#                     return error.error_stock_level_low(book_id) + (order_id,)
#
#                 cursor = self.conn.execute(
#                     "UPDATE store SET stock_level = stock_level - %s "
#                     "WHERE store_id = %s AND book_id = %s AND stock_level >= %s; ",
#                     (count, store_id, book_id, count),
#                 )
#                 if cursor.rowcount == 0:
#                     return error.error_stock_level_low(book_id) + (order_id,)
#
#                 self.conn.execute(
#                     "INSERT INTO new_order_detail(order_id, book_id, count, price) "
#                     "VALUES(%s, %s, %s, %s);",
#                     (uid, book_id, count, price),
#                 )
#
#             self.conn.execute(
#                 "INSERT INTO new_order(order_id, store_id, user_id) "
#                 "VALUES(%s, %s, %s);",
#                 (uid, store_id, user_id),
#             )
#             self.conn.commit()
#             order_id = uid
#         except psycopg2.Error as e:
#             logging.info("528, {}".format(str(e)))
#             return 528, "{}".format(str(e)), ""
#         except BaseException as e:
#             logging.info("530, {}".format(str(e)))
#             return 530, "{}".format(str(e)), ""
#
#         return 200, "ok", order_id
#
#     def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
#         conn = self.conn
#         try:
#             cursor = conn.execute(
#                 "SELECT order_id, user_id, store_id FROM new_order WHERE order_id = %s",
#                 (order_id,),
#             )
#             row = cursor.fetchone()
#             if row is None:
#                 return error.error_invalid_order_id(order_id)
#
#             order_id = row[0]
#             buyer_id = row[1]
#             store_id = row[2]
#
#             if buyer_id != user_id:
#                 return error.error_authorization_fail()
#
#             cursor = conn.execute(
#                 "SELECT balance, password FROM users WHERE user_id = %s;", (buyer_id,)
#             )
#             row = cursor.fetchone()
#             if row is None:
#                 return error.error_non_exist_user_id(buyer_id)
#             balance = row[0]
#             if password != row[1]:
#                 return error.error_authorization_fail()
#
#             cursor = conn.execute(
#                 "SELECT store_id, user_id FROM user_store WHERE store_id = %s;",
#                 (store_id,),
#             )
#             row = cursor.fetchone()
#             if row is None:
#                 return error.error_non_exist_store_id(store_id)
#
#             seller_id = row[1]
#
#             if not self.user_id_exist(seller_id):
#                 return error.error_non_exist_user_id(seller_id)
#
#             cursor = conn.execute(
#                 "SELECT book_id, count, price FROM new_order_detail WHERE order_id = %s;",
#                 (order_id,),
#             )
#             total_price = 0
#             for row in cursor:
#                 count = row[1]
#                 price = row[2]
#                 total_price = total_price + price * count
#
#             if balance < total_price:
#                 return error.error_not_sufficient_funds(order_id)
#
#             cursor = conn.execute(
#                 "UPDATE users SET balance = balance - %s"
#                 "WHERE user_id = %s AND balance >= %s",
#                 (total_price, buyer_id, total_price),
#             )
#             if cursor.rowcount == 0:
#                 return error.error_not_sufficient_funds(order_id)
#
#             cursor = conn.execute(
#                 "UPDATE users SET balance = balance + %s" "WHERE user_id = %s",
#                 (total_price, buyer_id),
#             )
#
#             if cursor.rowcount == 0:
#                 return error.error_non_exist_user_id(buyer_id)
#
#             cursor = conn.execute(
#                 "DELETE FROM new_order WHERE order_id = %s", (order_id,)
#             )
#             if cursor.rowcount == 0:
#                 return error.error_invalid_order_id(order_id)
#
#             cursor = conn.execute(
#                 "DELETE FROM new_order_detail WHERE order_id = %s", (order_id,)
#             )
#             if cursor.rowcount == 0:
#                 return error.error_invalid_order_id(order_id)
#
#             conn.commit()
#
#         except psycopg2.Error as e:
#             return 528, "{}".format(str(e))
#
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#
#         return 200, "ok"
#
#     def add_funds(self, user_id, password, add_value) -> (int, str):
#         try:
#             cursor = self.conn.execute(
#                 "SELECT password FROM users WHERE user_id = %s", (user_id,)
#             )
#             row = cursor.fetchone()
#             if row is None:
#                 return error.error_authorization_fail()
#
#             if row[0] != password:
#                 return error.error_authorization_fail()
#
#             cursor = self.conn.execute(
#                 "UPDATE users SET balance = balance + %s WHERE user_id = %s",
#                 (add_value, user_id),
#             )
#             if cursor.rowcount == 0:
#                 return error.error_non_exist_user_id(user_id)
#
#             self.conn.commit()
#         except psycopg2.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#
#         return 200, "ok"
