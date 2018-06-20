import jieba.posseg as pseg
import pandas as pd
import re
import nltk
import os
from typing import Tuple
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


stopwords = [line.rstrip() for line in open('./中文停用词库.txt', 'r', encoding='utf-8')]


def remove_nonChinese_character(sentence):
    sentence = str(sentence)
    pattern = re.compile('[^\u4E00-\u9FD5]+')
    chinese_sentence = pattern.sub('', sentence)             # 去除非中文词，不然分词会有影响
    return chinese_sentence


def line_to_words(line):
    line_with_chinese_only = remove_nonChinese_character(line)
    words_list = pseg.cut(line_with_chinese_only)
    cleaned_words = []
    for word, flag in words_list:
        if word not in stopwords:
            cleaned_words.append(word)
    return ' '.join(cleaned_words)


def neatcut(line):
    """
    :param line: 一条微博
    :return: 去除非中文并分词
    """
    stopwords.extend(customized_stopwords)
    line = str(line)
    wordlist = [pair.word for pair in list(pseg.cut(re.compile('[^\u4E00-\u9FD5]+').sub('', line)))
                if pair.word not in stopwords and len(pair.word) > 1 and pair.flag[0] not in "tfrmpcusdb"]
    return ' '.join(wordlist)


def get_word_list(data, column_name):
    """
    :param column_name: df 的一列 每行是分过词的文本评论内容
    :return: 把同一款车型的同一个评价内容（如【最不满意】)都拼到一起
    """
    word_list = []
    for _, row in data.iterrows():
        word_list += row[column_name].split(' ')
    return word_list


def most_freq_words(data, column='最不满意')->Tuple[list, list]:
    data = data[data[column].notnull()]
    # data['cut_text'] = data[column].apply(line_to_words)
    data['cut_text'] = data[column].apply(neatcut)
    word_list = get_word_list(data, 'cut_text')
    # 统计词频
    fdisk = nltk.FreqDist(word_list)
    common_words = fdisk.most_common(400)
    common_words = [(word, freq) for word, freq in common_words if len(word) > 1]
    words, freqs = zip(*common_words[:200])
    return words, freqs


def multiColumnsHighFrequencyWords(one_carType_data)->pd.DataFrame:
    dict_top_words = {}
    for column_to_analyze in need_wordcloud_columns:
        wordslist, freqlist = most_freq_words(one_carType_data, column=column_to_analyze)
        dict_top_words[column_to_analyze] = wordslist
        dict_top_words[column_to_analyze + "freq"] = freqlist
    multiColumnsWordsFreqs = pd.DataFrame(dict_top_words)
    return multiColumnsWordsFreqs


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def word_cloud(data, my_stopwords, background_image, use_col='comment', max_fontsize=70, save_path='wordcloud.png'):
    """
    :return: 词云图
    """

    background_image = plt.imread(background_image)
    wc = WordCloud(background_color='white',  # 设置背景颜色
                   mask=background_image,  # 设置遮罩图片,控制的是词云的形状，比如说松鼠形状的词云，云朵形状的等等，图清晰点比较好
                   max_words=55,  # 设置最大现实的字数
                   collocations=False,
                   stopwords=STOPWORDS.union(set(my_stopwords)),  # 设置停用词
                   font_path='MSYH.TTF',                          # 设置字体格式，如不设置显示不了中文
                   max_font_size=max_fontsize,  # 设置字体最大值，会自动根据图片大写调整，不同图的60看起来不一样
                   # min_font_size=2,    # 设的比较大的话，小的就不显示了
                   # random_state = 1800,  # 设置有多少种随机生成状态，即有多少种布局方案,横的竖的分布
                   scale=20    # 越大计算越慢，图的大小，不如让底图大点清晰点来得快
                   )

    text = ','.join(map(str, data[use_col]))
    wc.generate(text)
    image_colors = ImageColorGenerator(background_image)
    wc.recolor(color_func=image_colors)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(save_path)
    # wc.to_file("wordcloud.png")
    # plt.show()                        # 显示图片，调参阶段用


def plot_one_car_wordcloud_with_multicolumns(one_carType_data):

    car_type = one_carType_data["车型"].iloc[0]
    imagename = ["不满意", "满意", "完整"]
    fontsize = [110, 110, 110]
    for column_i in range(len(need_wordcloud_columns)):
        background = wordcloud_background_images[column_i]
        column_name = need_wordcloud_columns[column_i]
        img_savename = wordcloud_savepath+"/" + imagename[column_i] + car_type + "_wordcloud" + '.png'
        word_cloud(one_carType_data, customized_stopwords,
                   background, use_col="wordcut_" + column_name, max_fontsize=fontsize[column_i], save_path=img_savename)


def getColumnsCutforWordCloud(one_car_data, runtime=1):
    car_type = one_car_data["车型"].iloc[0]
    if runtime == 1:
        for column in need_wordcloud_columns:
            one_car_data["wordcut_" + column] = one_car_data[column].apply(neatcut)
        one_car_data.to_excel(wordcloud_savepath + "/wordcloud" + car_type + ".xlsx")
    else:
        one_car_data = pd.read_excel(wordcloud_savepath + "/wordcloud" + car_type + ".xlsx")
    return one_car_data


if __name__ == '__main__':

    need_wordcloud_columns = ["评论_最不满意的一点", "评论_最满意的一点", "长评价"]
    wordcloud_background_images = ["unsatisfied_back_image.jpg", "satisfied_back_image.jpg", "fullcomment_back_image.jpg"]
    # wordcloud_background_images = ["unsatisfied_back_image.jpg", "red.jpg",
    #                                "fullcomment_back_image.jpg"]
    customized_stopwords = ["觉得", "好像", "满意", "应该", "感觉", "没有", "nan", "不能", "起来", "有点", "完全",
                            "不到", "不会", "知道", "希望", "可能", "没什么", "东西", "个人", "方面", "看看", "不用",
                            "属于", "考虑", "进去", "舍得", "不错", "看起来", "毫无", "看中", "相比", "取车", "收入",
                            "处于", "重新", "发现", "能够", "想要", "情节", "丰富", "级别", "行驶", "水平", "相比",
                            "接车", "不免有些", "不免", "有些", "回来", "并称", "需要", "有待", "容易"]

    wordfreqs_savepath = "BX5/词频统计"
    wordcloud_savepath="BX5/词云图"
    create_folder(wordfreqs_savepath)
    create_folder(wordcloud_savepath)

    all_carType_data = pd.read_excel("BX5/cleanedCrawlerData.xlsx")
    # for carType in all_carType_data["车型"].unique():
    #     print(carType)
    #     one_car_data = all_carType_data[all_carType_data["车型"] == carType]
    #     words_with_freqs = multiColumnsHighFrequencyWords(one_car_data)
    #     words_with_freqs.to_excel(wordfreqs_savepath + '/' + carType + "高频词统计.xlsx")


    # # 对着满意，不满意，长评价画词云图，用分词后的画
    for carType in all_carType_data["车型"].unique():
        print(carType)
        filter_onecar = all_carType_data[all_carType_data["车型"] == carType]
        one_car = getColumnsCutforWordCloud(filter_onecar, runtime=2)
        plot_one_car_wordcloud_with_multicolumns(one_car)







