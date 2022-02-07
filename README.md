# pt.csust_crawler
爬取[长沙理工大学网络教学平台](http://pt.csust.edu.cn/meol/index.do)待提交作业

## 功能简介：
输入长沙理工大学网络教学平台的账号（学号）和密码。
即可得到有待提交作业的课程列表以及待提交作业的详细信息。

控制台会输出上面的信息。

另外程序还会自动创建如下几个文件：

- `reminder_data.txt`： 课程通知的源代码（来自Ajax请求）。
- courses/课程文件：待提交作业的详细信息，其中文件名的前半段表示课程名，后半段表示作业id。
<br>

> - 输入密码时采用的是getpass模块中的getpass方法，形式类似于Linux中输入密码，控制台不会进行回显(echo)。
>
> - 由于太过频繁的访问将得不到网站的数据，所以整个程序做了延时处理，运行大约花费2s左右。

## 使用方法:
### 前置要求：

克隆仓库并进入仓库：

```shell
git clone https://github.com/Crazyokd/pt.csust_crawler.git
cd pt.csust_crawler
```

安装好依赖：

```shell
pip install -r requirements.txt
```

### 使用方法
#### 1. 爬取作业并邮件提醒

运行脚本：

```shell
start.bat
```

> 邮箱相关配置请参考[**bulk-email-sender**](bulk-email-sender/README.md)，邮件功能参考自[**aahnik/bulk-email-sender**](https://github.com/aahnik/bulk-email-sender)。

#### 2. 爬取作业不邮件提醒

运行脚本：

```shell
# 方法一：使用bat脚本
get_homework.bat
# 方法二：执行python文件
python ./pt.csust_crawler/get_homework.py
```
> **注意：必须在bat脚本目录下，否则相对路径会发生错误**

## 附加功能：
### 清除系统通知

#### 功能简介：

清除长沙理工大学网络教学平台的系统通知（_简而言之就是把系统通知访问一遍_）

> 治疗强迫症?

#### 使用方法:

安装依赖：

```shell
pip install -r requirements.txt		#无需重复安装
```

运行脚本：

```shell
cd pt.csust_crawler
python clear_sn.py
```