import pandas as pd
import re
import glob


def split_comment(x):
    """
    :param x: 原始的comment
    :return: 把最不满意的，最满意的。。。。分出来
    """
    try:
        a = re.split('【', x)
        b = [re.split('】', x) for x in a][1:]
        tuple_comment = [(x[0].strip(), x[1].strip()) for x in b if len(x) > 1]
    except:
        tuple_comment = {}
        print(x)
    return dict(tuple_comment)


def get_excels_queue(file_path='新抓'):
    files_list = glob.glob(file_path + '/*.xlsx')
    return files_list


def get_car_name(file_name):
    # file_name example: 东风本田 - 本田CR - V.xlsx
    car_name = list(map(lambda x: x.replace('.xlsx', ''), file_name.split('\\')))[1]
    return car_name


def concatAllCarTypeComments(folder_name):
    """
    :param folder_name: 存放所有车型原始评论的文件夹名称或路径
    :return: 用于文本分析的excel数据
    """
    data_filenames = get_excels_queue(file_path=folder_name)

    combined_data = pd.DataFrame()

    for i in range(len(data_filenames)):
        data_i = pd.read_excel(data_filenames[i])
        if not "车型" in data_i.columns:
            carType = get_car_name(data_filenames[i])
            data_i["车型"] = carType
        combined_data = pd.concat([combined_data, data_i])
        print(data_filenames[i])
        print(combined_data.shape)
    return combined_data


def convertOneCommentColumnToItems(comment: pd.Series)->pd.DataFrame:
    comments = comment.tolist()
    dictComments = list(map(split_comment, comments))
    commentsToItems = pd.DataFrame(dictComments)
    return commentsToItems


def add_prefix(name_list, prefix):
    prefixed_names = list(map(lambda x: prefix + x, name_list))
    return prefixed_names


def cleanCrawlerData(folder_name):
    data = concatAllCarTypeComments(folder_name)
    new_columns = convertOneCommentColumnToItems(data["长评价"])
    new_columns.columns = add_prefix(new_columns.columns, "评论_")
    updated_comments = pd.concat([data.reset_index(drop=True), new_columns.reset_index(drop=True)], axis=1)
    return updated_comments


if __name__ == '__main__':
    folder = "BX7"
    result = cleanCrawlerData(folder)
    result.to_excel(folder + '/cleanedCrawlerData.xlsx', index=False)