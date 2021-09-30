# pt.csust_crawler
爬取长沙理工大学网络教学平台未读通知课程和待提交作业课程

## 功能简介：
输入长沙理工大学网络教学平台的账号（学号）和密码。
即可得到有未读通知或有待提交作业的课程列表。

控制台会输出上面的信息。
另外程序还会自动创建几个文件。
其中`reminder_data.txt` 表示爬取的信息源代码（来自Ajax请求）
`courses`文件夹中会有课程列表中每个课程的源代码（~~希望会更新进行处理~~￣□￣｜｜）

> 输入密码时采用的是getpass模块中的getpass方法，形式类似于Linux中输入密码，控制台不会进行回显(echo)。

## 使用方法:

克隆仓库：

`git clone https://github.com/Crazyokd/pt.csust_crawler.git`

切换到clone位置：

`cd pt.csust_crawler`

安装好依赖：

```shell
pip install requests
pip install pyquery
```

运行脚本：

`python spider.py`
