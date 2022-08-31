import pymysql
import json
from extensions import config_loader

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
        except:
            print("插入失败")
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
            # for row in data:
            #     id = row[0]
            #     comment = row[1]
            #     transform = row[2]
            #     print('music_id = %s, comment = %s, transform= %s' % (sid, name, transform))
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    def closeDB(self):
        self.db.close()


def read_database():
    dataset = regex_config
    for x, y in dataset.items():
        if x == "host":
            host1 = y
        elif x == "user":
            user1 = y
        elif x == "password":
            password1 = y
        elif x == "db":
            db1 = y

    return host1, user1, password1, db1


if __name__ == '__main__':
    content = read_database()
    dataset = regex_config
    for x, y in dataset.items():
        if x == "host":
            host1 = y
        elif x == "user":
            user1 = y
        elif x == "password":
            password1 = y
        else:
            db1 = y
    DbHandle = DataBaseHandle(host1, user1, password1, db1)
    # json_data, json_num = DbHandle.selectDB('select * from account')
    # print(json_data)
    mul_res = []
    describe = {"要求": "acquire", "工资及福利": "money", "工作时长": "work_time"}
    res = {"工种": "types", "期望工作城市": "city", "招工地点": "place", "招工人数": "number", "联系人": "无", "联系电话": "contact",
           "联系微信": "无",
           "项目描述": "describe"}
    mul_res.append(res)
    # print(json.dumps(mul_res,ensure_ascii=False))  # 有层次感
    json_data = json.dumps(mul_res, ensure_ascii=False)
    # print(json_data)
    DbHandle.insertDB("insert into json_test (json_data) values (' + json_data + ')")
# DbHandle.insertDB('insert into account (username, balance) values ("%s", "%s")' % ("Zmm", "8888"))
#     DbHandle.insertDB('insert into json_test (json_data) values ("%s")' % ("""[
#     {
#         "工种": [
#             [
#                 "电工"
#             ]
#         ],
#         "期望工作城市": [
#             [
#                 "苏州",
#                 "相城区"
#             ]
#         ],
#         "招工地点": [
#             []
#         ],
#         "招工人数": [
#             []
#         ],
#         "联系人": "无",
#         "联系电话": [
#             [
#                 [
#                     "18998990079"
#                 ]
#             ]
#         ],
#         "联系微信": "无",
#         "项目描述": {
#             "要求": [
#                 []
#             ],
#             "工资及福利": [
#                 []
#             ],
#             "工作时长": [
#                 [
#                     " 2022年6月2-7日 "
#                 ]
#             ]
#         }
#     }
# ]
#
# """))


# DbHandle.insertDB('insert into music (music_id, COMMENTS, DETAILS) values ("%s", "%s", "%s")' % ("001", "你好", "Hello"))
# DbHandle.deleteDB('delete from message where music_id = %s' % ("001"))
# DbHandle.updateDB('update music set COMMENTS = "%s" where DETAILS = "%s"' % ("只要一点点", "Hello"))
# raw_message, raw_num = DbHandle.selectDB('select mes_raw from message')
# print(raw_message, raw_num)
# if raw_num == 0:
#     print("目前数据库无数据，可直接插入")
# for item in raw_message:
#     str = ''.join(item)
# print(type(str))
