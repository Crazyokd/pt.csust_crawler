#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-06-18


from crawler.spider import PTCrawler
from crawler.util import get_info

if __name__=='__main__':
    info = get_info()
    pt_crawler = PTCrawler(info['account'], info['password'])
    pt_crawler.visit_sn_list()

    input() # pause