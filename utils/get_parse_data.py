import json

from process_recruit_detail_info import extract_info
from process_job_info import handle_search
import re
from Check_inval import check
from database_test import *

"""
{'期望工作地点': [], '招工单位': [], '招工信息': [{'工种': '', '期望工作地点': '', '招工单位': [], '招工人数': '', 
'联系人': [], '联系电话': '15822775267'}], '联系人': '无', '联系电话': ['15822775267'], '联系微信': '无', 
'项目内容': '专业格栅;方通;矿棉板;'}
{'期望工作地点': '', '招工单位': [], '招工信息': [{'工种': ['吊顶'], '期望工作地点': '', '招工单位': [], 
'招工人数': [], '联系人': [], '联系电话': '15822775267'}], 
'联系人': '无', '联系电话': ['15822775267'], '联系微信': '无', '项目内容': '专业格栅;方通;矿棉板;'}
"""

def keyword_match(text):
    pattern = r'长期合作|群发|换群|治疗|专业生产|购买|收购|办理|代发|劳务资质|听课|刷题|月返|全国通用' \
              r'价格低|学历提升|招商|包教包会|如有打扰|标准化资讯|直播|价优|交流学习|优惠名额|加盟|厂家直|分公司|总包|职称|资质' \
              r'|收：|收:|出：|出:|注册公司|安全员AC直出|收购劳务资质|汉硕佳酿|专业回收|批发|免费领取|定制|订做|定做|长期出|窗帘|装修|中标|铝单板|一手资源|承接|承包|定期发布'
    p1 = re.compile(pattern)
    m1 = p1.findall(text)
    print("关键词匹配：", m1)
    if len(m1) != 0:
        return False
    else:
        return True


def handle_info(text):
    types, contact = check(text, None, None, None)
    # print(types)
    cnt = 0
    if types == "[]" or len(types) == 0:
        cnt += 1
    if cnt >= 1:
        old_target = False
    else:
        old_target = True

    new_target = keyword_match(text)
    print(old_target, new_target)
    if old_target and new_target:
        return True
    else:
        return False


def to_str(item):
    if type(item) == str:
        return item
    else:
        if not item:
            return ""
        return "".join(item)


def to_list(item):
    if type(item) == list:
        return item
    else:
        if not item:
            return []
        return [item]


def format_return_result(res):
    formated_res = dict()
    formated_res["期望工作地点"] = to_list(res["期望工作地点"])
    formated_res["招工单位"] = to_list(res["招工单位"])
    recruit_infos = res["招工信息"]
    formated_res["联系人"] = to_str(res["联系人"])
    formated_res["联系电话"] = to_list(res["联系电话"])
    formated_res["联系微信"] = to_str(res["联系微信"])
    formated_res["项目内容"] = res["项目内容"]
    new_recruit_info = []
    for each_info in recruit_infos:
        info_dict = dict()
        info_dict["工种"] = to_str(each_info["工种"])
        info_dict["期望工作地点"] = to_str(each_info["期望工作地点"])
        info_dict["招工单位"] = to_list(each_info["招工单位"])
        info_dict["招工人数"] = to_str(each_info["招工人数"])
        info_dict["联系人"] = to_list(each_info["联系人"])
        info_dict["联系电话"] = to_str(each_info["联系电话"])
        new_recruit_info.append(info_dict)
    formated_res["招工信息"] = new_recruit_info
    return formated_res


def seg_punc(msg, wxid, raw, time):
    pattern = r'\n|\t|:|：|,|，| |!|！|\n'
    if not isinstance(msg, str):
        return {}
    result = re.split(pattern, msg)
    res, types, number, city, place, contact = extract_info(msg, wxid, raw, time)
    for i in range(len(result)):
        for j in range(len(types)):
            p1 = re.compile(types[j])
            m = p1.findall(result[i])
            if len(m) != 0:
                result[i] = ""
        for j in range(len(number)):
            p1 = re.compile(number[j])
            m = p1.findall(result[i])
            if len(m) != 0:
                result[i] = ""
        for j in range(len(city)):
            p1 = re.compile(city[j])
            m = p1.findall(result[i])
            if len(m) != 0:
                result[i] = ""

        for j in range(len(place)):
            p1 = re.compile(place[j])
            m = p1.findall(result[i])
            # print("招工单位匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("招工单位匹配成功，以用空格替换")
        for j in range(len(contact)):
            p1 = re.compile(contact[j])
            m = p1.findall(result[i])
            # print("联系电话匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("联系电话匹配成功，以用空格替换")

        p1 = re.compile("联系电话|报名电话|电话")
        m = p1.findall(result[i])
        # print(m)
        if len(m) != 0:
            result[i] = ""
            # print("匹配到")

    qa_sentence = ""
    for i in range(len(result)):
        # print(result[i])
        if len(result[i]) != 0:
            qa_sentence += result[i]
            qa_sentence += ";"
        # print(qa_sentence)
        # if i == len(result) - 1:
        #     qa_sentence += "。"
    # print(qa_sentence)
    res['项目内容'] = qa_sentence
    formated_res = format_return_result(res)
    # print(formated_res)
    configuration = json.dumps(formated_res, ensure_ascii=False)
    save_splice_info(configuration, wxid, raw, time)
    return formated_res


def find_job(msg):
    pattern = r'\n|\t|:|：|,|，| |!|！|\n'
    if not isinstance(msg, str):
        return {}
    result = re.split(pattern, msg)
    res, person, city, types, contact = handle_search(msg)
    # types = "你好"
    # print(len(types))
    print(result)
    for i in range(len(result)):
        # print("测试", i, "：", result[i])
        for j in range(len(person)):
            # print(types[j])
            p1 = re.compile(person[j])
            m = p1.findall(result[i])
            # print("工种匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("工种匹配成功，以用空格替换")
                # print("工种为：", types[j])
        for j in range(len(city)):
            p1 = re.compile(city[j])
            m = p1.findall(result[i])
            # print("人数匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("人数成功，以用空格替换")
        for j in range(len(types)):
            p1 = re.compile(types[j])
            m = p1.findall(result[i])
            # print("期望工作地点匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("期望工作地点匹配成功，以用空格替换")
        for j in range(len(contact)):
            p1 = re.compile(contact[j])
            m = p1.findall(result[i])
            # print("招工单位匹配：", m)
            if len(m) != 0:
                result[i] = ""
                # print("招工单位匹配成功，以用空格替换")

        p1 = re.compile("联系电话|报名电话|电话")
        m = p1.findall(result[i])
        # print(m)
        if len(m) != 0:
            result[i] = ""
            # print("匹配到")

    qa_sentence = ""
    for i in range(len(result)):
        # print(result[i])
        if len(result[i]) != 0:
            qa_sentence += result[i]
            qa_sentence += ";"
        # print(qa_sentence)
        # if i == len(result) - 1:
        #     qa_sentence += "。"
    # print(qa_sentence)
    res["项目内容"] = qa_sentence
    formated_res = format_return_result(res)
    return formated_res

def save_splice_info(res, wxid, raw, time):
    dataset = read_config()
    # print("标记")
    for x, y in dataset.items():
        if x == "host":
            host1 = y
        elif x == "user":
            user1 = y
        elif x == "password":
            password1 = y
        elif x == "db":
            db1 = y
    DbHandle = DataBaseHandle(host1, user1, password1, db1)
    DbHandle.insertDB("insert into recruit (mes_from, mes_raw, mes_time, mes_json) values ('%s', '%s', '%s', '%s')" % (
        wxid, raw, time, res))
    # raw_message, raw_num = DbHandle.selectDB('select mes_json from recruit')
    # print("抽取结果：", raw_message[0])
    # print("双引号结果：", json.dumps(raw_message[0], indent=4, ensure_ascii=False))

