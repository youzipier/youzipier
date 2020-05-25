import pymongo
from lxml import etree

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_xpath(url):
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="nationTable"]')))
    html_str = etree.HTML(driver.page_source)
    driver.close()
    # print(html)
    return html_str

def write_mongo(item):
    db['country'].insert(item)
    print(1111)

def parse_html(html_str):
    #武汉疫情
    trs = html_str.xpath('//table[@class="VirusTable_1-1-209_3U6wJT"]/tbody[1]/tr')
    for tr in trs:
        item = {}
        try:
            city = tr.xpath('./td[1]/a/div[1]/text()')[0]
            new_add = tr.xpath('./td[2]/text()')[0]
            already = tr.xpath('./td[3]/text()')[0]
            cure = tr.xpath('./td[4]/text()')[0]
            die = tr.xpath('./td[5]/text()')[0]
            item['城市'] = city
            item['新增确诊'] = new_add
            item['累计确诊'] = already
            item['治愈'] = cure
            item['死亡'] = die
            print(item)
            write_mongo(item)
        except Exception:
            pass
    #国内疫情
    tr_list = html_str.xpath('//table[@class="VirusTable_1-1-209_38pQEh"]/tbody[1]/tr')
    # print(tr_list)
    for tr in tr_list:
        item = {}
        try:
            city = tr.xpath('./td[1]//span[2]/text()')[0]
            new_add = tr.xpath('./td[2]/text()')[0]
            already = tr.xpath('./td[3]/text()')[0]
            cure = tr.xpath('./td[4]/text()')[0]
            die = tr.xpath('./td[5]/text()')[0]

            item['城市']=city
            item['新增确诊']=new_add
            item['累计确诊']=already
            item['治愈']=cure
            item['死亡']=die
            print(item)
            write_mongo(item)
        except Exception:
            pass


def main():
    #请求页面
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3'
    html_str = get_xpath(url)
    #解析数据
    parse_html(html_str)
if __name__ == '__main__':
    client = pymongo.MongoClient()
    db = client['yiqing']
    main()