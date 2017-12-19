import pandas as pd

car_name_list = ['Jeep(进口)-大切诺基(进口)', '广汽菲克Jeep-指南者', '广汽菲克Jeep-自由侠', '广汽菲克Jeep-自由侠']


def score_avg(car_name):
    file_name = ''.join(['C:\\Users\\Ruofei Shen\\Desktop\\Jeep\\', car_name, '.xlsx'])
    data = pd.read_excel(file_name, encoding='gbk')
    data['评价年月'] = data['评价时间'].apply(lambda x: x[:-3])
    use_columns = ['评价年月', '内饰', '动力', '外观', '性价比', '操控', '空间', '舒适性']
    avg_data = data[use_columns].groupby('评价年月').mean().reset_index()
    avg_data['车名'] = car_name

