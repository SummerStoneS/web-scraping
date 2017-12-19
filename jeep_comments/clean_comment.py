import pandas as pd
import re
import glob

data_filenames = glob.glob('汽车之家comments/*.xlsx')
data = pd.DataFrame()
for i in range(len(data_filenames)):
    data_i = pd.read_excel(data_filenames[i])
    data_i['car_type'] = list(map(lambda x:x.replace('.xlsx',''),data_filenames[i].split('\\')))[1]
    data = pd.concat([data, data_i])


def split_comment(x):
    """
    :param x: 原始的comment
    :return: 把最不满意的，最满意的。。。。分出来
    """
    a = re.split('【', x)
    b = [re.split('】', x) for x in a][1:]
    tuple_comment = [(x[0], x[1]) for x in b if len(x)>1]
    return dict(tuple_comment)

new_columns = pd.DataFrame(list(map(split_comment, data['长评价'].tolist())))
comment_data = pd.concat([data[['car_type','评价时间']].reset_index(drop=True), new_columns.reset_index(drop=True)],axis=1)
comment_data.to_excel('comment_data_all.xlsx',index=False)