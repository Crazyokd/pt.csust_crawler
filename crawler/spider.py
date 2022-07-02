#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-06-18


import re
import requests
import os
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta
from crawler.util import handle_job_content_use_html2text, parse_exception

os.environ['NO_PROXY']="pt.csust.edu.cn" # cancel proxy

class PTCrawler():
    url1='http://pt.csust.edu.cn/meol/loginCheck.do'
    url2='http://pt.csust.edu.cn/meol/welcomepage/student/interaction_reminder_v8.jsp'
    url4='http://pt.csust.edu.cn/meol/common/hw/student/hwtask.jsp?tagbug=client&strStyle=new06'

    data = [['logintoken', '1632975162171'], ['IPT_LOGINUSERNAME','0'],['IPT_LOGINPASSWORD','0']]

    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        ,'Host': 'pt.csust.edu.cn'
    }
    head=headers.copy()
    head['Referer']='http://pt.csust.edu.cn/meol/index.do'

    other_head=headers.copy()
    other_head['X-Requested-With']='XMLHttpRequest'
    other_head['Referer']='http://pt.csust.edu.cn/meol/personal.do'

    reset = False
    total_message = ""

    def __init__(self, account, password):
        self.s = requests.Session()
        self.data[1][1]=account
        self.data[2][1]=password
        self.is_login_success = False
        # 登录获取JSESSIONID
        try:
            self.s.request(method='post', url=self.url1, timeout=5, headers=self.head, data=self.data)
            self.is_login_success = True
        except requests.exceptions.ConnectionError or requests.exceptions.ReadTimeout:
            print("Oops! Please check the network connection")


    def get_remind_data(self):
        response=self.s.request(method='get', url=self.url2, timeout=5, headers=self.other_head)
        html=BeautifulSoup(response.text, 'html.parser').select("div.reminderbody > div.reminderwrap > ul")[0]
        with open('crawler/reminder_data.html','w',encoding='utf-8') as f:
            f.write(str(html))


    def handle_data(self):
        with open('crawler/reminder_data.html','r',encoding='utf-8') as f:
            str=f.read()
        # seg_1='<li><a href="###" title="点击查看"><span>.*?</span>门课程有待提交作业</a>.*'
        # seg_2='<a href="###" onclick="window.open.*?=(\d*).*?>(.*?)</a></li>.*<li><a href="###" title="点击查看">'
        # # 贪婪匹配
        # regularexp1=re.compile(seg_1+seg_2,re.S)
        # # 非贪婪匹配
        # regularexp2=re.compile(seg_1+'?'+seg_2,re.S)
        regularexp=re.compile('<a href="###" onclick="window.open.*?lid=(\d*)&amp;t=hw.*?>(.*?)</a>',re.S)
        ans=re.findall(regularexp,str)
        result=[]
        for item in ans:
            result.append((item[0],item[1].lstrip().rstrip()))
        return result


    def visit_sn_list(self):
        if self.is_login_success:
            base_url='http://pt.csust.edu.cn/meol/common/inform/index_stu.jsp?'
            prs={
                'lid': '0',
                's_gotopage': 1
            }  
            try:
                while True:
                    response=self.s.request(method='get', url=base_url+urlencode(prs), timeout=5, headers=self.headers)
                    html = BeautifulSoup(response.text, 'html.parser').select("html > body > div")[0]
                    table = str(html.select("table.valuelist")[0])
                    print("开始访问第"+str(prs['s_gotopage'])+"页系统通知")
                    
                    # 待优化：仅爬取未访问过的系统通知
                    regularexp=re.compile('<a class="infolist" href="message_content.jsp\?nid=(\d*)"',re.S)
                    ans=re.findall(regularexp,table)
                    for item in ans:
                        self.visit_sn(item)
                    regg=re.compile('下一页',re.S)
                    next=re.findall(regg, str(html.select(".navigation > .page")[0]))
                    print("第"+str(prs['s_gotopage'])+"页系统通知访问完毕\n")
                    if next.__len__()==0:
                        break
                    else:
                        prs['s_gotopage']=int(prs['s_gotopage'])+1
            except BaseException as e:
                parse_exception(e)
            finally:
                # close connection
                self.s.close()


    def visit_sn(self, id):
        test_head = self.headers.copy()
        base_url="http://pt.csust.edu.cn/meol/common/inform/message_content.jsp?"
        params={
            'nid':id
        }
        t_url=base_url+urlencode(params)
        response=self.s.request(method='get', url=t_url, timeout=5, headers=test_head)
        print("通知"+str(id)+"访问情况:"+"成功" if response.status_code==200 else "失败")  #Python不支持三元运算符
        time.sleep(0.5)


    def visit_course(self, data):
        # clear total.txt
        with open('crawler/courses/total.txt','w',encoding='utf-8',newline='') as f:
            f.write("")
        base_url='http://pt.csust.edu.cn/meol/jpk/course/layout/newpage/index.jsp?'
        for id,name in data:
            params={
                'courseId':id
            }
            t_url=base_url+urlencode(params)
            # 得到DWRSESSIONID
            self.s.request(method='get',url=t_url,timeout=5,headers=self.headers)

            test_head=self.headers.copy()
            test_head['Referer']=t_url
            response=self.s.request(method='get',url=self.url4,timeout=5,headers=test_head)
            html = BeautifulSoup(response.text, "html.parser").select("table.valuelist")[0]
            self.parse_homework_list(str(html), name)


    def parse_homework_list(self, str:str, name):
        # 注意'?'一定要转义
        regexp=re.compile('<a class="enter" href="write.jsp\?hwtid=(\d*)"',re.S)
        ans=re.findall(regexp,str)
        base_url='http://pt.csust.edu.cn/meol/common/hw/student/hwtask.view.jsp?hwtid='
        for i in ans:
            response=self.s.request(method='get', url=base_url+i, timeout=5, headers=self.headers)
            self.parse_homework(response.text, name, i)
            time.sleep(1)
        print()
        

    def parse_homework(self, str,name,id):
        try:
            re_title=re.compile('<th width="18%">标题</th>.*?<td>(.*?)&nbsp;</td>',re.S)
            title=re.findall(re_title,str)[0]
            re_release_time=re.compile('<th>发布时间</th>.*?<td>(.*?)</td>',re.S)
            release_time=re.findall(re_release_time,str)[0].strip()
            re_deadline=re.compile('<th>截止时间</th>.*?<td>(.*?)</td>',re.S)
            deadline=re.findall(re_deadline,str)[0].strip()
            re_job_content=re.compile('<th class="top">作业内容</th>.*?<td class="text">.*?<input type=.*?value=(.*?)>',re.S)
            # job_content=re.findall(re_job_content,str)[0][1:-1].replace("&lt;p&gt;",'').replace("&lt;/p&gt;",'').strip()
            job_content = re.findall(re_job_content, str)[0][1:-1].strip()
        except Exception as e:
            print("作业"+str(id)+"解析失败")

        job='#### 标题：' + title + '' + '\n#### 发布时间：' + release_time + '\n#### 截止时间：' + \
            deadline + '\n#### 作业内容：\n' + handle_job_content_use_html2text(job_content) + '\n'
        print("### 课程名：《"+name+"》")
        print(job)
        with open('crawler/courses/'+name+'_'+id+'.txt', 'w', encoding='utf-8', newline='') as f:
            f.write(job)
        with open('crawler/courses/total.txt', 'a', encoding='utf-8', newline='') as f:
            f.write("\n================================================================\n") #最后的换行似乎会被忽略
            f.write(job)

        self.determine_is_reminder(id, name, title, deadline, job, job_content)

            
    def main(self):
        if self.is_login_success:  
            try:
                self.get_remind_data()
                course_list=self.handle_data()
                print("### 课程清单")
                print(course_list)
                print()

                if len(course_list) == 0:
                    self.reset = True
                else:
                    self.visit_course(course_list)
            except BaseException as e:
                parse_exception(e)
            finally:
                # close connection
                self.s.close()


    def reminder(self, course_id:str, rest_hours:float):
        write_content = ""
        message = ""
        if os.getenv(course_id) is None:
            # 新发布作业
            write_content = course_id + '=' + 'true'
            message = "有新发布作业"
        elif os.getenv(course_id+'_reminder_first_time') is None and rest_hours <= 24:
            # 时间在一天以内
            write_content = course_id + '_reminder_first_time=' + str(datetime.now())
            message = "有作业将在一天内截止"
        elif os.getenv(course_id+'_reminder_last_time') is None and rest_hours <= 12:
            # 时间在半天以内
            write_content = course_id + '_reminder_last_time=' + str(datetime.now())
            message = "有作业马上将在半天内截止"
        else:
            # 时间不满足或已发送过相应提醒
            pass

        if write_content != "":
            with open('.env', 'a', encoding='utf-8') as dot_file:
                dot_file.write("\n"+write_content)
        # 发送邮件提醒
        return message


    def determine_is_reminder(self, course_id, course_name, homework_title, deadline, job, homework_content): 
        dt_end_time = datetime.strptime(deadline, '%Y年%m月%d日 %H:%M:%S')
        rest_hours = (dt_end_time.timestamp() - (datetime.today() + timedelta(hours=8-int(time.strftime('%z')[0:3]))).timestamp())/3600

        message = self.reminder(str(course_id), rest_hours)
        if message != "":
            self.total_message += message + "：<<" + course_name + "：" + homework_title + ">>\r\n\n\n"
            with open('./bulk/ATTACH/hw_detail.md', 'a', encoding='utf-8', newline='') as f:
                f.write("\n================================================================\n") #最后的换行似乎会被忽略
                f.write(job)