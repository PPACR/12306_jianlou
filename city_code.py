#导入包
import sqlite3
import requests

#构造headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
}

#城市代码
train_code_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'

#获取响应
response = requests.get(url=train_code_url, headers=headers)

#自动解码
response.encoding = response.apparent_encoding

#处理数据
text = response.text.replace("var station_names ='", '')[:-2]
list = text.split('@')[1:]

#将数据保存到字典
city_code_dict = {}
for i in list:
    i = i.split('|')
    city_code_dict[i[1]] = i[2]

#创建数据库链接
conn = sqlite3.connect('12306.db')
c = conn.cursor()

#创建数据表
# c.execute('''CREATE TABLE "citycode" (
#   "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "city" TEXT NOT NULL,
#   "code" TEXT NOT NULL
# );''')

#将字典插入数据库
for k, v in city_code_dict.items():
    c.execute(f"INSERT INTO main.citycode (city,code) VALUES ('{k}','{v}')")
conn.commit()
conn.close()
