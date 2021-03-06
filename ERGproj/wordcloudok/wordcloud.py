from os import walk, path
import re

import jieba
import jieba.analyse
import codecs
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image

work_path = "Path"
image_name = 'mask.png'
font_name = 'hksnt.ttf'     
data_file = 'total_lyrics.txt'

def generate_wordcloud(data):
    font_path = path.join(work_path, font_name)  # 字体

    color_mask = np.array(Image.open(path.join(work_path, image_name)))     # the shape of the world cloud

    max_words = 20000
    max_font_size = 75
    cloud = WordCloud(font_path=font_path, max_words=max_words, width=3000, height=2000, mask=color_mask,
                      max_font_size=max_font_size, background_color='white',
                      contour_width=3, contour_color='steelblue', random_state=42)

    wordcloud = cloud.generate(text=data)       # data should be string

    image_colors = ImageColorGenerator(color_mask)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3)
    axes[0].imshow(wordcloud, interpolation='bilinear')     # original color
    axes[1].imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')        # recolor
    axes[2].imshow(color_mask, cmap=plt.cm.gray, interpolation='bilinear')      # the mask picture

    wordcloud.to_file(path.join(work_path, 'recolor_{0}_{1}.png'.format(max_words, max_font_size)))     # save to file

    for ax in axes:
        ax.set_axis_off()
    plt.show()


def Seg(data_file):
    f = open("C:\\Users\\dell\\Desktop\\ERGproj\\SentimentAnalysisok\\stopwords.txt", 'r', encoding = 'utf-8-sig')
    stopwords = f.readlines()
    data = []
    lyrics = data_file.split("+")
    for lyr in lyrics:
        lyr = lyr.split("\n")
        for line in lyr:
            line = re.sub("[.\n]", ' ', line)
        lyr = " ".join(lyr)
        data.append(lyr)
    data = " ".join(data)

    local_words = jieba.cut(data, cut_all=False)       # cut the data
    for word in local_words:
        if len(word) > 1 and word != '\r\n' and word not in stopwords:
            words_data.append(word)

    return ' '.join(words_data

generate_wordcloud(words_data)
