# pt.csust_crawler
[长沙理工大学网络教学平台](http://pt.csust.edu.cn/meol/index.do)的作业发布和作业截止提醒

## 功能简介：
1. 作业刚发布时提醒
2. 作业将截止时提醒
    - 截止提醒的第一次提醒的触发条件是**检测到作业未提交并将在一天内截止**。
    - 截止提醒的第二次提醒的触发条件是**检测到作业未提交并将在半天内截止**。

> 由于一项作业最多提醒三次，故不至于造成骚扰。
>
> 另外该项目应该对爬取长理网络教学平台其他数据有很大的参考价值。

## 前提要求：
- 下载[Python3](https://www.python.org/)
    > 目前版本限制不明确，推荐使用`python3.8`

- 使用如下命令安装好依赖：
    ```shell
    pip install -r requirements.txt
    ```

- 填写好[.env](.env)文件中的配置信息
    > **注意，文件最后一定要留下一行空白行。**

- 修改[data.csv](bulk/data.csv)文件中的配置信息（可参考[**bulk-email-sender**](bulk/README.md)）

## 使用方法
1. 简单测试运行
```shell
python main.py
```

2. 配合 GitHub Action 真正实现作业提醒
    
    以下操作的操作对象均为[main.yml](.github/workflows/main.yml)
    1. 打开第五行和和第六行的注释。
    2. 编辑第六行的 **`- cron`**，选择一个适当的运行频率。
        > 关于`cron`的含义和用法可参考[https://jasonet.co/posts/scheduled-actions/](https://jasonet.co/posts/scheduled-actions/)

    3. 修改第25行和第26行的`git`配置信息。

## 附加功能：
> **注意：必须在主目录下，否则相对路径会发生错误**

### 1. 简单爬取作业
#### 功能简介：
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

#### 使用方法：
```shell
python crawler/get_homework
```

### 2. 清除系统通知
#### 功能简介：
清除长沙理工大学网络教学平台的系统通知（_简而言之就是把系统通知访问一遍_）

> 治疗强迫症?

#### 使用方法:
```shell
python crawler/clean_sn.py
```

## 待办
- [x] 作业发布后进行提醒
- [x] 作业将要截止时进行提醒(两次)
- [x] 提供 shell 版本脚本
- [ ] 解析作业详情
- [ ] 当没有抓取到任何有效数据时，重置[.env](.env)文件
- [ ] 已访问过的系统通知不重复访问
- [x] 使用[beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)代替[pyquery](https://github.com/gawel/pyquery)
- [ ] 采用面向对象的思想重构代码
- [ ] 消除[.env](.env)文件最后一行留白限制
- [x] 修复时差问题
- [ ] 细化异常处理
- [x] 提供运行日志记录

## 参考
- [aahnik/bulk-email-sender](https://github.com/aahnik/bulk-email-sender)
- [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [ad-m/github-push-action](https://github.com/ad-m/github-push-action)

## 协议
在**Apache-2.0**许可证下发布。有关更多信息，请参阅[LICENSE](LICENSE)。