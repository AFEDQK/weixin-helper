from LAC import LAC

from constant import PATH_CUSTION
from config_utils import ConfigLoader

# 装载LAC模型
from database_test import DataBaseHandle

lac = LAC(mode='lac')
# 装载干预词典, sep参数表示词典文件采用的分隔符，为None时默认使用空格或制表符'\t'
lac.load_customization(PATH_CUSTION, sep=None)
config_loader = ConfigLoader()
regex_config = config_loader.read_config()
replace_dict = config_loader.load_replace_dict()
all_provinces = config_loader.load_region()
DbHandle = DataBaseHandle(regex_config["host"], regex_config["user"], regex_config["password"], regex_config["db"])