import requests
import sqlite3
from lxml import etree
from openpyxl import Workbook

class Download(object):

    def getCollogeDic(self):
        '''
        获取学院字典
        :return: 学院字典
        '''
        collogeDic = {}
        #发送请求抓取学院信息
        url = 'http://zhjwjs.scu.edu.cn/teacher/personalSenate/giveLessonInfo/thisSemesterClassSchedule/indexPublic'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }
        r=requests.get(url = url, headers = headers)

        html = etree.HTML(r.text)
        collogeName = html.xpath("//select[@id='kkxs']//option/text()")[1:]
        collogeId = html.xpath("//select[@id='kkxs']//option/@value")[1:]

        for i in range(len(collogeId)):
            collogeDic[collogeId[i]] = collogeName[i]

        return collogeDic

    def query(self, kkxs, terms="2019-2020-1-1"):
        '''
        :param kkxs:学院编号
        :param terms: 学期号，默认2018-2019-2-1,terms格式为2018-2019-2-1
        :return:每个学院返回的课表数据
        '''

        datalist = []       #每个学院的课表数据
        #请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }
        url = "http://zhjwjs.scu.edu.cn/teacher/personalSenate/giveLessonInfo/thisSemesterClassSchedule/getCourseArragementPublic"
        postdata = {
            "zxjxjhh": terms,  # 学期,默认是18-19第二学期
            "kch": "",  # 课程号
            "kcm": "",  # 课程名
            "js": "",  # 教师
            "kkxs": kkxs,  # 开课院系
            "skxq": "",  # 上课星期
            "skjc": "",  # 上课节次
            "xq": "",  # 校区
            "jxl": "",  # 教学楼
            "jas": "",  # 教室
            "pageNum": "1",  # 显示的页数
            "pageSize": "30",  # 每页的课程数
            "kclb": ""  # 课程类别
        }
        r = requests.post(url = url, data = postdata, headers = headers)
        m = r.json()["list"]
        #继续下一页请求直到完成
        totalcourse = m["pageContext"]["totalCount"]  # 总课数
        page = totalcourse / 30 + 1
        while int(postdata["pageNum"]) <= page:  # 存储数据到list
            currentpage = int(postdata["pageNum"])
            for i in r.json()["list"]["records"]:
                datalist.append(i)
            currentpage += 1
            postdata["pageNum"] = str(currentpage)
            r = requests.post(url=url, data=postdata, headers=headers)

        return datalist

    def save_to_excel(self):
        '''
        保存数据为excel
        :return: None
        '''
        #创建表格
        wb = Workbook()
        ws = wb.active
        ws.append(["课程号",
                   "课序号",
                   "课程名",
                   "学分",
                   "开课院系",
                   "上课教师",
                   "选课限制",
                   "校区",
                   "上课教室",
                   "上课星期",
                   "周次",
                   "教学楼",
                   "上课节次"])      #添加第一行

        collogeDic = self.getCollogeDic()           #获取学院信息

        for colloge_id in collogeDic:       #循环遍历填充信息
            response_course = self.query(colloge_id)
            for each_course in response_course:
                kch = each_course['kch']  # 课程号
                kxh = each_course['kxh']  # 课序号
                kcm = each_course['kcm']  # 课程名
                xf = each_course['xf']  # 学分
                kkxsjc = each_course['kkxsjc']  # 开课院系
                skjs = each_course['skjs']  # 上课教师
                xkxzsm = each_course['xkxzsm'].strip()  # 选课限制说明
                kkxqm = each_course['kkxqm']  # 校区
                jash = each_course['jash']  # 上课教室
                skxq = each_course['skxq']  # 上课星期
                zcsm = each_course['zcsm']  # 周次
                jxlm = each_course['jxlm']  # 教学楼
                if (each_course['skjc'] != None):
                    jieci = str(each_course['skjc']) + "-" + str(each_course['skjc'] + each_course['cxjc'] - 1)  # 上课节次
                else:
                    jieci = None
                ws.append([kch, kxh, kcm, xf, kkxsjc, skjs, xkxzsm, kkxqm, jash, skxq, zcsm, jxlm, jieci])
            print("%s数据已完成" % collogeDic[colloge_id])

        wb.save('course.xlsx')      #保存

    def save_to_db(self):
        '''
        保存到数据库
        :return:
        '''
        #创建表
        con=sqlite3.connect("course.db")
        cursor = con.cursor()

        cursor.execute('''CREATE TABLE course(
                                                课程号 varchar(50),
                                                课序号 varchar(50),
                                                课程名 varchar(50),
                                                学分 varchar(50),
                                                开课院系 varchar(50),
                                                上课教师 varchar(50),
                                                选课限制 varchar(50),
                                                校区 varchar(50),
                                                上课教室 varchar(50),
                                                上课星期 varchar(50),
                                                周次 varchar(50),
                                                教学楼 varchar(50),
                                                上课节次 varchar(50))''')       #创建数据表
        con.commit()

        collogeDic = self.getCollogeDic()  # 获取学院信息

        for colloge_id in collogeDic:  # 循环遍历填充信息
            response_course = self.query(colloge_id)
            for each_course in response_course:
                kch = each_course['kch']  # 课程号
                kxh = each_course['kxh']  # 课序号
                kcm = each_course['kcm']  # 课程名
                xf = each_course['xf']  # 学分
                kkxsjc = each_course['kkxsjc']  # 开课院系
                skjs = each_course['skjs']  # 上课教师
                xkxzsm = each_course['xkxzsm'].strip()  # 选课限制说明
                kkxqm = each_course['kkxqm']  # 校区
                jash = each_course['jash']  # 上课教室
                skxq = each_course['skxq']  # 上课星期
                zcsm = each_course['zcsm']  # 周次
                jxlm = each_course['jxlm']  # 教学楼
                if (each_course['skjc'] != None):
                    jieci = str(each_course['skjc']) + "-" + str(each_course['skjc'] + each_course['cxjc'] - 1)  # 上课节次
                else:
                    jieci = None

                cursor.execute('''insert into course(课程号,
                                                    课序号,
                                                    课程名,
                                                    学分,
                                                    开课院系,
                                                    上课教师,
                                                    选课限制,
                                                    校区,
                                                    上课教室,
                                                    上课星期,
                                                    周次,
                                                    教学楼,
                                                    上课节次)
                                                    values(
                                                    ?,?,?,?,?,?,?,?,?,?,?,?,?
                                                    )''',(kch,
                                                          kxh,
                                                          kcm,
                                                          xf,
                                                          kkxsjc,
                                                          skjs,
                                                          xkxzsm,
                                                          kkxqm,
                                                          jash,
                                                          skxq,
                                                          zcsm,
                                                          jxlm,
                                                          jieci,))          #填充信息
            print("%s数据已完成" % collogeDic[colloge_id])

        con.commit()

if __name__=="__main__":
    d=Download()
    print('''请选择保存方式:
            1 保存到excel
            2 保存到sqlite数据库''')
    i=input('请输入数字:')
    if i=='1':
        d.save_to_excel()
    elif i=='2':
        d.save_to_db()