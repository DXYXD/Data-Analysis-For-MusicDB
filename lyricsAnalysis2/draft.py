from sentimentAnalysis import Sentiment
from feature_extraction import FeatureExtraction
from svm import SVM
from seg import Seg
import re
import os
root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

datalist = []
with open('D:\\Academic_work\\01_ERG3010\\Project\\lyricAnalysis2\\lijianlyrics2.txt', 'r', encoding='utf-8-sig') as f:
    for line in f:
        line = f.readline()
        if ':' not in line and line != '':
            line = "".join(line.split())
            line = re.sub('[a-zA-Z0-9-+.\n~]', '', line)
            datalist.append(line) 

''' 分词 统计词频  '''
# seg = Seg() 
# seg_datalist = seg.seg_from_datalist(datalist)
# keywords = dict(seg.get_keyword_from_datalist(datalist))
# print(datalist)
# print(seg_datalist)
# print(keywords)

'''  sentiment analysis  '''
word_list = []
lable_list = []
train_data = []
neg_corpus_path = ['negEZ', 'negRZ', 'negNTUSD']
pos_corpus_path = ['posEZ', 'posRZ', 'negNTUSD']
# negative word
for path in neg_corpus_path:
    with open('D:\\Academic_work\\01_ERG3010\\Project\\corpus\\{}{}'.format(path,'.txt'), 'r', encoding = 'utf-8-sig') as fn:
        for word in fn:
            word = fn.readline()
            word = word.strip('\n')
            word_list.append(word)
            lable_list.append('neg')
            train_data.append(('neg', word))
# print(train_data)

# positive word
for path in pos_corpus_path:
    with open('D:\\Academic_work\\01_ERG3010\\Project\\corpus\\{}{}'.format(path,'.txt'), 'r', encoding = 'utf-8-sig') as fn:
        for word in fn:
            word = fn.readline()
            word = word.strip('\n')
            word_list.append(word)
            lable_list.append('pos')
            train_data.append(('pos', word))

fe = FeatureExtraction(word_list, lable_list)
best_words = fe.best_words(1000, False)
svm = SVM(50, best_words)
svm.train_model(train_data[:100])
svm.save_model(root_path + 'model')
result = svm.predict_datalist(datalist)
print(result)
