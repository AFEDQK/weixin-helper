from LAC import LAC

from utils.constant import PATH_CUSTION
from utils.config_utils import ConfigLoader

# 装载LAC模型
lac = LAC(mode='lac')
# 装载干预词典, sep参数表示词典文件采用的分隔符，为None时默认使用空格或制表符'\t'
lac.load_customization(PATH_CUSTION, sep=None)
config_loader = ConfigLoader()

