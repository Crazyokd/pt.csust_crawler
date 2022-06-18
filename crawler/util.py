#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-06-18


import getpass
import re

def get_info():
    info = {}
    info['account'] = input("请输入学号：")
    info['password'] =getpass.getpass("请输入密码：") 
    print()
    return info


def parse_exception(e):
    if e.__class__.__name__ == 'IndexError':
        print("Oops! Your account is blocked or Wrong account or password")
    if e.__class__.__name__ == 'KeyboardInterrupt':
        print("Oops! You terminated the program manually")

    
def handle_job_content(self, job_content:str):
    # job_content=re.sub("&lt;.*?&gt;","",job_content)
    # 替换空格和换行符
    job_content=job_content.replace("&amp;nbsp;"," ")\
        .replace("&lt;br/&gt;","\n")
    # 去除标签
    job_content = re.sub("&lt;.*?&gt;","",job_content)
    # optmize
    job_content = job_content.replace("&amp;", "").replace("gt;", ">").replace("lt;", "<")
    # clean redundant line
    job_content = re.sub("\n{3,}", "\n\n", job_content)
    job_content = re.sub("(\r\n){3,}", "\r\n\r\n", job_content)

    return job_content