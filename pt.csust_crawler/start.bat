python pt.csust_crawler\\get_homework.py

copy /Y .\\pt.csust_crawler\\courses\\total.txt .\\bulk-email-sender\\ATTACH\\hw_detail.txt

del .\\pt.csust_crawler\\courses\\total.txt

python .\\bulk-email-sender\\send.py