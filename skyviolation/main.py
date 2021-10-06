import requests
import os
import time
import json

os.environ['NO_PROXY']='pan.xindongli-edu.com'

headers = {
        'User-Agent': 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

resource_list=[]

def downloader(url,path):
    start = time.time()
    response = requests.get(url,headers=headers,stream=True) # stream属性必须带上
    chunk_size = 1024 # 每次下载的数据大小
    content_size = int(response.headers['content-length']) # 总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB' %(content_size / chunk_size / 1024)) # 换算单位
        with open(path,'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
    else:
        print("下载地址似乎出问题了...")

def main():
    for res in resource_list:
        print(res["title"]+"下载中...")
        downloader(res["url"],'sky_violation/'+res["title"])
        print(res["title"]+"下载完成")

if __name__=='__main__':
    # with open("skyviolation_list.json",'w',encoding='utf-8') as f:
    #     f.write(json.dumps(urls,indent=4,ensure_ascii=False))
    with open('skyviolation_list.json','r',encoding='utf-8') as f:
        resource_list=json.loads(f.read())
    main()