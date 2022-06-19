#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Rekord
# @Date: 2022-06-18


import math
from bulk.send import send
import settings
from crawler.spider import PTCrawler
import os

if __name__ == '__main__':
    # clear hw_detail.md
    with open('./bulk/ATTACH/hw_detail.md', 'w', encoding='utf-8') as compose_file:
        compose_file.write("")

    # get homework
    pt_crawler = PTCrawler(settings.ACCOUNT, settings.PASSWORD)
    pt_crawler.main()

    # determine whether reseting configuration
    number_of_invalid_run = int(settings.NUMBER_OF_INVALID_RUN)
    run_frequency_level = int(settings.RUN_FREQUENCY_LEVEL)
    if pt_crawler.reset == True:
        # no data captured for the first time
        if number_of_invalid_run == 0:
            with open('.env', 'w', encoding='utf-8') as dot_file:
                dot_file.write("display_name="+settings.DISPLAY_NAME+"\n")
                dot_file.write("sender_email="+settings.SENDER_EMAIL+"\n")
                dot_file.write("email_password="+settings.EMAIL_PASSWORD+"\n")
                dot_file.write("account="+settings.ACCOUNT+"\n")
                dot_file.write("password="+settings.PASSWORD+"\n")

        number_of_invalid_run += 1
        if run_frequency_level < 3 and number_of_invalid_run >= 3 * math.pow(2, run_frequency_level):
            run_frequency_level = min(3, run_frequency_level+1)
    else:
        run_frequency_level = 0
        number_of_invalid_run = 0
    os.system('dotenv set run_frequency_level '+str(run_frequency_level))
    print()
    os.system('dotenv set number_of_invalid_run '+str(number_of_invalid_run))        
    print()

    # determine whether sending email
    if pt_crawler.total_message != "":
        send(pt_crawler.total_message)