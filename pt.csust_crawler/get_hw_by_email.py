import settings
import spider

if __name__=='__main__':
    try:
        spider.start_with_email(settings.ACCOUNT,settings.PASSWORD)
    except:
        print("账密错误或网络异常")
    finally:
        # 关闭连接
        spider.s.close()
        # 暂停程序，防止程序闪退
        # input()