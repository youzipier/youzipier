import pymongo
from selenium import webdriver
from urllib import parse
from lxml import etree

def write_mongo(item):
    db['shangpin'].insert(item)
    print(1111)

def get_html(base_url):

    driver = webdriver.Chrome()
    driver.get(base_url)
    driver.implicitly_wait(10)
    html_str = etree.HTML(driver.page_source)
    driver.close()
    return html_str

def parse_html(html_str):
    li_list = html_str.xpath('//ul[@class="clearfix"]/li[@class=" g_over"]')
    for li in li_list:
        item = {}
        #.当前
        img = li.xpath('./a/img/@src')[0]
        name = li.xpath('./div/div/a/text()')[0]
        xiaoliang = li.xpath('./div/div/span[2]/i/text()')[0]
        pirce = li.xpath('./div/div[3]/span[2]/text()')[0]
        item['img']=img
        item['name']=name
        item['xiaoiang']=xiaoliang
        item['pirce']=pirce
        # print(item)
        # write_mongo(item)

def main():
    url = 'http://www.ppa7.com/kw-%E4%B8%AD%E5%9B%BD%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6%E7%BA%AA%E5%BF%B5%E5%93%81/'
    base_url = parse.unquote(url)
    print(base_url)
    # print(parse.unquote(url))
    html_str = get_html(base_url)
    data = parse_html(html_str)

if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client['jinian']
    main()