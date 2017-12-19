<<<<<<< HEAD
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


def get_comment(url, list_of_dict):

    bs_obj = BeautifulSoup(urlopen(url), 'html.parser', from_encoding='gbk')

    # 车的名字
    car_name = bs_obj.find('div', {'class': 'subnav-title-name'}).get_text().strip()

    every_comment = bs_obj.find_all('div', {'class': 'mouthcon'})                   # 每个人的评价区

    for node in every_comment:
        car_dict = {}
        car_dict = get_left_content(node, car_dict)
        car_dict = get_main_comment(node, car_dict)
        list_of_dict.append(car_dict)

    base_url = 'https://k.autohome.com.cn'

    if bs_obj.find('a', {'class': 'page-item-next'}):
        time.sleep(20)
        next_page_url = urllib.parse.urljoin(base_url, bs_obj.find('a', {'class': 'page-item-next'})['href'])
        list_of_dict.extend(get_comment(next_page_url, list_of_dict))

    return car_name, list_of_dict

if __name__ == '__main__':
    # url = 'https://k.autohome.com.cn/521/?pvareaid=2099118#dataList'  # 大切诺基
    # competitor_data = pd.read_excel('C:\\Users\Ruofei Shen\Desktop\Jeep\竞品车型表.xlsx')
    # for own_car in competitor_data['本品'].unique()[-1:]:
    #     competitor = competitor_data[competitor_data['本品'] == own_car]
    #     competitor_url_list = competitor['网址']
    #     output_directory = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\',own_car])
    #     if not os.path.exists(output_directory):
    #         os.makedirs(output_directory)
    #     for url in competitor_url_list:
    #         list_of_dict = []
    #         car_name, list_of_dict = get_comment(url, list_of_dict)
    #         a = pd.concat([pd.Series(x) for x in list_of_dict], axis=1).T
    #         file_name = ''.join([output_directory, car_name, '.xlsx'])
    #         a.to_excel(file_name)


    url_1 = 'https://k.autohome.com.cn/3872/9907/#pvareaid=101484'
    url_list = ['https://k.autohome.com.cn/3872/9907/index_'+str(i)+'.html?GradeEnum=0' for i in range(2,14)]  # dataList
    for url in url_1 + url_list:
        list_of_dict = []
        car_name, list_of_dict = get_comment(url, list_of_dict)
    a = pd.concat([pd.Series(x) for x in list_of_dict], axis=1).T
    file_name = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\', car_name, '.xlsx'])
    a.to_excel(file_name)
=======
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


def get_comment(url, list_of_dict):

    bs_obj = BeautifulSoup(urlopen(url), 'html.parser', from_encoding='gbk')

    # 车的名字
    car_name = bs_obj.find('div', {'class': 'subnav-title-name'}).get_text().strip()

    every_comment = bs_obj.find_all('div', {'class': 'mouthcon'})                   # 每个人的评价区

    for node in every_comment:
        car_dict = {}
        car_dict = get_left_content(node, car_dict)
        car_dict = get_main_comment(node, car_dict)
        list_of_dict.append(car_dict)

    base_url = 'https://k.autohome.com.cn'

    if bs_obj.find('a', {'class': 'page-item-next'}):
        time.sleep(20)
        next_page_url = urllib.parse.urljoin(base_url, bs_obj.find('a', {'class': 'page-item-next'})['href'])
        list_of_dict.extend(get_comment(next_page_url, list_of_dict))

    return car_name, list_of_dict

if __name__ == '__main__':
    # url = 'https://k.autohome.com.cn/521/?pvareaid=2099118#dataList'  # 大切诺基
    # competitor_data = pd.read_excel('C:\\Users\Ruofei Shen\Desktop\Jeep\竞品车型表.xlsx')
    # for own_car in competitor_data['本品'].unique()[-1:]:
    #     competitor = competitor_data[competitor_data['本品'] == own_car]
    #     competitor_url_list = competitor['网址']
    #     output_directory = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\',own_car])
    #     if not os.path.exists(output_directory):
    #         os.makedirs(output_directory)
    #     for url in competitor_url_list:
    #         list_of_dict = []
    #         car_name, list_of_dict = get_comment(url, list_of_dict)
    #         a = pd.concat([pd.Series(x) for x in list_of_dict], axis=1).T
    #         file_name = ''.join([output_directory, car_name, '.xlsx'])
    #         a.to_excel(file_name)


    url_1 = 'https://k.autohome.com.cn/3872/9907/#pvareaid=101484'
    url_list = ['https://k.autohome.com.cn/3872/9907/index_'+str(i)+'.html?GradeEnum=0' for i in range(2,14)]  # dataList
    for url in url_1 + url_list:
        list_of_dict = []
        car_name, list_of_dict = get_comment(url, list_of_dict)
    a = pd.concat([pd.Series(x) for x in list_of_dict], axis=1).T
    file_name = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\', car_name, '.xlsx'])
    a.to_excel(file_name)
>>>>>>> 9a0ef0c52f26197b955b688d5a8243eba1b9474f
