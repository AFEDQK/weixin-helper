# -*- coding: utf-8 -*- #
# @Time : 2022/8/13 21:52
import json
from constant import PATH_RE_CONFIG, PATH_REGION, PATH_REGEX_REPLACE


class ConfigLoader(object):
    def init_app(self, app):
        self.regex_config = self.read_config()
        self.all_region = self.load_region()

    def read_config(self):
        """"读取配置"""
        with open(PATH_RE_CONFIG, "r", encoding="utf-8-sig") as json_file:
            config = json.load(json_file)
        return config

    def update_config(self, config):
        """"更新配置"""
        with open(PATH_RE_CONFIG, "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)
        return None

    def load_region(self):
        # 加载所有行政区（包括省，市，区，镇，乡，街道等）
        # https://github.com/uiwjs/province-city-china
        all_region = []
        with open(PATH_REGION, "r", encoding="utf-8") as fd:
            all_lines = fd.readlines()
            for item in all_lines:
                all_region.append(item.strip("\n"))
        return all_region

    def load_replace_dict(self):
        # 获取替换文本中特殊文本的数据
        replace_regular = []
        with open(PATH_REGEX_REPLACE, "r", encoding="utf-8") as fd:
            lines = fd.readlines()
            for line in lines:
                origin_text, replace_text = line.strip("\n").split(";")
                replace_regular.append((origin_text, replace_text))
        return replace_regular
