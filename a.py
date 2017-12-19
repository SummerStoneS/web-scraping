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
    next_page = bs_obj.find('a', {'class': 'page-item-next'})['href']
    if next_page:
        next_page_url = urllib.parse.urljoin(base_url, next_page)
        list_of_dict.extend(get_comment(next_page_url, list_of_dict))


    return list_of_dict