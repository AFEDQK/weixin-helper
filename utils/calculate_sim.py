import jieba
from simhash import Simhash
import sys
sys.path.append('../database/')
threshold = 0


def calculate_simhash(s1, s2):
    words1 = jieba.lcut(s1, cut_all=True)
    words2 = jieba.lcut(s2, cut_all=True)
    sim = Simhash(words1).distance(Simhash(words2))
    # print("对比结果：", sim)
    if(sim>threshold):
        return False
    else:
        return True



