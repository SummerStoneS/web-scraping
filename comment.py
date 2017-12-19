from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pymongo

url = 'https://k.autohome.com.cn/358/7050/?summarykey=56315&g#pvareaid=2112104'
url = 'https://k.autohome.com.cn/3845/?pvareaid=2099118'      # 指南者

bs_obj = BeautifulSoup(urlopen(url), 'html.parser', from_encoding='gbk')

# 车的名字
car_name = bs_obj.find('div', {'class': 'subnav-title-name'}).get_text().strip()
# 车的评分
score = bs_obj.find('span', {'class': 'font-arial number-fen'}).get_text()

# 这款车的评价标签
tag_list = []
for node in bs_obj.find('div',{'class':'revision-impress impress-small'}).children:
    try:
        tag_list.append(node.get_text())
    except:                                      # 'NavigableString' object has no attribute 'get_text' node中间会有空行
        pass

for node in bs_obj.find('div',{'class':'revision-impress impress-small'}).children:
    if not isinstance(node, NavigableString):
        tag_list.append(node.get_text())

# 质量评价
quality_dim_list = bs_obj.find('div',{'class':'quality-form'}).findChildren('dt')
quality_dim_list = [str(node).strip('</dt>')for node in quality_dim_list]   # ['车身外观', '行驶过程', '功能操作', '电子设备', '座椅', '空调系统', '内饰', '发动机', '变速系统']

quality_dim_num = []
for node in bs_obj.find('div',{'class':'quality-form'}).findChildren('span',{'class':'histogram'}):
    quality_dim_num.append(node.get_text())

quality_dim = list(zip(quality_dim_list, quality_dim_num))

remark = []
for node in bs_obj.find_all('div',{'class':'title-name name-width-01'}):
    try:
        remark.append(node.findChildren('a')[1].get_text())
    except:
        pass


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


every_comment = bs_obj.find_all('div', {'class': 'mouthcon'})                   # 每个人的评价区
list_of_dict = []
for node in every_comment:
    car_dict = {}
    car_dict = get_left_content(node, car_dict)
    car_dict = get_main_comment(node, car_dict)
    list_of_dict.append(car_dict)



attribute = dict(zip(['score','tag','quality','remark','long_remark'],[score,tag_list,quality_dim,remark,long_remark]))
car_dict = dict(car_name=car_name, attribute=attribute)

# 存数据库
client = pymongo.MongoClient()
db = client['car']
collection = db['car_comment']
collection.insert_one(car_dict)