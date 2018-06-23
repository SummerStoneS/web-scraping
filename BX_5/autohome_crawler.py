"""
@time: 6/16/2018 2:51 PM

@author: 柚子
"""
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json


config = json.load(open("config.json"))


def get_left_content(node):
    """
    :param node: a full comment area from a user
    :return: a dict of the left part messages
    """
    left_contents = {}
    left_column_items = node.find_elements_by_class_name('choose-dl')
    for line in left_column_items:
        item_name = line.find_element_by_tag_name("dt").text
        left_contents[item_name] = line.find_element_by_tag_name('dd').text.strip()
    return left_contents


def get_title(node):
    title_content = {}
    koubei = node.find_element_by_class_name("title-name")
    datee = koubei.find_element_by_tag_name("b").text
    title_sentence = koubei.find_elements_by_tag_name("a")[1].text
    title_content["评价时间"] = datee
    title_content["口碑"] = title_sentence
    return title_content


def get_full_remark(node):
    """
    :param node:
    :return: 显示全部内容的评论
    """
    long_remarks = {}
    full_content_link_url = node.find_element_by_class_name('allcont').find_element_by_tag_name("a").get_property("href")
    new_browser = webdriver.Chrome()
    new_browser.get(full_content_link_url)
    remarks_list = new_browser.find_elements_by_class_name("mouth-item")
    for item in remarks_list:
        key = '长' + item.find_element_by_class_name("icon").text          # 口碑，追加
        # for script in item.find_elements_by_tag_name('script'):
        #     script.replace_with("")                     # 把脚本全部去除
        remark_content = item.find_element_by_class_name('text-con').text
        cleaned_comment = re.sub(r"[a-zA-Z/:?;{} ()._=+0-9-]+", '', remark_content).strip()
        long_remarks[key] = cleaned_comment
    return long_remarks


def get_right_comment(node):
    right_comment = {}
    right_comment.update(get_title(node))

    # 长评价要到【显示全部内容】里去看
    # car_dict['长评价'] = node.find('div', {'class': 'text-con'}).get_text().strip()
    comment_contents = node.find_element_by_class_name('text-con').text.strip()
    right_comment["长评价"] = comment_contents          # 有人会发布追加评价
    return right_comment


class CommentsCrawler:
    def __init__(self):
        self.car_id = None
        self.car_name = None
        self.browser = webdriver.Chrome()
        self.base_url = 'https://k.autohome.com.cn/'

    def get_first_page_url(self):
        return self.base_url + str(self.car_id) + '/?pvareaid=2099118'

    def get_total_urls(self):
        first_page_url = self.get_first_page_url()
        page_number = self.get_pages_num()
        if page_number > 1:
            url_more = [self.base_url + str(self.car_id) + '/index_' + str(i) + '.html?pvareaid=2099118#dataList'
                        for i in range(2, min(page_number + 1, 41))]  # dataList
        else:
            url_more = []
        urls_list = [first_page_url] + url_more
        return urls_list

    def get_pages_num(self):
        try:
            find_page_icon = self.browser.find_element_by_class_name('page-item-info')
            # 如果是大于一页的话
            pagenum_text = find_page_icon.text                       # a='共13页'
            page_num = int(re.sub('[\u4E00-\u9FD5]+', '', pagenum_text))
        except NoSuchElementException:
            page_num = 1
        return page_num

    def open_first_page(self, car_id):
        self.car_id = car_id
        self.browser.get(self.get_first_page_url())         # 打开首页
        is_carName_exists = self.browser.find_element_by_class_name('subnav-title-name')
        if not is_carName_exists:
            print("车的id：{}".format(self.car_id))
            raise ValueError("页面搜索不到车名")
        else:
            self.car_name = is_carName_exists.text               # 车的名字
            print(self.car_name)

    def crawl_all_pages(self):
        total_urls = self.get_total_urls()
        total_comments = []
        for url in total_urls:
            print(url)
            onePageComments = self.parse_one_page(url)
            total_comments.extend(onePageComments)
            all_comments_df = pd.concat([pd.Series(x) for x in total_comments], axis=1).T
            file_name = ''.join([self.car_name, '.xlsx'])
            all_comments_df.to_excel(file_name)
            time.sleep(config['PageFlipSleep'])

    def parse_one_page(self, url):
        while 1:
            try:
                self.browser.get(url)
                break
            except TimeoutException:
                time.sleep(config['TimeoutReload'])
        all_comments = self.browser.find_elements_by_class_name('mouthcon')  # 页面里所有的用户评论
        comments_list = []
        for node in all_comments:
            comment = {}  # 一条新的记录
            comment.update(get_left_content(node))
            comment.update(get_right_comment(node))
            comment["车型"] = self.car_name
            comments_list.append(comment)
        return comments_list


def verify_if_need(browser):
    """
    :param browser: 浏览器打开窗口
    :return: 如果要验证，点击验证，刷新后应当重新加载之前要访问的页面
    """
    try:
        html_status = browser.find_element_by_class_name("geetest_radar_tip")
        html_status.click()
    except Exception:
        print("no verification need")


if __name__ == '__main__':
    # carType_file = pd.read_excel(r'C:\Users\Ruofei Shen\Desktop\Lowrence_BX5\BX5_cars_id_name.xlsx')
    carType_file = pd.read_excel(r'C:\Users\Ruofei Shen\Desktop\Lowrence_BX5\BX7_cars_id_name.xlsx')
    carType_id_list = list(carType_file['car_id'])
    crawler = CommentsCrawler()
    for carType_id in carType_id_list:
        crawler.open_first_page(carType_id)
        verify_if_need(crawler.browser)
        crawler.crawl_all_pages()
















