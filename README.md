# Crawler
程序目的 获得自己可能喜欢的书籍的信息。

给定初始豆瓣页面(默认为《代码大全》)url，然后提取该网页书籍的名称，评分，作者，出版社，出版时间，价格，ISBN，简介，热评和豆瓣推荐书籍的url。只要url管理器中的未爬取url集合不为空或者未到达指定爬取的次数，就一直爬取网页的信息以及新的url。

# 使用Python3.5编写，需要的Python模块：
- urllib, 高级Web交流模块，根据支持的协议下载数据
beautifulsoup4, 处理HTML/XML
re, 提供正则表达式相关操作
pymongo, 连接MongoDB数据库，并对其进行操作
pyExcelerator, 提供Excel相关的操作
 

- spider_main.py, 爬虫引擎，进行各项任务的调度
url_manager.py, url管理器，管理已爬取和未爬取的url，提供添加url，获取url，查询是否还有未爬取的url等功能
html_downloader.py, html下载器
html_parser.py, html分析器，提取html中的数据和url
html_outputer.py, html输出器，将提取的信息以一种较为友好的html形式保存
mongoDB.py, 数据库操作器，替代url管理器，html输出器
 

- 加入mongoDB.py, 数据库操作器
创建4个MongoDB集合，newUrls, oldUrls, notFoundUrls, book
在数据库操作器中实现url管理器的功能，这样就可以断点爬取了
在数据库操作器中实现html输出器的功能，将book集合中所有文档的关键信息打印成Excel文件


- 增加ISBN爬取
增加热评爬取
修改html输出器，显示ISBN以及热评
