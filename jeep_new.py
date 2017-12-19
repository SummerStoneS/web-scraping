from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pandas as pd
import urllib
import os
import time

# url = 'https://k.autohome.com.cn/3872/?pvareaid=2099118'      # 自由光
# url = 'https://k.autohome.com.cn/3845/?pvareaid=2099118'      # 指南者

# url = 'https://k.autohome.com.cn/4072/?pvareaid=2099118#dataList'        #自由侠
# url = 'https://k.autohome.com.cn/521/?pvareaid=2099118#dataList' # 大切诺基


def get_left_content(node, car_dict):
    '''
    :param node: 每一个评价区
    :return: 评价区左边的东西
    '''
    for line in node.findChildren('dl', 'choose-dl'):
        key_word = line.findChildren('dt')[0].get_text().strip()
        car_dict[key_word] = line.findChildren('dd')[0].get_text().strip()
    return car_dict


def get_main_comment(node, car_dict):
    koubei = node.findChildren('div', {'class': "title-name name-width-01"})
    car_dict['评价时间'] = koubei[0].findChildren('a')[0].get_text()
    car_dict['口碑'] = koubei[0].findChildren('a')[1].get_text()
    car_dict['长评价'] = node.find('div', {'class': 'text-con'}).get_text().strip()
    return car_dict

headers = {
    'Referer': 'https://k.autohome.com.cn/521/8609/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def get_comment(url, list_of_dict):
    req = urllib.request.Request(url)
    for key, value in headers.items():
        req.add_header(key, value)

    response = urllib.request.urlopen(req)
    html = response.read()
    #
    bs_obj = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
    # bs_obj = BeautifulSoup(urlopen(url), 'html.parser', from_encoding='gbk')
    # 车的名字
    car_name = bs_obj.find('div', {'class': 'subnav-title-name'}).get_text().strip()

    every_comment = bs_obj.find_all('div', {'class': 'mouthcon'})                   # 每个人的评价区

    for node in every_comment:
        car_dict = {}
        car_dict = get_left_content(node, car_dict)
        car_dict = get_main_comment(node, car_dict)
        list_of_dict.append(car_dict)

    return car_name, list_of_dict

if __name__ == '__main__':

    url_1 = 'https://k.autohome.com.cn/3845/?pvareaid=2099118'
    url_list = ['https://k.autohome.com.cn/3845/index_'+str(i)+'.html?pvareaid=2099118#dataList' for i in range(2, 33)]  # dataList
    final = []
    # url_last = ['https://k.autohome.com.cn/3872/9907/index_' + str(i) + '.html?GradeEnum=0' for i in range(10, 14)]
    for url in [url_1] + url_list:
    # for url in url_last:
        list_of_dict = []
        car_name, list_of_dict = get_comment(url, list_of_dict)
        final.extend(list_of_dict)
        time.sleep(30)
    a = pd.concat([pd.Series(x) for x in final], axis=1).T
    # file_name = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\', car_name, '1.xlsx'])
    file_name = ''.join([car_name, '.xlsx'])
    a.to_excel(file_name)