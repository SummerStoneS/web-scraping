from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pandas as pd
import urllib
import os
import time
import re
import requests

# url = 'https://k.autohome.com.cn/3872/?pvareaid=2099118'      # 自由光
# url = 'https://k.autohome.com.cn/3845/?pvareaid=2099118'      # 指南者
# url = 'https://k.autohome.com.cn/4072/?pvareaid=2099118#dataList'  #自由侠
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

sess = requests.Session()
sess.headers = headers
sess.proxies = {
    'http': 'socks5://localhost:1080',
    'https': 'socks5://localhost:1080'
}

def get_comment(url, list_of_dict):
    # req = urllib.request.Request(url)
    # for key, value in headers.items():
    #     req.add_header(key, value)

    # response = urllib.request.urlopen(req)
    # html = response.read()
    html = sess.get(url).content
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
    print("This url is Successful!")

    return car_name, list_of_dict


def find_pages(url):
    html = sess.get(url).content
    bs_obj = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
    find_page_icon = bs_obj.find('span', {'class': 'page-item-info'})
    if find_page_icon:
        # 如果是大于一页的话
        a = find_page_icon.get_text()                       # a='共13页'
        page_num = int(re.sub('[\u4E00-\u9FD5]+', '', a))
    else:
        page_num = 1
    return page_num


def run_main(car_number):
    """
    :param car_number: 车型对应的id，用来加在url里的
    :return: 所有comment
    """
    url_1 = 'https://k.autohome.com.cn/'+str(car_number)+'/?pvareaid=2099118'                  # 某个车型的口碑首页
    if car_number == 4072:
        url_1 = 'https://k.autohome.com.cn/4072/9555/#pvareaid=101484'
    elif car_number == 521:
        url_1 = 'https://k.autohome.com.cn/521/8609/#pvareaid=101484'
    # 判断这个车型的评论有多少页
    page_number = find_pages(url_1)
    if page_number > 1:                 # 页码是否大于一页
        print(page_number)
        if car_number == 4072:          # 4072和521车型的url长得不太一样
            url_more = ['https://k.autohome.com.cn/4072/9555/index_'+str(i)+'.html?GradeEnum=0#dataList' for i in range(2,min(page_number+1,41))]
        elif car_number == 521:
            url_more = ['https://k.autohome.com.cn/521/8609/index_' + str(i) + '.html?GradeEnum=0#dataList' for i in
                        range(2, min(page_number + 1, 41))]
        else:
            url_more = ['https://k.autohome.com.cn/'+str(car_number)+'/index_'+str(i)+'.html?pvareaid=2099118#dataList' for i in range(2, min(page_number+1,41))]  # dataList
        url_list = [url_1] + url_more
    else:                               # 页码只有一页
        url_list = [url_1]

    final = []
    # url_last = ['https://k.autohome.com.cn/3872/9907/index_' + str(i) + '.html?GradeEnum=0' for i in range(10, 14)]
    for url in url_list:
        list_of_dict = []
        try:
            car_name, list_of_dict = get_comment(url, list_of_dict)
        except:
            print('This url crashed')
            print(url)
            continue
        final.extend(list_of_dict)
        print(url)
        time.sleep(30)

    a = pd.concat([pd.Series(x) for x in final], axis=1).T

    file_name = ''.join([car_name, '.xlsx'])
    a.to_excel(file_name)

if __name__ == '__main__':
    # 获取车型的id
    car_id_list = pd.read_excel('normal_car_id.xlsx')
    car_id_list = car_id_list['car_id'].unique()

    for car_id in car_id_list:
        print('现在爬的车id是:')
        print(car_id)
        run_main(car_id)



