# -*- coding: utf-8 -*-
import sqlite3

from util import cy_logger


class DBSqlite3:

    def __init__(self, create_table_sql):
        self.db = "../db/spider.db"
        sqlite3.connect(self.db).execute(create_table_sql)
        cy_logger.log("DBSqlite3 init")

    def get_connection(self):
        return sqlite3.connect(self.db)

    def execute(self, sql, params):
        if type(params) == list and len(params) == 0:
            return
        connection = self.get_connection()
        try:
            # 执行sql语句
            if type(params) == list:
                connection.executemany(sql, params)
            else:
                connection.execute(sql, params)
            connection.commit()
            cy_logger.log("executes successfully")
        except Exception as e:
            cy_logger.error(str(e))
            # 发生错误时回滚
            connection.rollback()
        finally:
            # 关闭数据库连接
            connection.close()

    def fetchall(self, sql):
        # 使用cursor()方法获取操作游标
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            return cursor.fetchall()
        except Exception as e:
            cy_logger.error(e)
        finally:
            # 关闭数据库连接
            connection.close()

    def fetchone(self, sql):
        # 使用cursor()方法获取操作游标
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取单条数据
            return cursor.fetchone()
        except Exception as e:
            cy_logger.error(e)
        finally:
            # 关闭数据库连接
            connection.close()

    def select_rows_paper(self, sql, param=None, page_no=1, page_size=20):
        """
        分页查询
        """
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                if param:
                    sql = sql + '%s' % param

                cursor.execute("SELECT COUNT(1) FROM (%s) tmp" % sql)
                total = cursor.fetchall()[0][0]
                pages = 0
                rows = []
                if total > 0:
                    # 总页数
                    pages = int(total / page_size) if total % page_size == 0 else int(total / page_size) + 1

                    if page_no > pages:
                        page_no = pages
                    offset = (page_no - 1) * page_size  # 偏移量
                    sql = sql + ' LIMIT %s, %s' % (offset, page_size)
                    cy_logger.log(sql)
                    cursor.execute(sql)
                    rows = cursor.fetchall()

                return {'total': total, 'page_no': page_no, 'pages': pages, 'rows': rows}
        except Exception as e:
            cy_logger.error(e)
        finally:
            connection.close()
