import pymysql
from be.model import db_conn
from be.model import error

class Search(db_conn.DBConn):
    def search_in_store(self, choose: int, store_id: str, keyword: str, page: int, limit: int):
        o=""
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (o,)

            choose = int(choose)
            page = int(page)
            limit = int(limit)
            skip_count = (page - 1) * limit

            result = []

            if choose == 0:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE store_id = %s AND JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (store_id, f"%{keyword}%", limit, skip_count))
            elif choose == 1:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE store_id = %s AND JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (store_id, f"%{keyword}%", limit, skip_count))
            elif choose == 2:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE store_id = %s AND JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (store_id, f"%{keyword}%", limit, skip_count))
            elif choose == 3:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE store_id = %s AND JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (store_id, f"%{keyword}%", limit, skip_count))

            result = []
            for row in self.cursor.fetchall():
                title, author, book_intro, content, tags = row
                book_data = {
                    "title": title,
                    "author": author,
                    "book_intro": book_intro,
                    "content": content,
                    "tags": tags.split(', ') if tags else []
                }
                result.append(book_data)

            return 200, "ok", result

        except pymysql.Error as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []

    def search_all(self, choose: int, keyword: str, page: int, limit: int):
        try:
            choose = int(choose)
            page = int(page)
            limit = int(limit)
            skip_count = (page - 1) * limit

            result = []

            if choose == 0:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (f"%{keyword}%", limit, skip_count))
            elif choose == 1:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (f"%{keyword}%", limit, skip_count))
            elif choose == 2:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (f"%{keyword}%", limit, skip_count))
            elif choose == 3:
                query = """
                    SELECT JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.title')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.author')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.content')),
                           JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.tags'))
                    FROM store
                    WHERE JSON_UNQUOTE(JSON_EXTRACT(book_info, '$.book_intro')) LIKE %s
                    LIMIT %s OFFSET %s
                """
                self.cursor.execute(query, (f"%{keyword}%", limit, skip_count))

            result = []
            for row in self.cursor.fetchall():
                title, author, book_intro, content, tags = row
                book_data = {
                    "title": title,
                    "author": author,
                    "book_intro": book_intro,
                    "content": content,
                    "tags": tags.split(', ') if tags else []
                }
                result.append(book_data)

            return 200, "ok", result

        except pymysql.Error as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []