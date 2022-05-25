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
        
    # determine whether reseting configuration
    if spider.reset == True:
        with open('.env', 'w', encoding='utf-8') as dot_file:
            dot_file.write("display_name="+settings.DISPLAY_NAME+"\n")
            dot_file.write("sender_email="+settings.SENDER_EMAIL+"\n")
            dot_file.write("email_password="+settings.EMAIL_PASSWORD+"\n")
            dot_file.write("account="+settings.ACCOUNT+"\n")
            dot_file.write("password="+settings.PASSWORD+"\n")
            
    # determine whether sending email
    if spider.total_message != "":
        send(spider.total_message)