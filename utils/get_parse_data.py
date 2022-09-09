import json

from process_recruit_detail_info import extract_info
from process_job_info import handle_search
import re
from Check_inval import check
from extensions import config_loader
from database_test import DataBaseHandle

all_provinces = config_loader.load_region()
regex_config = config_loader.read_config()

"""
{'期望工作地点': [], '招工单位': [], '招工信息': [{'工种': '', '期望工作地点': '', '招工单位': [], '招工人数': '', 
'联系人': [], '联系电话': '15822775267'}], '联系人': '无', '联系电话': ['15822775267'], '联系微信': '无', 
'项目内容': '专业格栅;方通;矿棉板;'}
{'期望工作地点': '', '招工单位': [], '招工信息': [{'工种': ['吊顶'], '期望工作地点': '', '招工单位': [], 
'招工人数': [], '联系人': [], '联系电话': '15822775267'}], 
'联系人': '无', '联系电话': ['15822775267'], '联系微信': '无', '项目内容': '专业格栅;方通;矿棉板;'}
"""


def keyword_match(text):
    pattern = r'群发|换群|治疗|专业生产|购买|收购|办理|代发|劳务资质|听课|刷题|月返|全国通用' \
              r'价格低|学历提升|招商|包教包会|如有打扰|标准化资讯|直播|价优|交流学习|优惠名额|加盟|厂家直|分公司|总包|职称|资质' \
              r'|出：|出:|注册公司|安全员AC直出|收购劳务资质|汉硕佳酿|专业回收|批发|免费领取|定制|订做|定做|长期出|窗帘|装修|中标|铝单板|一手资源|承接|定期发布|消除企查查' \
              r'微蓝盒子|专业补录|业绩补录|电话联系厂家|茅台|免费邮寄样品|现货秒发|欢迎老板询价下单|专业考培各类证书|报名考证|实力解决通过率 |免配合| 免考|【微蓝盒子】|收；' \
              r'低价接单|极速出货|包邮|麦裙|智能群|收以下证书|收证书|收：|网络课程|在线网课|意向学员|协助报名|课程|生产厂家|预结算|图纸设计|标书制作|注册执照|代理记账|代开发票|住建厅八大员|周期短|价格低' \
              r'退休一级造价|八大员一次过|继续教育|股权质押|资产抵押|项目抵押|历史最低价|当天发货|国之重器|致富热线|让利|宣传|真心为你服务|漏水检测|启动资金|量大从优|公司过账|薄利多销|价格包你满意|出售|工商变更|工商注册' \
              r'4G流量卡|物联卡|全国发货|収藏永久看|每！日！福！利|全国秒发|安卓系统|速度快|价格合适|新旧设备分期融资|企业融资|贸易代采|欠条回收|长期换|项目直投|年利率|放款周期|走账|降负债 |成考|免试入学|测温设备管理系统|系统|代幵' \
              r'验后付款|周期快|马上截止报名|回收|三辊闸| 全网推广|授权抖音快手|专业年审|审车|效果图|各类证书|官网永久可查|唯一社保|二级房建|公司资金雄厚|服务项目|全国业绩补录 |车年审|全国求购|中介茶水丰厚|专业消防预算和报价|专业消防图纸设计出图盖章' \
              r'旋转吊篮|intel 酷睿i5处理器|靓机好货|全国包邮|补录|专业办证|建筑配件系列产品|投保电话|一站式采购|软过免考通道|软过免考|经销商|代理商|免费拆除|年租|感应门 地簧门|出山东建筑乙|做分期|回函|免费试用|封号|项目广告|出租！出租！|优惠多多 |瓷砖供应' \
              r'求包月|安许'
    p1 = re.compile(pattern)
    m1 = p1.findall(text)
    print("关键词匹配：", m1)
    if len(m1) != 0:
        return False
    else:
        return True


def cc_target(contact, city):
    if contact == "[]" or len(contact) == 0:
        contact_target = False
    else:
        contact_target = True
    if city == "[]" or len(city) == 0:
        city_target = False
    else:
        city_target = True
    if contact_target and city_target:
        return True
    else:
        return False


def handle_info(text):
    types, contact, city, res = check(text, None, None, None)
    formated_res = format_return_result(res)
    city = formated_res["期望工作地点"]
    print(types, contact, city)
    cnt = 0
    if types == "[]" or len(types) == 0:
        cnt += 1
    if cnt >= 1:
        old_target = False
    else:
        old_target = True

    add_target = cc_target(contact, city)

    new_target = keyword_match(text)
    print(old_target, new_target, add_target)
    if old_target and new_target and add_target:
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


def postprocess_working_place(working_place):
    if not working_place:
        return []
    new_working_place = []
    for item in working_place:
        if len(item) > 1:
            new_working_place.append(item)
    if len(new_working_place) == 1:
        if new_working_place[0] in all_provinces:
            return []
        else:
            return new_working_place
    else:
        return new_working_place


def format_return_result(res):
    formated_res = dict()
    working_place = to_list(res["期望工作地点"])
    # 处理单独省、市、区的情况，以及不正确的地址
    formated_res["期望工作地点"] = postprocess_working_place(working_place)
    #拍脑袋定的长度，后期修改
    recruit_company = to_list(res["招工单位"])
    if len(recruit_company) > 20:
        formated_res["招工单位"] = []
    else:
        formated_res["招工单位"] = recruit_company
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
    dataset = regex_config
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
