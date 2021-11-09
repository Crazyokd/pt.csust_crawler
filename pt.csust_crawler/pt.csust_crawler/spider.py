import re
import requests
import os
import pyquery
import getpass
import time
from urllib.parse import urlencode

os.environ['NO_PROXY']="pt.csust.edu.cn"
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

s=requests.Session()    

def get_message():
    data[1][1]=input("请输入学号：")
    data[2][1]=getpass.getpass("请输入密码：")
    print()
    # 登录获取JSESSIONID
    s.request(method='post',url=url1,timeout=5,headers=head,data=data)

def get_remind_data():
    response=s.request(method='get',url=url2,timeout=5,headers=other_head)
    html=pyquery.PyQuery(response.text)
    reminder=html("#reminder")
    with open('reminder_data.txt','w',encoding='utf-8') as f:
        f.write(reminder.html())

def handle_data():
    with open('reminder_data.txt','r',encoding='utf-8') as f:
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

def visit_sn_list():
    base_url='http://pt.csust.edu.cn/meol/common/inform/index_stu.jsp?'
    prs={
    'lid':'0',
    's_gotopage':1
    }  
    while True:
        print("开始访问第"+str(prs['s_gotopage'])+"页系统通知")
        response=s.request(method='get',url=base_url+urlencode(prs),timeout=5,headers=headers)
        html=pyquery.PyQuery(response.text)
        table=html("table.valuelist").html()    #table类型为str
        # with open('table.txt','w',encoding='utf-8') as f:
        #     f.write(table)
        
        # 待优化：仅爬取未访问过的系统通知
        regularexp=re.compile('<a href="message_content.jsp\?nid=(\d*)" class="infolist"',re.S)
        ans=re.findall(regularexp,table)
        for item in ans:
            visit_sn(item)
        regg=re.compile('下一页',re.S)
        next=re.findall(regg,html.html())
        print("第"+str(prs['s_gotopage'])+"页系统通知访问完毕\n")
        if next.__len__()==0:
            break
        else:
            prs['s_gotopage']=int(prs['s_gotopage'])+1

def visit_sn(id):
    test_head=headers.copy()
    base_url="http://pt.csust.edu.cn/meol/common/inform/message_content.jsp?"
    params={
        'nid':id
    }
    t_url=base_url+urlencode(params)
    response=s.request(method='get',url=t_url,timeout=5,headers=test_head)
    print("通知"+str(id)+"访问情况:"+"成功" if response.status_code==200 else "失败")  #Python不支持三元运算符
    time.sleep(0.5)

def visit_course(data):
    base_url='http://pt.csust.edu.cn/meol/jpk/course/layout/newpage/index.jsp?'
    for id,name in data:
        params={
            'courseId':id
        }
        t_url=base_url+urlencode(params)
        # 得到DWRSESSIONID
        s.request(method='get',url=t_url,timeout=5,headers=headers)

        test_head=headers.copy()
        test_head['Referer']=t_url
        response=s.request(method='get',url=url4,timeout=5,headers=test_head)
        html=pyquery.PyQuery(response.text)
        table=html('table.valuelist')
        parse_homework_list(table.html(),name)
        time.sleep(1)

def parse_homework_list(str:str,name):
    # 注意'?'一定要转义
    regexp=re.compile('<a href="write.jsp\?hwtid=(\d*)" class="enter"',re.S)
    ans=re.findall(regexp,str)
    base_url='http://pt.csust.edu.cn/meol/common/hw/student/hwtask.view.jsp?hwtid='
    for i in ans:
        response=s.request(method='get',url=base_url+i,timeout=5,headers=headers)
        parse_homework(response.text,name,i)
    print()

def handle_job_content(job_content:str):
    # job_content=re.sub("&lt;.*?&gt;","",job_content)
    # 替换空格和换行符
    job_content=job_content.replace("&amp;nbsp;"," ")\
        .replace("&lt;br/&gt;","\n")
    # 去除标签
    return re.sub("&lt;.*?&gt;","",job_content)
    

def parse_homework(str,name,id):
    re_title=re.compile('<th width="18%">标题</th>.*?<td>(.*?)&nbsp;</td>',re.S)
    title=re.findall(re_title,str)[0]
    re_release_time=re.compile('<th>发布时间</th>.*?<td>(.*?)</td>',re.S)
    release_time=re.findall(re_release_time,str)[0].strip()
    re_deadline=re.compile('<th>截止时间</th>.*?<td>(.*?)</td>',re.S)
    deadline=re.findall(re_deadline,str)[0].strip()
    re_job_content=re.compile('<th class="top">作业内容</th>.*?<td class="text"><input type=.*?value=(.*?)>',re.S)
    job_content=re.findall(re_job_content,str)[0][1:-1].replace("&lt;p&gt;",'').replace("&lt;/p&gt;",'').strip()
    job='标题：'+title+''+'\n发布时间：'+release_time+'\n截止时间：'+deadline+'\n作业内容：\n'+handle_job_content(job_content)+'\n'
    print("课程名：《"+name+"》")
    print(job)
    with open('pt.csust_crawler/courses/'+name+'_'+id+'.txt','w',encoding='utf-8') as f:
        f.write(job)
    with open('pt.csust_crawler/courses/'+'total.txt','a',encoding='utf-8') as f:
        f.write("\n================================================================\n") #最后的换行似乎会被忽略
        f.write(job)
        

def clear_sn():
    get_message()
    visit_sn_list()

def main():
    get_message()
    get_remind_data()
    course_list=handle_data()
    print(course_list)
    print()
    visit_course(course_list)

if __name__=='__main__':
    try: 
        main()
    except:
        print("账密错误或网络异常")
    finally:
        # 关闭连接
        s.close()
        # 暂停程序，防止程序闪退
        # input()