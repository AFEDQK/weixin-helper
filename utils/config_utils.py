# -*- coding: utf-8 -*- #
# @Time : 2022/8/13 21:52
import json
from constant import PATH_RE_CONFIG


class ConfigLoader(object):
    def init_app(self, app):
        self.regex_config = self.read_config()

    def read_config(self):
        """"读取配置"""
        with open(PATH_RE_CONFIG, "r", encoding='UTF-8') as json_file:
            config = json.load(json_file)
        return config

    def update_config(self, config):
        """"更新配置"""
        with open(PATH_RE_CONFIG, "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)
        return None
