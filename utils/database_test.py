import logging

import pymysql
import json
from extensions import config_loader
from extensions import DbHandle

regex_config = config_loader.read_config()


class DataBaseHandle(object):
    """定义一个MySQL 操作类"""

    def __init__(self, host1, user1, password1, db1):
        self.db = pymysql.connect(host=host1,
                                  user=user1,  # 用户名
                                  password=password1,  # 密码
                                  db=db1)  # 选中的数据库

    def createDB(self, sql):
        self.cursor = self.db.cursor()

        try:
            print("执行过这里")
            self.cursor.execute(sql)
        except:
            print('Error: unable to create table')
        finally:
            self.cursor.close()

    def insertDB(self, sql):
        self.cursor = self.db.cursor()
        try:
            num = self.cursor.execute(sql)
            print("插入条数为：", num)
            self.db.commit()
        except Exception as e:
            logging.info(f"插入失败：{e}")
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        self.cursor = self.db.cursor()

        try:
            num = self.cursor.execute(sql)
            print("删除条数为：", num)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDB(self, sql):
        self.cursor = self.db.cursor()

        try:
            num = self.cursor.execute(sql)
            print("更新条数为：", num)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDB(self, sql):
        self.cursor = self.db.cursor()

        try:
            num = self.cursor.execute(sql)
            # print("查询条数为：", num)
            data = self.cursor.fetchall()
            # print("查询的内容为：", data)
            return data, num
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def closeDB(self):
        self.db.close()


if __name__ == '__main__':
    mul_res = []
    describe = {"要求": "acquire", "工资及福利": "money", "工作时长": "work_time"}
    res = {"工种": "types", "期望工作城市": "city", "招工地点": "place", "招工人数": "number", "联系人": "无", "联系电话": "contact",
           "联系微信": "无",
           "项目描述": "describe"}
    mul_res.append(res)
    # print(json.dumps(mul_res,ensure_ascii=False))
    json_data = json.dumps(mul_res, ensure_ascii=False)
    # print(json_data)
    DbHandle.insertDB("insert into json_test (json_data) values (' + json_data + ')")
