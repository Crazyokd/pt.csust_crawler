# pt.csust_crawler
爬取[长沙理工大学网络教学平台](http://pt.csust.edu.cn/meol/index.do)待提交作业

## 功能简介：
输入长沙理工大学网络教学平台的账号（学号）和密码。
即可得到有待提交作业的课程列表以及待提交作业的详细信息。

控制台会输出上面的信息。
另外程序还会自动创建几个文件。
其中`reminder_data.txt` 是课程通知的源代码（来自Ajax请求）
~~`courses`文件夹中会有课程列表中每个课程主页的源代码~~（~~希望会更新进行处理~~￣□￣｜｜）

**21.10.5更新：courses文件夹中含有待提交作业的详细信息，其中文件名的前半段表示课程名，后半段表示作业id。**

> 输入密码时采用的是getpass模块中的getpass方法，形式类似于Linux中输入密码，控制台不会进行回显(echo)。
>
> 由于太过频繁的访问将得不到网站的数据，所以整个程序做了延时处理，运行大约花费2s左右。

## 使用方法:

克隆仓库：

```shell
git clone https://github.com/Crazyokd/pt.csust_crawler.git
```

切换到clone位置：

```shell
cd pt.csust_crawler
```

安装好依赖：

```shell
pip install requests
pip install pyquery
```

运行脚本：

`python spider.py`

