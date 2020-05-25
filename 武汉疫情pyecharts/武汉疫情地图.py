import pymongo
import pandas as pd
import numpy as np
#新型冠状病毒3月14日数据结果

#连接数据库
client = pymongo.MongoClient()
db = client['yiqing']
data = db['country'].find()

# 数据清洗
# 查询结果是游标便利之后添加到列表
city_list = []
add_list = []
sum_list = []
cure_list = []
die_list = []
for i in data:
    city_list.append(i['城市'])
    add_list.append(i['新增确诊'])
    sum_list.append(i['累计确诊'])
    cure_list.append(i['治愈'])
    die_list.append(i['死亡'])
print(city_list)

#将数据中的-值用0代替 并且将字符串全部转换为数字进行处理
def str_int(value):
    for i in range(len(value)):
        if value[i] =='-':
            value[i]='0'
    for i in range(len(value)):
        value[i] = int(value[i])
    return value


#一.世界六大洲疫情统计数据
six_zhou = city_list[-6:]
six_zhou_a = str_int(add_list)[-6:]
six_zhou_s = str_int(sum_list)[-6:]
six_zhou_c = str_int(cure_list)[-6:]
six_zhou_d = str_int(die_list)[-6:]


#二.其他国家疫情统计
other_city = city_list[:48]
other_a = str_int(add_list)[:48]
other_s = str_int(sum_list)[:48]
other_c = str_int(cure_list)[:48]
other_d = str_int(die_list)[:48]

print(other_s)
#三.中国城市疫情统计数据
# print(city_list.index('湖北')) 48
# print(city_list.index('西藏')) 81
china_city = city_list[48:82]
china_a = str_int(add_list)[48:82]
china_s = str_int(sum_list)[48:82]
china_c = str_int(cure_list)[48:82]
china_d = str_int(die_list)[48:82]

from pyecharts.charts import Bar,Geo,Map,Grid #图库
from pyecharts import options as opts #标题设置
from pyecharts.globals import ThemeType #主题

bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE))
bar.add_xaxis(six_zhou)
bar.add_yaxis('总确诊人数',six_zhou_s)
bar.add_yaxis('新增确诊人数',six_zhou_a)
bar.add_yaxis('新增治愈人数',six_zhou_c)
bar.add_yaxis('新增死亡人数',six_zhou_d)
bar.set_global_opts(title_opts={'text':'3月14日六大洲疫情情况','subtext':'数据来源百度疫情实时大数据'})
bar.render()
x = [list(z) for z in zip(china_city,china_s)]

map = Map(init_opts=opts.InitOpts(width='900px',height='550px',renderer='RenderType.CANVAS' ,theme=ThemeType.ROMA))
map.add('确诊总人数',x,'china')
map.set_global_opts(
    title_opts=opts.TitleOpts(title="中国地图"),
    visualmap_opts=opts.VisualMapOpts(max_=1450),
)

map.render('全国地图.html')

other_city1=["China", "Canada", "Brazil", "Russia", "United States","France"]
other_s1 = [67933,27980,205,93,12300,27980]
# other_s1=[1750,5233]
map = Map(init_opts=opts.InitOpts(width='900px',height='550px',renderer='RenderType.CANVAS' ,theme=ThemeType.ROMA))
map.add('确诊总人数',[list(z) for z in zip(other_city1,other_s1)],'world')
map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
map.set_global_opts(
    title_opts=opts.TitleOpts(title="世界地图"),
    visualmap_opts=opts.VisualMapOpts(max_=30000),
)

map.render('其他国家.html')