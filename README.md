# 四川大学课表下载

<p>
<img src='https://img.shields.io/badge/author-%E5%B0%8F%E5%B7%9D-ff69b4.svg'>
<img src='https://img.shields.io/github/license/2239559319/courseDownload.svg?style=flat'>
<img src='https://img.shields.io/badge/python-3.0%2B-blue.svg'>
<img src='https://img.shields.io/badge/python-3.6-blue.svg'>
<img src='https://img.shields.io/pypi/dm/scuCourseDownloader.svg?colorB=blue&style=flat'>
</p>

* * *

\##运行环境:python3.6

> 第三方模块:requests,lxml,openpyxl

## 运行方法，运行main.py文件即可

## 注意

-   程序运行时间依赖网速，可能由于网速过快倒是出现运行失败，这个时候重新运行即可。每一个学院的课表处理完后都有提示信息。
-   程序运行后会提示选择保存方式，可以保存为excel或者sqlite数据库文件。保存问excel运行完成会在当前目录下生成course.xlsx文件，保存为数据库文件会在当前目录下生成course.db文件。
-   ## 程序默认下载的是18-19第二学期课表，如果要下载其他课表，请在代码70行query函数添加第二参数学期，格式为"2018-2019-2-1"

> 如果想学习本程序教程请点击后面的链接进入教程[程序教程][2]

> 开发者版本scuCourseDownloader已经上传至pypi，[进入pypi页面][1]

[1]: https://pypi.org/project/scuCourseDownloader/

[2]: https://blog.csdn.net/w2239559319/article/details/88359913
