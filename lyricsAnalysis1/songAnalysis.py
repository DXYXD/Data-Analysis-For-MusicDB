from os import walk, path
import re

import jieba
import jieba.analyse
import codecs
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image

work_path = "D:\\Academic_work\\01_ERG3010\\Project\\lyricsAnalysis1"
image_name = 'mask.jpg'
font_name = 'STFANGSO.TTF'     
data_file = 'total_lyrics.txt'


def hadle_data():
    data = []
    pattern_en = re.compile(r'.*:.*')       # 过滤掉作词作曲等信息
    pattern_cn = re.compile(r'.*：.*')

    for dirpath, dirname, filenames in walk(work_path):
        for file in filenames:
            if file.split('.')[-1] == 'txt':
                with codecs.open(path.join(dirpath, file), 'r', 'utf-8') as f:
                    for line in f:
                        data.append('\n')  # 每首歌之间补上换行
                        if not (pattern_cn.match(line) or pattern_en.match(line) or len(line.strip()) == 0):
                            data.append(line)
                        else:
                            pass
    with codecs.open(path.join(work_path, data_file), 'w', 'utf-8') as f:
        f.write(' '.join(data))


def generate_wordcloud(data):
    font_path = path.join(work_path, font_name)  # 字体

    color_mask = np.array(Image.open(path.join(work_path, image_name)))     # the shape of the world cloud

    max_words = 2000
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

    wordcloud.to_file(path.join(work_path, 'color_{0}_{1}.png'.format(max_words, max_font_size)))     # save to file

    for ax in axes:
        ax.set_axis_off()
    plt.show()


if __name__ == "__main__":
    hadle_data()

    original_data = ""
    words_data = []
    
    with codecs.open(path.join(work_path, data_file), 'rb', 'utf-8') as f:
        original_data = f.read()
        local_words = jieba.cut(original_data, cut_all=False)       # cut the data
        for word in local_words:
            if len(word) > 1 and word != '\r\n':
                words_data.append(word)
    generate_wordcloud(' '.join(words_data))
