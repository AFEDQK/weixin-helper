import logging

import pymysql


class DataBaseHandle(object):
    """定义一个MySQL 操作类"""

    def __init__(self, host1, user1, password1, db1):
        self.db = pymysql.connect(host=host1,
                                  user=user1,  # 用户名
                                  password=password1,  # 密码
                                  db=db1)  # 选中的数据库
        self.cursor = self.db.cursor()

    def createDB(self, sql):
        try:
            print("执行过这里")
            self.cursor.execute(sql)
        except Exception as e:
            logging.info(f"创建数据表异常:{e}")
        finally:
            self.cursor.close()

    def insertDB(self, sql):
        try:
            num = self.cursor.execute(sql)
            print("插入条数为：", num)
            self.db.commit()
        except Exception as e:
            logging.info(f"插入数据失败：{e}")
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        try:
            num = self.cursor.execute(sql)
            print("删除条数为：", num)
            self.db.commit()
        except Exception as e:
            logging.info(f"Error: delete data error:{e}")
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDB(self, sql):
        try:
            num = self.cursor.execute(sql)
            print("更新条数为：", num)
            self.db.commit()
        except Exception as e:
            logging.info(f"Error: unable data error:{e}")
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDB(self, sql):
        try:
            num = self.cursor.execute(sql)
            # print("查询条数为：", num)
            data = self.cursor.fetchall()
            # print("查询的内容为：", data)
            return data, num
        except Exception as e:
            logging.info(f"Error: unable to fecth data:{e}")
        finally:
            self.cursor.close()

    def closeDB(self):
        self.db.close()
