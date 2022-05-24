# from crawler.spider import start_with_email
from bulk.send import send
import settings
import crawler.spider as spider

if __name__ == '__main__':
    # clear hw_detail.md
    with open('./bulk/ATTACH/hw_detail.md', 'w', encoding='utf-8') as compose_file:
        compose_file.write("")

    # get homework
    try:
        spider.start_with_email(settings.ACCOUNT,settings.PASSWORD)
    except:
        print("账密错误或网络异常")
    finally:
        # 关闭连接
        spider.s.close()
        
    # determine whether sending email
    if spider.total_message != "":
        send(spider.total_message)