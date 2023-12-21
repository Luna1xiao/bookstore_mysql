import pymysql
from be.model import error
from be.model import db_conn

import logging
class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    # def add_book(
    #     self,
    #     user_id: str,
    #     store_id: str,
    #     book_id: str,
    #     book_json_str: str,
    #     stock_level: int,
    # ):
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id)
    #         if not self.store_id_exist(store_id):
    #             return error.error_non_exist_store_id(store_id)
    #         if self.book_id_exist(store_id, book_id):
    #             return error.error_exist_book_id(book_id)
    #
    #         self.cursor.execute(
    #             "INSERT INTO store(store_id, book_id, book_info, stock_level)"
    #             "VALUES (%s, %s, %s, %s)",
    #             (store_id, book_id, book_json_str, stock_level),
    #         )
    #         self.cursor.connection.commit()
    #     except pymysql.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         return 530, "{}".format(str(e))
    #     return 200, "ok"
    def add_book(
            self,
            user_id: str,
            store_id: str,
            book_id: str,
            book_json_str: str,
            stock_level: int,
    ):
        try:
            # Check if user, store, and book exist
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)
            insert_query = ("INSERT INTO store (store_id, book_id, book_info, stock_level) ""VALUES (%s, %s, %s, %s)")
            values = (store_id, book_id, book_json_str, stock_level)
            self.cursor.execute(insert_query, values)
            self.cursor.connection.commit()

        except pymysql.Error as e:
            # Handle database errors
            return 528, "{}".format(str(e))

        except BaseException as e:
            # Handle other unexpected errors
            return 530, "{}".format(str(e))

        # Return success response
        return 200, "ok"

    # def add_stock_level(
    #     self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    # ):
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id)
    #         if not self.store_id_exist(store_id):
    #             return error.error_non_exist_store_id(store_id)
    #         if not self.book_id_exist(store_id, book_id):
    #             return error.error_non_exist_book_id(book_id)
    #
    #         self.cursor.execute(
    #             "UPDATE store SET stock_level = stock_level + %s "
    #             "WHERE store_id = %s AND book_id = %s",
    #             (add_stock_level, store_id, book_id),
    #         )
    #         self.cursor.connection.commit()
    #     except pymysql.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         return 530, "{}".format(str(e))
    #     return 200, "ok"
    def add_stock_level(
            self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            # Check if user, store, and book exist
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            # Update stock level in the store
            update_query =( "UPDATE store SET stock_level = stock_level + %s ""WHERE store_id = %s AND book_id = %s")

            self.cursor.execute(update_query, (add_stock_level, store_id, book_id))
            affected_rows = self.cursor.rowcount

            # Check if the update was successful


            # Commit the changes to the database
            self.cursor.connection.commit()


        except pymysql.Error as e:
            # Handle other database errors
            return 528, "{}".format(str(e))

        except BaseException as e:
            # Handle other unexpected errors
            return 530, "{}".format(str(e))

        # Return success response
        return 200, "ok"

    # def create_store(self, user_id: str, store_id: str) -> (int, str):
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id)
    #         if self.store_id_exist(store_id):
    #             return error.error_exist_store_id(store_id)
    #         self.cursor.execute(
    #             "INSERT into user_store(store_id, user_id)" "VALUES (%s, %s)",
    #             (store_id, user_id),
    #         )
    #         self.cursor.connection.commit()
    #     except pymysql.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         return 530, "{}".format(str(e))
    #     return 200, "ok"
    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            # Check if the user exists
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)

            # Check if the store already exists
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            # Create a new store for the user
            insert_query = "INSERT INTO user_store (store_id, user_id) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (store_id, user_id))

            # Commit the changes to the database
            self.cursor.connection.commit()

        except pymysql.Error as e:
            # Handle database errors
            return 528, "{}".format(str(e))

        except BaseException as e:
            # Handle other unexpected errors
            return 530, "{}".format(str(e))

        # Return success response
        return 200, "ok"

    def send_books(self, store_id: str, order_id: str) -> (int, str):
        try:
            # Check if the store exists
            self.cursor.execute("SELECT * FROM store WHERE store_id = %s", (store_id,))
            if not self.cursor.fetchone():
                return error.error_non_exist_store_id(store_id)

            # Update the order status to 3 (assuming 3 represents "sent")
            self.cursor.execute("SELECT * FROM history_order WHERE order_id = %s", (order_id,))
            order = self.cursor.fetchone()

            if not order:
                return error.error_invalid_order_id(order_id)

            order_status = order[3]  # Assuming status is at index 3

            if order_status != 2:
                return 500, "Invalid order status"

            # Update the order status to 3 (assuming 3 represents "sent")
            self.cursor.execute(
                "UPDATE history_order SET status = %s WHERE order_id = %s",
                (3, order_id)
            )
            self.cursor.connection.commit()

        except pymysql.Error as e:
            logging.error("MySQL Error: {}".format(str(e)))
            return 500, "Internal Server Error"

        return 200, "ok"