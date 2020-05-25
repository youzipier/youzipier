import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#修改字体：
plt.rcParams['font.sans-serif'] = 'SimHei'
#正常显示符号问题：
plt.rcParams['axes.unicode_minus'] = False
#提取数据
data = pd.read_csv('dog.csv',encoding='utf-8')
data.drop(index=197,inplace=True)
print(data.info())
#将来源国数据清洗
def get_origin(element):
    if '中国' in element or '四川' in element or '青藏高原' in element or '贵州' in element:
        element = '中国'
    elif '英国' in element:
        element = '英国'
    elif '美国' in element:
        element = '美国'
    elif '法国' in element:
        element = '法国'
    elif '俄罗斯' in element:
        element = '俄罗斯'
    elif '加拿大' in element:
        element = '加拿大'
    elif '捷克斯洛伐克' in element or '捷克和斯洛伐克' in element:
        element = '捷克斯洛伐克'
    elif '中东地区' in element:
        element = '中东地区'
    return element
data['origin']=data['origin'].transform(get_origin)
# print(data['origin'])
#对犬种价格进行处理 吐血
def get_averge(element):
    if '-' in element:#4000--7000有个害群之马
        if '--' in element:
            element = element.replace('--','-')
        p=re.compile(r'(\d+)-(\d+)')
        data = p.findall(element) #[('1000', '3000')]
        price = (int(data[0][1])+int(data[0][0]))//2
        element = price
    elif '~' in element:
        p = re.compile(r'(\d+)~(\d+)')
        data = p.findall(element)  # [('1000', '3000')]
        price = (int(data[0][1]) + int(data[0][0])) // 2
        element = int(price)
    else:
        p = re.compile(r'\d+')
        data =p.search(element)
        if data:
            element = data.group()
            if element< '10':
                element = int(element*10000)
        else:
            element = 2000
    return element
data['price']=data['price'].transform(get_averge)
data['price']=data['price'].transform(int)
# print(data['price'].dtypes)
# 1.对比各个国家犬种的价格
df = data.groupby('origin')['price'].mean().reset_index()

#a.柱状图
sns.barplot(x='origin',y='price',data=df)
plt.xticks( rotation=270)

plt.show()

#2狗的是身高越高体重越大吗'
def change_cm(value):
    p = re.compile(r'(\d+).*?(\d+)')
    nums=p.findall(value)
    value = (int(nums[0][0])+int(nums[0][1]))/2
    return int(value)
data['height'] = data['height'].transform(change_cm)

def change_kg(value):
    p = re.compile(r'(\d+).*?(\d+)')
    nums = p.findall(value)
    value = (int(nums[0][0]) + int(nums[0][1])) / 2
    return int(value)

data['weight']= data['weight'].transform(change_kg)
# print(data[['height','weight','size','life_age']])

df1=data[['height','weight']]

# b.抖动图 （Jittering with stripplot）
# 通常，多个数据点具有完全相同的 X 和 Y 值。 结果，多个点绘制会重叠并隐藏。
# 为避免这种情况，请将数据点稍微抖动，以便您可以直观地看到它们。 使用 seaborn 的 stripplot（）很方便实现这个功能。
# fig = plt.subplots(figsize=(15,8), dpi= 80)
# sns.stripplot(df1['height'],df1['weight'], jitter=0.25, size=8,  linewidth=.5)
# plt.show()

# c.相关图查看个字段相关性
# 对寿命进行处理
data['life_age'] = data['life_age'].str[:2].str.replace('-','').str.replace('－','')
# print(data['life_age'])
#整体查看数据相似程度
# plt.figure()
# 相关图用于直观地查看给定数据框（或二维数组）中所有可能的数值变量对之间的相关度量
# sns.heatmap(data.corr())
# plt.show()

#d.树形图类似于饼图，它可以更好地完成工作而不会误导每个组的贡献
import squarify
df2 = data.groupby('origin').count().reset_index()
# print(df2)
sizes=df2.index.tolist()[1:]
# print(sizes)
labels = df2.apply(lambda x: str(x[0]) + " (" + str(x[1]) + ")", axis=1)
# print(labels)
colors = [plt.cm.Spectral(i/float(len(labels))) for i in range(len(labels))]
# print(df2.index)
# plt.figure(figsize=(12,8),dpi=80)
# squarify.plot(sizes=sizes,label=labels,
#               color=colors,alpha=.8)
# plt.axis('off')
# plt.show()
