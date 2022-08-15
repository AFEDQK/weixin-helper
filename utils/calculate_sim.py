import jieba
from simhash import Simhash
import sys
sys.path.append('../database/')
from database_test import *
threshold = 3


def calculate_simhash(s1, s2):
    words1 = jieba.lcut(s1, cut_all=True)
    words2 = jieba.lcut(s2, cut_all=True)
    sim = Simhash(words1).distance(Simhash(words2))
    # print(sim)
    if(sim>threshold):
        return False;
    else:
        return True;

if __name__ == '__main__':
    str1 = "【阿里达摩院】NLP组日常/校招实习 （北京/杭州 可转正）\
    团队介绍：\
     我们属于达摩院NLP团队，本组主要围绕搜索相关NLP进行前沿技术攻坚与落地。\
     涉及方向包括语言模型、基础词法分析、向量召回、语义相关性。\
     我们有良好的业务场景、海量的数据资源与GPU资源，业务好、技术深、人员稳定。\
    实习内容：\
     结合实际业务中遇到的痛点难点，进行相关研究并发表论文\
     参加相关领域国际评测比赛\
    投递要求：\
     有至少一篇顶会/顶刊论文\
    其它：\
     校招实习生面向2022.11-2023.10毕业的海内外应届毕业生，实习期结束可转正\
    有兴趣的同学欢迎私聊或直接发送简历到ada.drx@alibaba-inc.com"


    str6 = "NLP组日常/校招实习 （北京/杭州 可转正）\
    团队介绍：\
     我们属于达摩院NLP团队，本组主要围绕搜索相关NLP进行前沿技术攻坚与落地。\
     \
     我们有良好的业务场景、海量的数据资源与GPU资源，业务好、技术深、人员稳定。\
    实习内容：\
     结合实际业务中遇到的痛点难点，进行相关研究并发表论文\
     参加相关领域国际评测比赛\
    投递要求：\
     有至少一篇\
    其它：\
     校招实习生面向2022.11-2023.10毕业的海内外应届毕业生，实习期结束可转正\
    有兴趣的同学欢迎私聊或直接发送简历到ada.drx@alibaba-inc.com"
    str2 = "招聘帖 知识图谱算法工程师\
    平安产险科技中心 急招 知识图谱算法工程师\
    base深圳平安金融中心\
    【岗位要求】\
    1、计算机相关方向，硕士及以上学历\
    2、三年以上工作经验，在大规模网络中，有实际的GCN的风控项目落地经验，架构设计经验;\
    3、熟悉图神经网络的图嵌入算法GCN、GraphSage、GAT HetGNN、HIN2vec等\
    4、熟悉图表示学习与计算框架包括PyG、DGL一种或多种。并精通 Spark、Hadoop等大数据分布式框架。\
    5、精通一个或多个编程语言，包括但不限于Python，scala，C/C++，精通sql、linux，精通graphframes库;\
    6、熟悉Neo4j图数据库，并掌握数据查询调优。\
    7、具备较强的钻研和攻关能力，善于沟通和团队协作，具有强的数据敏感性。\
    【职责】:1、负责公司保险关系图谱的建设和规划工作\
    2、负责制定解决跨业务风控、营销问题的图技术方案及落地实施。制定并实施可落地的大规模网络系统基础架构方案。\
    3、通过图数据分析及数据挖掘，多个维度输出逻辑性高、解释性强的分析报告，识别业务场景中团伙性黑产\
    4、主导图算法新技术的持续突破;\
    团队氛围好有活力，福利待遇丰厚～～\
    965工作制，有时需要加班，放心不卷～\
    感兴趣的大佬欢迎将简历投递至邮箱hanxuanw_cufe@163.com\
    也欢迎加微信whx549263141进一步了解岗位"

    str3 = "腾讯AI平台部招聘对话方向的NLP实习生，欢迎大家投递，base可北京可深圳。投递邮箱：josehwang@tencent.com\
    岗位要求：\
    1. 计算机相关专业，硕士及以上；\
    2. 具有扎实的机器学习，熟悉深度学习在NLP领域的常用方法，参与或主导过 NLP 项目（如对话/小说生成、知识图谱/事件图谱构建等优先），至少有1～2年相关经验；\
    3. 具有优秀的编码能力, 有扎实的数据结构和算法功底，熟悉常见的深度学习框架 (如tensorflow、pytorch)；\
    4. 具有优秀的分析问题和解决问题的能力，有激情，敢于接受具有挑战性的事情； \
    岗位职责： \
    1. 跟踪业界自然语言生成最新研究成果，如对话生成、小说创作等；\
    2. 根据实际应用效果不断改进模型或算法，将前沿NLP技术/成果应用于游戏内容生成场景中；\
    "

    str4 = '大龄工！20人！日结！月结均可！天津津南大型食品厂！' \
          '主要工作:辅助机器、装箱、码拍、摆料等简单易学的岗位 要求:男18-55周岁.女18-50周岁，两班倒制！' \
          '工资:3天后日结白班180元.夜班190元，平均工资5500以上待遇:免费3餐免费住宿免费体检免费发放行李被褥 ' \
          '联系电话:13114872789微信同步'
    # extract_info(str)
    str5 = '招聘清洁工！199990人！地点：月球！主要内容:扫地 ' \
           '要求:吃苦耐劳，两班倒制！待遇:1800/月' \
           ' 联系电话:13114872789微信同步'

    # calculate_simhash(str1,str6)
    # calculate_simhash(str3, str2)
    # calculate_simhash(str3, str1)
    # calculate_simhash(str1, str4)
    # calculate_simhash(str1, str5)
    # calculate_simhash(str3, str5)
    # DbHandle = DataBaseHandle()
    # raw_message, raw_num = DbHandle.selectDB('select mes_raw from message')
    # print(raw_num)
    # str_raw1 = ''.join(raw_message[1])
    # str_raw2 = ''.join(raw_message[2])
    # print(str_raw1)
    # print(str_raw2)
    # target = calculate_simhash(str_raw1, str_raw2)
    # print(target)



