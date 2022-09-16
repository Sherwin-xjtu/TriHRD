# -*- coding: utf-8 -*-
__author__ = 'jennyzhang'
import logging

class Config():
    # 创建一个logger
    def __init__(self,arg):
        self.log_file = arg
        self.logger = logging.getLogger('statisticNew')
        self.f = logging.Formatter('[%(levelname)s %(processName)s %(asctime)s %(funcName)s] %(message)s')
        self.h = logging.FileHandler(self.log_file, 'w')
        self.h.setFormatter(self.f)
        self.logger.addHandler(self.h)
        self.logger.setLevel(logging.INFO)

    def getLog(self):
        return self.logger
