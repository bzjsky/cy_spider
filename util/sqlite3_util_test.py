from util import cy_logger
from util.sqlite3_util import DBSqlite3

if __name__ == '__main__':
    sqlite = DBSqlite3("""
                    create table IF NOT EXISTS student(
                        customer VARCHAR(20),
                        produce VARCHAR(40),
                        amount FLOAT,
                        date DATE   
                    )
                    """)
    sqlite.execute("INSERT INTO student VALUES(?,?,?,?)",
                   [("zhangsan", "notepad", 999, "2017-01-02"), ("lishi", "binder", 3.45, "2017-04-05")])
    cy_logger.log(sqlite.fetchall("select * from student"))
