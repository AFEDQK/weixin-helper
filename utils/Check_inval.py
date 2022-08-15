# import re
# encoding:UTF-8
import regex as re
import json
import re as r
import json
from LAC import LAC
import sys
sys.path.append('../database/')
# from database_test import *
import re as re2
# 装载LAC模型
lac = LAC(mode='lac')

def read_config():
    """"读取配置"""
    with open("re_config.json", encoding='UTF-8') as json_file:
        config = json.load(json_file)
    return config


def update_config(config):
    """"更新配置"""
    with open("config.json", 'w') as json_file:
        json.dump(config, json_file, indent=4)
    return None

def getTypes(msg):
    types_text = [ "信号工|一开一指挥|塔司|普焊|升降机工人|索工|司机|货梯司机|一司两指|木工|技术主管|普通工人|大龄工|快递|分拣员|下料工|岩棉|绑扎师傅|中工|拖石膏工人|擦色师父|外护工|下吊绳师傅|支模师傅|收口师傅|接线工|管工|铺砖师傅|社会工|暑假工|木模师傅|铝膜工|钢构老师|水工|氩弧焊|冷做工|辅助工|派遣工|外包|正式工|检验员|注塑|售后客服|线检|差价工|技术员|小时工|日结工|女工|流水线|整机装配|跟单管理员|长期小时工|作业员|功能测试|包装|插件|骑手|顺丰快递|男工|学生工|熟练工|生产技工|检查员|女工|冷作|二保焊|打砂工|喷涂工|大工|测试工|手焊|气保焊|单道焊|手把焊|埋弧焊|制芯工人|冷芯工学|修整工|升降机司机|电梯司机|升降机驾驶员|施工电梯|单指挥|管道二保焊工|通风安装工|消防通风大工|铁皮师傅|地砖师傅|内粉师傅|内保温师傅|木工班组|拆模班组|油工|消防水工|钢筋班组|后台大工|木模工|打板团队|水电师傅|起重机司机|库房管理|通风小工|消防水班组|消防电工|钢筋制作师傅|井架司机|货梯机手|信工|检验员|通风安装工|主管|配菜",
        "塔吊司机|瓦工|砌筑|贴砖|抹灰", "建筑木工|铝模|二次结构", "钢筋工|翻样|后台", "架子工|架工|爬架", "电工|水电工", "水暖工|安装工|管道|通风", "钢结构|网架|不锈钢",
                  "焊工|钳工|铆工|钣金", "普工|小工|杂工|力工", "混凝土工|砼工", "吊装工|装配式建筑|构件安装", "防水工", "弱电|安防|消防", "建筑信息模型",
                  "装修木工|吊顶|木地板", "家具木工|制作|安装|全屋定制", "油漆|涂料|大白|墙纸", "幕墙工|玻璃|石材|门窗", "外墙|保温|吊篮", "打胶|美缝", "地坪|混凝土地坪",
                  "地暖", "工地清洁|开荒|保洁", "敲墙|开孔|拆除|切割工", "机械操作|机械安装", "机修|维修", "塔吊|吊车|指挥", "人货电梯|升降机司机", "挖机|推土机|压路机",
                  "货车|运输车|渣土车", "叉车|铲车|装载机", "罐车|泵车司机", "其他司机", "设备安装|维护", "建造师", "施工员", "质量员", "安全员", "材料员", "实验员|取样员",
                  "技术负责人|项目总工", "资料员|内业", "造价|预算", "成本会计", "测绘", "工长", "监理", "实习生", "项目经理|建造师", "库管员", "道路|公路|铁路",
                  "桥梁", "隧道|涵洞", "护坡|边坡", "爆破", "园林|绿化", "古建筑", "市政|管网", "亮化|照明", "地基|挖桩|破桩", "加固|防护", "土石方", "工厂普工",
                  "产线技术员", "操作工|车工|铣工", "注塑工", "挡车工", "工石焊工|锡焊", "装配工|组装工", "鞋厂|箱包", "服装厂招工", "印刷厂招工", "纺织|细纱|印花",
                  "针车|缝纫工|裁床", "质检|品检|调试", "煤矿|窑厂", "铸造工|钻床|冲压", "生产主管|经理|调度", "电镀工", "打磨|抛光|喷漆", "裁翦工", "包装工",
                  "跟单员|仓管|发货", "研发|编程|产品设计", "产品测试员", "电气工程师|CNC", "学徒工", "工厂电工|电路维护", "调色师|烫工", "物流|运输|装车|卸货",
                  "保安|门卫|看护", "会计|出纳|记帐|记录员", "新媒体|拍摄|直播", "汽修|汽配", "喷绘|广告", "兼职|日结|临时工", "教师|教员", "文员|行政|商务",
                  "其它各类招工", "建筑电工", "普工", "豇", "叉车工", "铆工", "电工小工或焊工小工", "混凝土工保安瓦工工厂普工", "钢筋工后台制作", "专业架子工", "钢结构网架安装",
                  "隔墙板", "班组", "普工，", "我想找一份开车的工作", "吊车司机", "铝模工", "模板工", "木工装修，吊顶隔断", "货运司机", "驾驶员", "保安", "吊车指挥",
                  "危险品押运员", "货物运输", "外墙涂料真石漆", "贴砖，砌墙", "架子工", "制衣车工", "铲车，叉车", "保安和者叉车", "钢筋工", "厨师", "拆架子拆木", "专职司机",
                  "C1驾照司机", "专业抹楼梯踏步", "装车，分拣", "电焊和气割", "净化车间", "净化板安装", "殡仪馆", "安装玻璃隔断", "打胶", "玻璃门等等", "门窗等等", "司马",
                  "烫衣服大烫", "开孔", "钻孔", "服务", "打磨工", "装卸工", "倒混泥土", "剃凿打磨", "水钻钻孔", "二保电焊工", "手工活外发", "家具维修师",
                  "后厨小时工", "想找火葬场工作", "刮大白刷乳胶漆", "幕墙工", "油漆，刮原子灰，喷漆", "水磨石固化地平", "铲车司机！电焊工", "c1照4米2以下可开", "吊车"
                 ]
    #十人   30到50人 四个 五六个 5—7人 1到2人 8九个人 shi ming shiwu ming 一个工管住不管吃 一个礼拜 一个班
    #算0.5个工 不要暑期工 暑假工不要 物流仓库 28个班 热水空调 汽车玻璃 服务费20 威特电梯 8个通层
    text=''
    for t in types_text:
        text=text+"|"+t
    types = []

    tmp = re.findall(text, msg)

    # print('ty=',tmp)
    for t in tmp:
        if t != None and len(t)>0 and  t not in types:
            types.append(t)
    # print('types=', types)
    return types



regex_number = ''
regex_place = ''
regex_money = ''
regex_time = ''
regex_content = ''
regex_title = ''
regex_acquire = ''
regex_city = ''
regex_type = ''
regex_contact = ''
def getORGName(str_content):
    text = str_content
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    res = []
    for item in resdict.items():
        if str(item[1]) == 'ORG':
            res.append(item[0])
    return res

def getLOCName(str_content):
    text = str_content
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    # print(resdict)
    res = []
    for item in resdict.items():
        if str(item[1]) == 'LOC' :
            res.append(item[0])
    return res

def getMNumber(str_content):
    text = str_content
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    # print(resdict)
    res = []
    for item in resdict.items():
        mystr=str(item[0]).replace('\n','').replace(' ','')
        if (str(item[1]) == 'm' or str(item[1]) == 'n') and len(mystr)==11 and mystr.isdigit():
            res.append(mystr)
    return res



def getAllMsg(content,data_original):

    place = []
    if len(place) == 0:
        tmp = getORGName(data_original)
        res = []
        for i in range(0, len(tmp)):
            if tmp[i] != '微信' and tmp[i] != '微信电话' and tmp[i] not in res:
                res.append(tmp[i])
        place = res
    if (len(place) > 3):
        # place = place[0]
        place = get_special_content(regex_place, content)

    # 地点
    # city = get_special_content(regex_place, content)
    city=''
    if len(city) == 0:
        tmp = getLOCName(data_original)
        res = []
        for i in range(0, len(tmp)):
            if tmp[i] not in res:
                res.append(tmp[i])
        city = res
    if len(city) == 0:
        # 按配置找城市
        city = re.findall(regex_city, content);
        city = list(set(city))
        city = ",".join(city);
    # 薪资待遇
    money = get_special_content(regex_money, content)

    contact = getMNumber(content)


    # 招工内容
    text = get_special_content(regex_content, content)
    # 工作时长
    work_time = get_special_content(regex_time, content)
    # 要求
    acquire = get_special_content(regex_acquire, content)
    # 人数
    number = re.findall('\d+人|\d+名|数名|大量|若干|\d+个|\d+人|多名|若干个|几个|\d+—\d+人|\d+到\d+人|\d+位', content)
    # if len(number)==0:
    #     number = re.findall('\d+名', content)
    # if len(number) == 0:
    #     number = re.findall('数名', content)
    # if len(number) == 0:
    #     number = re.findall('\d+个', content)
    # if len(number)==0:
    #     number = re.findall('\d+人', data_original)
    # if len(number) == 0:
    #     number = re.findall('\d+名', data_original)
    # if len(number) == 0:
    #     number = re.findall('数名|多名', data_original)
    # if len(number) == 0:
    #     number = re.findall('\d+个', data_original)



    # 招聘类型
    types= getTypes(content)
    # types = get_special_content(regex_title, content.replace('招聘装配工','装配工'))
    # print('刚开始=',types)
    # print(content)
    # if (len(types) == 0):
    #     # regex = '(?<=)([电|力|焊|普|操作|男|装卸|女|钳|铆|木|钢筋|小|管|氩电焊|起重|汽车|履带|保].{0,5}[实习生|工|工程师|吊|运|焊])';
    #     regex = '(?<=)([电|力|焊|普|男|装卸|女|钳|铆|木|钢筋|小|管|氩电焊|起重|汽车|履带|保|装|打].{0,4}[实习生|工|工程师|吊|运|焊])';
    #     tmp = re.findall(regex, content.replace('工厂','厂子'));
    #     print('tmp=',tmp)
    #     res = []
    #     for item in tmp:
    #         if item != '工' and item!='.' and '，' not in item :  # and item not in res
    #             res.append(item.replace('工 工', '工').replace('，工',''))
    #     types = res
    #     print('a=',types)
    # #特殊的工作：电话客服，快递员
    # regex = '塔吊指挥|电话客服|快递员|指挥男|电梯司机|信号工|司机|指挥|施工员|测量员|电梯操作工|操作工|主管|厨师|配菜师傅|服务员';
    # tmp = re.findall(regex, content)
    # # res = []
    # # for item in tmp:
    # #     if item != '工' and item != '.':
    # #         res.append(item.replace('工 工', '工'))
    #
    # if len(types)==0:
    #     types=tmp
    # # 处理 工种包含数字
    # for i in range(0, len(types)):
    #     # 处理  "工种": "小时工17元/小",
    #     find = re.findall('\d+', types[i])
    #     for j in range(0, len(find)):
    #         if find[j] in types[i]:
    #             idx = types[i].index(find[j])
    #             if idx != 0:
    #                 types[i] = types[i][:idx]
    #     tmp = types[i]
    #     for j in range(0, len(number)):
    #         tmp = tmp.replace(number[j], '')
    #         types[i] = tmp
    # for t in types:
    #     if t in res:
    #         types = res
    #         break
    #
    # if (len(types) == 0):
    #     types = text
    #
    # #新增 工种：急需
    # forward_text="急需"
    # backward_text='。|！|，'
    # regex_concat = '(?<=' + forward_text + ').*?(?=' + backward_text + '|～～|！|其它：)'
    # new_type= re.findall(regex_concat, content)
    # if len(types)==0:
    #     types=''.join(new_type)

    #新增 工资
    pattern = re.compile('[,。！][^,。！]*工资[^,。！]*[,。！]')
    str1=pattern.search(content)
    if str1!=None and len(money)==0:
        start,end=str1.span()
        money = content[start+1:end]
    #新增 年龄要求
    str1 = re.findall('男\d+岁以下|女\d+岁以下|\d+-\d+岁|\d+到\d+岁|\d+-\d+周岁|\d+岁以下|\d+周岁以下|'
                      '女\d+左右|男\d+岁|女不超过\d+岁|男不超过\d+岁|女不超过\d+|男不超过\d+', content)
    if str1!= None and len(acquire) == 0:
        acquire = str1
    str1 = re.findall('(?<=)([男|女].{0,5}以下)', content)
    if str1 != None and len(acquire) == 0:
        acquire = str1
    str1 = re.findall('男\d+岁以下|女\d+岁以下|\d+-\d+岁|\d+到\d+岁|\d+-\d+周岁|\d+岁以下|\d+周岁以下|'
                      '女\d+左右|男\d+岁|女不超过\d+岁|男不超过\d+岁|女不超过\d+|男不超过\d+', data_original)
    if str1 != None and len(acquire) == 0:
        acquire = str1


    # 新增 价格25
    regex = '(?<=)(价格\d+)';
    tmp = re.findall(regex, content)
    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace('，', '').replace('。', '')
    if len(money) == 0 and tmp != None:
        money = tmp
    # 新增 价格 ：单价36-40元，单价38
    regex = '(?<=)([价|格].*?[元|，|。])';
    tmp = re.findall(regex, content)
    for i in range(0,len(tmp)):
        tmp[i]=tmp[i].replace('，','').replace('。','')
    if len(money)==0 and tmp!=None:
        money=tmp
    # 新增 价格 ：36-40元
    regex = '\d+每个月|浙江证\d+|外地证\d+|没有证：\d+|\d+加班\d+|\d+－\d+元|\d+-\d+元|\d+～\d+元|\d+--\d+元|\d+一个月|加班\d+|\d+/\d+|\d+加\d+|\d++\d+|6000+20'
    tmp = re.findall(regex, content.replace('O','0'))

    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace('，', '').replace('。', '')
    if len(money) == 0 and tmp != None:
        money = tmp
    regex='(?<=)(，.{0,5}[外地证|省内证|省外证].{0,5}[，|\d++\d+]|[外地证|省内证|省外证].{0,5}[，|\d++\d+])'
    tmp = re.findall(regex, content.replace('O', '0'))

    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace('，', '').replace('。', '')
    if len(money) == 0 and tmp != None:
        money = tmp

    # 新增 要求：有xx证
    regex = '(?<=)([外|有|官|要|必须|只要|能|省|浙].{0,5}[证|经验|性|苦|书|件|查]|[要|必须|只要].{0,3}[女|男]|现在在.*?，|.{0,3}疫苗.{0,5}，)';
    tmp = re.findall(regex, content)

    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace('，', '').replace('。', '')
    if len(acquire) == 0 and tmp != None and acquire!=tmp:
        acquire = tmp

    if len(acquire)==1 and type(acquire)==list and acquire!=tmp :
        for i in range(0,min(len(tmp),len(acquire))):
            if str(tmp[i]) not in acquire[i] and  "要求" not in str(tmp[i]):
                acquire[i] = str(acquire[i]) + " " + str(tmp[i])
        if len(tmp)>len(acquire) and len(acquire)==1 and type(acquire)==list:
            for j in range(len(acquire),len(tmp)):
                acquire[0]= str(acquire[0]) + " " + str(tmp[j])
    # 新增 福利 ：免费xx,包xx，
    regex = '(?<=)([免|包|提|宿|可].{2,7}[，|。|饭]|加班.{0,3}多|压一付一|月清|加班.{0,3}，|包.{0,5}[住|吃]|管.{0,7}[住|吃])';
    tmp = re.findall(regex, content)
    for i in range(0, len(tmp)):
        tmp[i] = tmp[i].replace('，', '').replace('。', '')
    if tmp != None and len(tmp)!=0 and len(money)==1:
        for t in tmp:
            if t not in money[0]:
                # print(t)
                money[0]=money[0]+','+t
    if len(money)==0 and tmp != None:
        money=tmp
    #如果工种比 工资数量多太多就额外切分检索工资

    if len(types)-len(money)>3:
        money_all=[]
        content1=content.replace('\n','')
        for i in range(0,len(types)):
            if i<len(types)-1:
                sentence=re.findall(types[i]+'.*?'+types[i+1],content1)
            else:
                sentence = re.findall(types[i] + '.*?<end>', content1)
            sentence=''.join(sentence)

            # 新增 价格 ：单价36-40元，单价38
            money_t=[]
            regex = '(?<=)([单价|价格].*?[元|，|。])';
            tmp = re.findall(regex, sentence)
            for i in range(0, len(tmp)):
                tmp[i] = tmp[i].replace('，', '').replace('。', '')
            if len(money_t) == 0 and tmp != None:
                money_t = tmp
            # 新增 价格 ：36-40元
            regex = '外地证\d+|没有证：\d+|\d+－\d+元|\d+-\d+元|\d+～\d+元|\d+--\d+元|\d+一个月|加班\d+|\d+/\d+';
            tmp = re.findall(regex, sentence)
            for i in range(0, len(tmp)):
                tmp[i] = tmp[i].replace('，', '').replace('。', '')
            if len(money_t) == 0 and tmp != None:
                money_t = tmp
            # 新增 价格 ：xx元
            regex = '\d+元';
            tmp = re.findall(regex, sentence)
            for i in range(0, len(tmp)):
                tmp[i] = tmp[i].replace('，', '').replace('。', '')
            if len(money_t) == 0 and tmp != None:
                money_t = tmp
            if len(money_t) != 0 :
                money_all.append(money_t)
            else:
                money_all.append('')
            money=money_all

    persons=getPERName(content)
    # print(persons)
    #处理经理
    tmp1=[]
    for t in persons:
        # print(t)
        if type(types)==list:
            for i in range(0,len(types)):
                if types[i]=='经理' and content.index('经理')>content.index(t):
                    # print('qa=',types[i],t)
                    continue
                else:
                    tmp1.append(types[i])
    if len(tmp1)>0:
        types=tmp1

    return types,money,acquire,number,contact,city,work_time,place,persons

def get_res(content, wxid, raw, time,data_original):
    """
    :param content:
    :return:
    """
    types, money, acquire, number, contact, city, work_time, place,persons = getAllMsg(content,data_original)

    # types_r=[]

    # for it in types:
    #     it = str(it)
    #     number_txt = re.findall('\d+名', it);
    #
    #     number_txt2 = re.findall('\d+人', it);
    #
    #     it = it.replace(str(number_txt).replace('[','').replace(']','').replace('\'',''), '').replace(str(number_txt2).replace('[','').replace(']','').replace('\'',''), '')
    #     types_r.append(it)
    # types = types_r
    return process_return(types, money, acquire, number, contact, city, work_time, place, persons,wxid, raw, time,data_original,content)#此句新添加



def process_return(types, money, acquire, number, contact, city, work_time, place, persons,wxid, raw, time,data_original,content):
    # #处理 工种包含数字
    # if type(types)==list:
    #     for i in range(0, len(types)):
    #         # 处理  "工种": "小时工17元/小",
    #         find = re.findall('\d+', types[i])
    #         for j in range(0, len(find)):
    #             if find[j] in types[i]:
    #                 idx = types[i].index(find[j])
    #                 if idx != 0:
    #                     types[i] = types[i][:idx]
    #         tmp = types[i]
    #         for j in range(0, len(number)):
    #             tmp = tmp.replace(number[j], '')
    #             types[i] = tmp
    # else:
    #     # 处理  "工种": "小时工17元/小",
    #     find = re.findall('\d+',types)
    #     for j in range(0, len(find)):
    #         if find[j] in types:
    #             idx = types.index(find[j])
    #             if idx != 0:
    #                 types = types[:idx]
    #     tmp = types
    #     for j in range(0, len(number)):
    #         tmp = tmp.replace(number[j], '')
    #         types= tmp
    # #处理 工种重复:普焊和普焊带焊 types=['普焊','普焊带焊','啊啊啊哈哈哈','啊啊啊']
    # types = ['普焊', '普焊带焊', '啊啊啊哈哈哈', '啊啊啊']
    # if type(types)==list and len(types)>1:
    #     tmp = []
    #     for i in range(0, len(types)):
    #         for j in range(0, len(types)):
    #             if i != j:
    #                 if types[i] in types[j] and types[i] not in tmp:
    #                     tmp.append(types[i])
    #                     types[j] = types[i]
    #                 elif types[j] in types[i] and types[j] not in tmp:
    #                     tmp.append(types[j])
    #                     types[i] = types[j]
    #                 if types[j] not in types[i] and types[i] not in types[j] and types[i] not in tmp and j == len(
    #                         types) - 1:
    #                     tmp.append(types[i])
    #         if types[i] not in tmp and i == len(types) - 1:
    #             tmp.append(types[i])
    #     types = tmp
    if type(types)==list:
        for i in range(0, len(types)):
            if '一开一' in types[i] and type(number)==list:
                number.insert(i,'1组')
                break
    if type(types) == list:
        for i in range(0, len(types)):
            if '一开一' in types[i] and "司机" in types:
                types.remove('司机')
                break
    # print(types)
    # 处理 工种重复:但是留长的 types=['普焊','普焊带焊','啊啊啊哈哈哈','啊啊啊']
    # types = ['普焊', '普焊带焊', '啊啊啊哈哈哈', '啊啊啊']
    if type(types) == list and len(types) > 1:
        tmp = []
        for i in range(0, len(types)):
            for j in range(0, len(types)):
                if i != j:
                    if types[i] in types[j] and types[j] not in tmp:
                        tmp.append(types[j])
                        types[i] = types[j]
                    elif types[j] in types[i] and types[i] not in tmp:
                        tmp.append(types[i])
                        types[j] = types[i]
                    if types[j] not in types[i] and types[i] not in types[j] and types[i] not in tmp and j == len(
                            types) - 1:
                        tmp.append(types[i])
            if types[i] not in tmp and i == len(types) - 1:
                tmp.append(types[i])
        types = tmp
    # print(types)
    # #处理 "工种": "电梯司机工地可以煮饭",
    # flag = 0
    # for t in types:
    #     if '一开一' in t:
    #         flag = 1
    #         break
    # regex = '塔吊指挥|电话客服|快递员|指挥男|电梯司机|信号工|司机|指挥|施工员|测量员'
    # newt = re.findall(regex, content)
    # if flag==0:
    #     for i in range(0, len(types)):
    #         for t in newt:
    #             if t in types[i]:
    #                 types[i] = t
    #
    # #处理 工资包含： "6500加班20女不超过45岁男不超过50岁"，电话
    # for i in range(0,len(money)):
    #     for t in contact:
    #         money[i]=money[i].replace(t,'')
    #     for t in acquire :
    #         if type(money)!=list:
    #             money[i]=money[i].replace(t,'')

    # for i in range(0,len(types)):
    #     types[i] = types[i].replace(' ','').replace('（','').replace('|','').replace('.','').replace('）','')
    all_info=[]
    # if len(types) > 1:
    for i in range(0, len(types)):
        if len(types) > 1 and type(types)==list:
            one_types = types[i]
        else:
            one_types=types
        if len(money) > i and len(types) > 1 and type(types)==list:

            one_money = money[i]
        else:
            one_money = money
            # t1=[]
            # for t in one_money:
            #     if t not in t1:
            #         t1.append(t)
            # one_money=t1
            # print(one_money)
        if len(acquire) > i and len(types) > 1 and type(types)==list:
            one_acquire = acquire[i]
        else:
            one_acquire = acquire
        if len(number) > i and len(types) > 1 and type(types)==list:
            one_number = number[i]
        elif len(number) <= i and len(types) > 1 and type(types)==list:
            one_number = ''
        else:
            one_number = number
        if len(contact) >= len(types) and len(types) > 1 and type(types)==list:
            one_contact = contact[i]
        else:
            one_contact = contact
        one_contact = str(one_contact).replace(']', '').replace('[', '').replace(',', '').replace('\'','')
        if len(place) >= len(types) and len(types) > 1 and type(types)==list:
            one_place = place[i]
        else:
            one_place = place
        if len(city) >= len(types) and type(city) != type("") and type(types)==list:
            one_city = city[i]
        else:
            one_city = city
        res = ''  # 地址
        if type(one_city) == list and type(types)==list:
            for item in one_city:
                if "市" in item:
                    res = item
                    break
            if res == '':
                one_city = one_city[0]
            else:
                one_city = res
        if len(work_time) >= len(types) and type(types)==list:
            one_time = work_time[i]
        else:
            one_time = work_time
        if type(one_acquire)==list  :
            work_content=",".join(one_acquire)
        else:
            work_content = one_acquire
        if type(one_money)==list:
            work_content=work_content  +" "+",".join(one_money)
        else:
            work_content = work_content + " " + one_money
        # if type(one_time)==list:
        #     work_content = work_content +" "+",".join(one_time)
        # else:
        #     work_content = work_content + " " +one_time
        if type(persons) == list and len(persons)>=len(types):
            one_persons =  persons[i]
        else:
            one_persons = persons
        info = {"工种": one_types, "期望工作地点": one_city, "招工单位": one_place, "招工人数": one_number, "联系人": one_persons,
              "联系电话": one_contact}
        all_info.append(info)
        if type(types)!=list:
            break
    res = { "期望工作地点": city, "招工单位": place, "招工信息":all_info,"联系人": "无",
           "联系电话": contact, "联系微信": "无", "项目内容": "无"}

    json_data = json.dumps(res, indent=4, ensure_ascii=False)
    # print(json_data)
    # save_database(res, wxid, raw, time, json_data)
    return types,acquire,money,data_original
    # return types,acquire,money,data_original
def delBlank(obj):
    t = []
    if type(obj)==type(t):
        for i in range(0,len(obj)):
            obj[i]=str(obj[i]).strip(' ')
    else:
        obj = str(obj).strip(' ')
    return obj

# def save_database(mul_res, wxid, raw, time, json_data):
#     dataset = read_config()
#     for x, y in dataset.items():
#         if x == "host":
#             host1 = y
#         elif x == "user":
#             user1 = y
#         elif x == "password":
#             password1 = y
#         elif x == "db":
#             db1 = y
#     DbHandle = DataBaseHandle(host1, user1, password1, db1)
#
#     for i in mul_res:
#         job_type = i['工种']
#         job_city = i['期望工作地点']
#         job_loc = i['招工单位']
#         job_num = i['招工人数']
#         job_peo = i['联系人']
#         job_tel = i['联系电话']
#         job_wx = i['联系微信']
#         job_req = i['要求']
#         job_mon = i['工资及福利']
#         job_tim = i['工作时长']
#         res = {"工种": delBlank(job_type), "期望工作地点":  delBlank(job_city), "招工单位": delBlank(job_loc), "招工人数": delBlank(job_num), "联系人": delBlank(job_peo), "联系电话": delBlank(job_tel), "联系微信": delBlank(job_wx),
#                "要求": delBlank(job_req), "工资及福利": delBlank(job_mon), "工作时长": delBlank(job_tim), "原始信息": raw}
#         json_data = json.dumps(res, ensure_ascii=False)
#         job_tel = str(job_tel).replace(' ','').replace('[ ]','').replace(']','').replace(',','')
#         json_data = str(json_data).replace('"', '\'')
#         DbHandle.insertDB(
#             'insert into recruit (mes_from, mes_raw, mes_time, mes_json) values ("%s", "%s", "%s", "%s")' % (
#                 wxid, raw, time, json_data))
#
#         print(json.dumps(res, indent=2, ensure_ascii=False))


def get_special_content(forward_text, content):
    """
    输入正则表达式匹配的开始的字符串，生成匹配的结尾字符串，返回匹配的结果
    :param forward_text:
    :param content:
    :return:
    """
    list_rg = [regex_place, regex_money, regex_time, regex_title, regex_content, regex_acquire, '<end>'
               , regex_number,regex_contact]  # 获取所有需要匹配的字符串
    list_rg.remove(forward_text)  # 移除开头字符串
    backward_text = "|".join(list_rg)  # 组合起来
    if(forward_text!=regex_title and forward_text!=regex_time and forward_text!=regex_money):
        regex_concat = '(?<=' + forward_text + ').*?(?=\\n|' + backward_text + '|～～|！|其它：)'  # 组成完整表达式
    else:#if (forward_text==regex_title):

        regex_concat = '(?<=' + forward_text + ').*?(?=，|。|：|！|' + backward_text+'|\\n)'
        # print(regex_concat)
    # else:
    #     print(forward_text)
    #     regex_concat = '(?<=' + forward_text + ').*?(?=' + backward_text + '|，|。|\\n)'
    # print(regex_concat)
    return re.findall(regex_concat, content)



def check(data, wxid, raw, time):
    conf = read_config()
    globals().update(conf)
    data_original = data
    # data=re.sub('\(.*?\)','',data)
    # data = re.sub('\（.*?\）', '', data)
    # data = re.sub('\（.*?\)', '', data)#（女不超过45岁男不超过50岁)\
    #处理 电话号码人
    phones=re.findall('[0-9]{11}', data)
    for p in phones:
        data=data.replace(p,' '+p+' ')
    #处理 189 0074 8140
    phones = re.findall('[0-9]{3} [0-9]{4} [0-9]{4}', data)
    for p in phones:
        data = data.replace(p,' '+p.replace(' ','')+' ')

    # 十人   30到50人 四个 五六个 8九个人 shi ming shiwu ming 一个工管住不管吃 一个礼拜 一个班
    # 算0.5个工 不要暑期工 暑假工不要 物流仓库 28个班 热水空调 汽车玻璃 服务费20 威特电梯 8个通层

    data = '<start>'+data.replace('有空调','有空 调').replace('胡经理','经 理').replace('招聘装配工','装配工').replace('空调车间','空 调车间').replace('招生','').replace('》','，').replace('个多月',' 个多月').replace('一个人','一 个人').replace('个星期',' 个星期').replace('一个工管住不管吃','一 个工管住不管吃').replace('个礼拜',' 个礼拜').replace('个班',' 个班').replace('0.5个工','0.5 个工').replace('个通层',' 个通层').replace('不要暑期工','').replace('暑假工不要','').replace('五个',' 5个').replace('个月',' 个月').replace('个小时',' 个小时').replace('三个',' 3个').replace('五个',' 5个').replace('两个',' 2个').replace('一个',' 1个').replace('十个人', ' 10人').replace('一名',' 1名').replace('二名',' 2名').replace('两名',' 2名').replace('三名',' 3名').replace('空调淋','空 调淋').replace('十人',' 10人')\
        .replace('四个',' 4个').replace('九个人',' 9个').replace('十五名',' 15名').replace('十名',' 10名') \
        .replace('物流仓库', '物 流仓 库').replace('热水空调', '热水空 调').replace('汽车玻璃', '汽车玻 璃 调').replace('服务费', '服 务费').replace('威特电梯', '威特电 梯').replace('空调室','空 调室').replace('五六个','5到6个').replace('26个英文字母','26 个英文字母').replace('26个大小写字母','26 个大小写字母').replace('26个字母','26 个字母').replace('个工作日',' 个工作日').replace('人间',' 人间').replace('2个及以上完整','2 个及以上完整').replace('人一个房间','人一个房间').replace('个房间',' 个房间').replace('十五个','15个').replace('四名','4名').replace('\n','').replace('管网证','管 网证').replace('六名','6名')+'<end>'
    # data_original=data_original.replace('法休','法定节假日休息')
    # print('da=',data)
    return get_res(data, wxid, raw, time,data_original)

def check_num_exist(content):
    patter = "(?:^|[^\d])(1\d{10})(?:$|[^\d])"
    phone_list = re.compile(patter).findall(content)
    if phone_list:
        return True
    else:
        return False

def getPERName(str_content):
    text = str_content
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    # print(resdict)
    res = []
    for item in resdict.items():
        if str(item[1]) == 'PER':
            res.append(item[0])
    return res







