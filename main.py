import math
import requests
from bulk.send import send
import settings
import crawler.spider as spider
import os

if __name__ == '__main__':
    # clear hw_detail.md
    with open('./bulk/ATTACH/hw_detail.md', 'w', encoding='utf-8') as compose_file:
        compose_file.write("")

    try:
        # get homework
        spider.start_with_email(settings.ACCOUNT,settings.PASSWORD)

        # determine whether reseting configuration
        if spider.reset == True:
            number_of_invalid_run = int(settings.NUMBER_OF_INVALID_RUN)
            # no data captured for the first time
            if number_of_invalid_run == 0:
                with open('.env', 'w', encoding='utf-8') as dot_file:
                    dot_file.write("display_name="+settings.DISPLAY_NAME+"\n")
                    dot_file.write("sender_email="+settings.SENDER_EMAIL+"\n")
                    dot_file.write("email_password="+settings.EMAIL_PASSWORD+"\n")
                    dot_file.write("account="+settings.ACCOUNT+"\n")
                    dot_file.write("password="+settings.PASSWORD+"\n")

            number_of_invalid_run += 1
            os.system('dotenv set number_of_invalid_run '+str(number_of_invalid_run))
            run_frequency_level = int(settings.RUN_FREQUENCY_LEVEL)
            if run_frequency_level < 3 and number_of_invalid_run >= 3 * math.pow(2, run_frequency_level):
                run_frequency_level = min(3, run_frequency_level+1)
                os.system('dotenv set run_frequency_level '+str(run_frequency_level))
        else:
            os.system('dotenv set run_frequency_level 0')
            os.system('dotenv set number_of_invalid_run 0')
                
        # determine whether sending email
        if spider.total_message != "":
            send(spider.total_message)

    except IndexError:
        print("Oops! Your account is blocked or Wrong account or password")
    except requests.exceptions.ConnectionError:
        print("Oops! Please check the network connection")
    finally:
        # 关闭连接
        spider.s.close()