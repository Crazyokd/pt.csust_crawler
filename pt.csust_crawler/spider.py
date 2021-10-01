import re
import requests
import os
import pyquery
import getpass
from urllib.parse import urlencode

os.environ['NO_PROXY']="pt.csust.edu.cn"
url1='http://pt.csust.edu.cn/meol/loginCheck.do'
url2='http://pt.csust.edu.cn/meol/welcomepage/student/interaction_reminder_v8.jsp'

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

s=requests.Session()    

def get_message():
    data[1][1]=input("请输入学号：")
    data[2][1]=getpass.getpass("请输入密码：")

def get_data():
    s.request(method='post',url=url1,timeout=5,headers=head,data=data)         
    response=s.request(method='get',url=url2,timeout=5,headers=other_head)
    html=pyquery.PyQuery(response.text)
    reminder=html("#reminder")
    with open('reminder_data.txt','w',encoding='utf-8') as f:
        f.write(reminder.html())

def handle_data():
    with open('reminder_data.txt','r',encoding='utf-8') as f:
        str=f.read()
    regularexp=re.compile('<a href="###" onclick="window.open.*?=(\d*).*?>(.*?)</a></li>',re.S)
    ans=re.findall(regularexp,str)
    result=[]
    for item in ans:
        result.append((item[0],item[1].lstrip().rstrip()))
    return result

def visit_course(data):
    base_url='http://pt.csust.edu.cn/meol/jpk/course/layout/newpage/index.jsp?'
    for id,name in data:
        params={
            'courseId':id
        }
        response=s.request(method='get',url=base_url+urlencode(params),timeout=5,headers=headers)
        with open('courses/'+name+'.txt','w',encoding='utf-8') as f:
            f.write(response.text)

def main():
    get_message()
    get_data()
    print(handle_data())
    visit_course(handle_data())

if __name__=='__main__':
    main()