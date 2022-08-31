import regex as re

from utils.extensions import lac


def getPERName(text):
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    res = []
    for item in resdict.items():
        if str(item[1]) == 'PER':
            res.append(item[0])
    return res


def getLOCName(text):
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    res = []
    for item in resdict.items():
        if str(item[1]) == 'LOC':
            res.append(item[0])
    return res


def getMNumber(text):
    lac_result = lac.run(text)
    resdict = dict(zip(lac_result[0], lac_result[1]))
    res = []
    for item in resdict.items():
        mystr = str(item[0]).replace('\n', '').replace(' ', '')
        if (str(item[1]) == 'm' or str(item[1]) == 'n') and len(mystr) == 11 and mystr.isdigit():
            res.append(mystr)
    return res


def handle_search(data):
    types_text = ["瓦工|砌筑|贴砖|抹灰", "建筑木工|铝模|二次结构", "钢筋工|翻样|后台", "架子工|架工|爬架", "电工|水电工", "水暖工|安装工|空调|管道|通风", "钢结构|网架|不锈钢",
                  "焊工|钳工|铆工|钣金", "普工|小工|杂工|力工", "混凝土工|砼工", "吊装工|装配式建筑|构件安装", "防水工", "弱电|安防|消防|电梯", "建筑信息模型",
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
                  "后厨小时工", "想找火葬场工作", "刮大白刷乳胶漆", "幕墙工", "油漆，刮原子灰，喷漆", "水磨石固化地平", "铲车司机！电焊工", "c1照4米2以下可开", "吊车",
                  "信号工|一开一指挥|塔司|普焊|升降机工人|索工|司机|货梯司机|一司两指|木工|技术主管|普通工人|大龄工|快递|分拣员|下料工|岩棉|绑扎师傅|中工|拖石膏工人|擦色师父|外护工|下吊绳师傅|支模师傅|收口师傅|接线工|管工|铺砖师傅|社会工|暑假工|木模师傅|铝膜工|钢构老师|水工|氩弧焊|冷做工|辅助工|派遣工|外包|正式工|检验员|注塑|售后客服|线检|差价工|技术员|小时工|日结工|女工|流水线|整机装配|跟单管理员|长期小时工|作业员|功能测试|包装|插件|骑手|顺丰快递|男工|学生工|熟练工|生产技工|检查员|女工|冷作|二保焊|打砂工|喷涂工|大工"]

    types = []
    for t in types_text:
        regex = t
        tmp = re.findall(regex, data)

        if tmp != None and tmp != []:
            for tt in tmp:
                if tt not in types:
                    types.append(tt)
    contact = getMNumber(data)
    person = getPERName(data)
    city = getLOCName(data)

    info = {"姓名": person, "期望工作城市": city, "工种": types, "联系电话": contact, "项目内容": "无"}

    return info, person, city, types, contact


def pre_process():
    d = """
    INSERT INTO `t_type_of_work` VALUES (1, '瓦工/砌筑/贴砖/抹灰', NULL, 1, 0, NULL, '2022-04-20 17:54:03', NULL, NULL);
INSERT INTO `t_type_of_work` VALUES (2, '建筑木工/铝模/二次结构', NULL, 1, 0, NULL, '2022-04-20 17:54:03', NULL, NULL);
INSERT INTO `t_type_of_work` VALUES (3, '钢筋工/翻样/后台', NULL, 1, 0, NULL, '2022-04-20 17:54:03', NULL, NULL);

    """
    data = re.sub('INSERT INTO `t_type_of_work` VALUES \(\d+, ', '', d)
    print(data)
    # data = re.sub(', NULL, NULL, \d+, \d+, \'\d+-\d+-\d+ \d+:\d+:\d+\', NULL, NULL\);', '', data)
    data = re.sub(', NULL, \d, \d, NULL, \'\d+-\d+-\d+ \d+:\d+:\d+\', NULL, NULL\);', '', data)
    print('hhhhhhhhh\n\n')
    print(data)
