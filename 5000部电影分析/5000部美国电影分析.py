
"""
1.案例背景
电影公司制作一部新电影推向市场时，要想获得成功，通常要了解电影市场趋势，
观众喜好的电影类型，电影的发行情况，改编电影和原创电影的收益情况，以及观众喜欢什么样的内容。

本案例来源于kaggle上的TMDB 5000 Movie Dataset数据集，
为了探讨电影数据可视化，
为电影的制作提供数据支持，主要研究以下几个问题：

电影类型如何随着时间的推移发生变化的？
Universal和Paramount两家影视公司的对比情况如何？
改编电影和原创电影的对比情况如何？
电影时长与电影票房及评分的关系？
分析电影关键字
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
#1. 底层编译： engine:c ==> python
credits = pd.read_csv('tmdb_5000_credits.csv', encoding='utf-8', engine='python')
# print(credits.info())

movies = pd.read_csv(r'tmdb_5000_movies.csv', encoding='utf-8', engine='python')
# print(movies.info())
#2.

# print((credits['title'] == movies['title']).sum())

#一、合并数据：
#1.修改表的名称：
credits.rename(columns={'movie_id':'id'}, inplace=True)

#2.主键合并
data = pd.merge(credits, movies, on=['title','id'], how='outer')
# print(data.info())


#二、数据分析：
#1. 电影类型如何随着时间的推移发生变化的？

#(1)找到空值的电影；# 2014-06-01
# print(data.loc[data['release_date'].isnull(), 'title'])

#(2)填充空值：
data['release_date'].fillna('2014/06/01', inplace=True)

#(3)求一共有多少种电影类型？
#a: 将json字符串类型转为Python类型：
data['genres'] = data['genres'].transform(json.loads)

#b.提出电影类型：
type_set = set()#存放所有电影类型；
def get_movie_type(element):
    type_list = []
    if element:
        for value in element:
            name = value['name'] #电影类型：
            type_list.append(name)
            type_set.add(name)
    return ' '.join(type_list)

data['genres'] = data['genres'].transform(get_movie_type)
# print(type_set)
# print(data['genres'])


#（4）字符串操作：判断是够包含某种电影，是的话给1， 不是给0
for movie_type in list(type_set):
    data[movie_type] = data['genres'].str.contains(movie_type).transform(lambda x:1 if x else 0)
# print(data.shape)

#（5）上映时间处理
data['release_year'] = pd.to_datetime(data['release_date']).dt.year

# print(data['release_year'].min())
# print(data['release_year'].max())

#(7)分析：
#（7-1） 每个年份各个类型的变化折线图：
Groupby_year = data.groupby('release_year')[list(type_set)].sum()

plt.figure(dpi=200)
#修改字体：
plt.rcParams['font.sans-serif'] = 'SimHei'
#正常显示符号问题：
plt.rcParams['axes.unicode_minus'] = False
x = Groupby_year.index  #年份
for movie_type in list(type_set):
    y = Groupby_year[movie_type]
    plt.plot(x, y)
plt.xlabel('年份')
plt.ylabel('数量')
plt.title('电影类型数量与年份之间关系')
plt.legend(list(type_set))
plt.savefig('数量与年份.png')
plt.show()

#(7-2)不同类型的电影总数的占比:
movie_type_sum = data[list(type_set)].sum(axis=0).sort_values(ascending=False)
plt.figure(figsize=(8,8))
plt.pie(movie_type_sum, labels=movie_type_sum.index, autopct='%1.1f%%')
# plt.show()


#(7-2)-2 柱状图：
plt.figure()
x = np.arange(len(list(type_set)))
y = movie_type_sum
plt.barh(x, y)
plt.yticks(x, movie_type_sum.index)
plt.title('不同类型电影总数')
plt.xlabel('数量')
plt.ylabel('电影种类')
plt.savefig('种类与数量.png')
# plt.show()

#问题二： 电影类型与利润的关系？
#（1）计算利润：
data['profit'] = data['revenue'] - data['budget']

#（2）每种类型的电影平均盈利各是多少？
#求取各个类型的电影的平均利润值，【不能直接分组搞定】
profit_mean_list = []
movie_type_list = []
for movie_type in list(type_set):
    profit_mean = data.loc[data[movie_type] == 1, 'profit'].mean()
    movie_type_list.append(movie_type)
    profit_mean_list.append(profit_mean)

#构建dataframe， 并进行排序
value= {'profit_mean':profit_mean_list, 'movie_type': movie_type_list}
profit_mean_df = pd.DataFrame(value).sort_values(by='profit_mean', ascending=False)
# print(profit_mean_df)

#绘图：
plt.figure()
# x = np.arange(len(list(type_set)))
# plt.barh(x, profit_mean_df['profit_mean'])
# plt.yticks(x, profit_mean_df['movie_type'])
# plt.show()

##问题三： Universal和Paramount两家影视公司的对比情况如何？

'Paramount Pictures'
'Universal Pictures'

#（1）创建两列值：分别为这两个公司，
data['Paramount Pictures']  = data['production_companies'].str.contains('Paramount Pictures')
data['Universal Pictures']  = data['production_companies'].str.contains('Universal Pictures')

#（2）盈利情况、 发行影片分析：
#a. 平均盈利情况：
#因为data['Paramount Pictures'] 元素为bool值， 可以将其作为取值条件：
Paramount_profit = data.loc[data['Paramount Pictures'], 'profit'].mean()
Univer_profit = data.loc[data['Universal Pictures'], 'profit'].mean()

#b. 发行影片情况：
Paramount_sum = data['Paramount Pictures'].sum()
Universal_sum  = data['Universal Pictures'].sum()

# p1 = plt.figure()
# x= [1, 2]
# y1 = [Paramount_profit, Univer_profit]
#
# p1.add_subplot(2,1,1)
# plt.bar(x, y1)
# labels = ['Paramount', 'Universal']
# plt.xticks(x, labels)
# plt.legend('平均每部电影的盈利')
#
# p1.add_subplot(2,1,2)
# y2= [Paramount_sum, Universal_sum]
# plt.bar(x, y2)
# plt.xticks(x, labels)
# plt.legend('每个公司发行影片情况')
# plt.show()


# 问题四改编电影和原创电影的对比情况如何？
data['keywords']=data['keywords'].transform(json.loads)
def get_name(element):
    based_on = ''
    for value in element:
        if 'based on' in value['name']:
            based_on+=value['name']
    return based_on
data['keywords']=data['keywords'].transform(get_name)
#找到有base on 字样的数据记为不是原创
data['是否原创']=data['keywords'].str.contains('based on')
#不是原创返回true 想将字段改为是否原创即不是原创 返回0
data['是否原创'] = data['是否原创'].transform(lambda x:0 if x else 1)
# print(data['是否原创'])
#4.1 按发行时间段比较 原创电影所占比例与非原创电影所占比例  判断原创电影与非原创电影发展峰值
data['发行时间段']=pd.cut(data['release_year'], range(1916,2019,10))
# print(data['发行时间段'])
yc_number = data.groupby('发行时间段')['是否原创'].sum()
total_number = data.groupby('发行时间段')['是否原创'].count()
no_yc_number = total_number-yc_number
s = pd.Series([str(yc_number.index[i]) for i in range(10)])
# print(s)
# print(total_number)
plt.figure(figsize=(10,8))
plt.plot(s.values,yc_number/total_number)
plt.plot(s.values,no_yc_number/total_number)
plt.legend(['原创','非原创'])
for x,y in zip(s.values,yc_number/total_number):
    plt.text(x,y+0.02,(round(y,1)))
for x,y in zip(s.values,no_yc_number/total_number):
    plt.text(x,y+0.02,(round(y,1)))
plt.grid(alpha=0.3)
plt.title('各时间段原创电影与非原创电影所占比例')
plt.savefig('原创.png')
# plt.show()

# 问题五电影时长与电影票房及评分的关系？
# 5.1 按电影时间段分组求电影票房的平均以及评分的平均
print(data['runtime'].isnull().sum())
print(data.info())
#17个字段
data['时长分段']=pd.cut(data['runtime'],[i for i in range(0,360,20)])
#按时间段分组的平均评分
vote_average=data.groupby('时长分段')['vote_average'].mean().dropna()
print(vote_average)
#按时间段分组的平均收入
revenue=data.groupby('时长分段')['revenue'].mean().dropna()
print(revenue)
r = pd.Series([str(revenue.index[i])for i in range(15)])
print(r)

x = ['0~20分钟','20~40分钟','40~60分钟','60~80分钟','80~100分钟','100~120分钟',
     '120~140分钟','140~160分钟','160~180分钟','180~200分钟','200~220分钟',
     '220~240分钟','240~260分钟','260~280分钟','280分钟之后']

plt.figure()
plt.plot(r.values,revenue.values)
plt.grid(alpha=0.3)
plt.ylabel('平均票房')
plt.xlabel('时间分组')
plt.xticks(r.values,x,rotation=270)
plt.title('电影时长与票房的关系')
plt.show()

plt.figure()

plt.plot(r.values,vote_average.values)
plt.grid(alpha=0.3)
plt.xticks(r.values,x,rotation=270)
plt.ylabel('平均评分')
plt.xlabel('时间分组')
plt.title('电影时长与评分的关系')
plt.savefig('时长与票房.png')
plt.show()