from collections import Counter, defaultdict
import thulac
import pickle
import os
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
# 歌手页面下 

# 读取歌词
def read_song(file_name):
  song_list = []
  singers_set = set()
  # 逐行读取歌词
  with open(file_name, 'r', encoding = 'utf-8') as f:
    for line in f:
      text_segs = line.split()
      title = text_segs[1]
      singer = text_segs[2]
      song = text_segs[-1]

      singers_set.add(singer)

      # 去除非汉字字符
      valid_char_list = [c for c in poem if '\u4e00' <= c <= '\u9fff' or c == '，' or c == '。']
      validated_song = ''.join(valid_char_list)
      # 按照歌手、标题、内容的格式保存
      song_list.append((singer, title, validated_song))

  return song_list, singers_set

# 对歌曲分词
def cut_song_to_words(song_file, saved_words_file):
    save_dir = os.path.dirname((saved_words_file))
    dumped_file = os.path.join(save_dir, 'song_words_stat_result.pkl')

    char_counter = Counter()  # 字频统计
    vocab = set()  # 词汇库
    word_counter = Counter()  # 词频统计
    genre_counter = defaultdict(Counter)  # 针对每个词性的Counter

    fid_save = open(saved_words_file, 'w', encoding = 'utf-8')
    lex_analyzer = thulac.thulac()  # 分词器
    line_cnt = 0
    with open(song_file, 'r', encoding = 'utf-8') as f:
      for line in f:
        text_segs = line.split()
        singer_counter = text_segs[2]
        singer_counter[singer] += 1

        song = text_segs[-1]
        # 去除非汉字字符
        valid_char_list = [c for c in poem if '\u4e00' <= c <= '\u9fff' or c == '，' or c == '。']
        for char in valid_char_list:
          char_counter[char] += 1

        regularized_song = ''.join(valid_char_list)
        word_genre_pairs = lex_analyzer.cut(regularized_song)

        word_list = []
        for word, genre in word_genre_pairs:
          word_list.append(word)
          vocab.add(word)
          word_counter[word] += 1
          genre_counter[genre][word] += 1

        save_line = ' '.join(word_list)
        fid_save.write(save_line + '\n')

        if line_cnt % 10 == 0:
          print('%d poets processed.' % line_cnt)
        line_cnt += 1

    fid_save.close()
    # 存储下来
    dumped_data = [char_counter, author_counter, vocab, word_counter, genre_counter]
    with open(dumped_file, 'wb') as f:
      pickle.dump(dumped_data, f)

    return char_counter, genre_counter

# 将分词结果转换为向量
def word2vec(words_file):
  save_dir = os.path.dirname((words_file))
  vector_file = os.path.join(save_dir, 'word_vectors.model')

  if os.path.exists(vector_file):
    print('find word vector file, loading directly...')
    model = Word2Vec.load(vector_file)
  else:
    print('calculating word vectors...')
    model = Word2Vec(LineSentence(words_file), size=400, window=3, min_count=10,
                     workers=multiprocessing.cpu_count())
    # 将计算结果存储起来，下次就不用重新计算了
    model.save(vector_file)

  return model

def print_stat_results(char_counter, author_counter, genre_counter, vector_model):
    def print_counter(counter):
        for k, v in counter:
            print(k, v)

    # 基于字的分析
    print('\n\n基于字的分析')
    # 常用字排名
    print('\n常用字排名')
    print_counter(char_counter.most_common(12))
    # 季节排名
    print('\n季节排名')
    for c in ['春', '夏', '秋', '冬']:
        print(c, char_counter[c])
    # 颜色排名
    print('\n颜色排名')
    colors = ['红', '白', '青', '蓝', '绿', '紫', '黑', '黄','翠']
    for c in colors:
        print(c, char_counter[c])
    # 植物排名
    print('\n植物排名')
    plants = ['梅', '兰', '竹', '菊', '松', '柳', '枫', '桃', '梨', '杏']
    for p in plants:
        print(p, char_counter[p])
    # 动物排名
    print('\n动物排名')
    age_animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪','猫']
    for a in age_animals:
        print(a, char_counter[a])

    # 基于词的分析
    print('\n\n基于词的分析')
    # 地名排名
    print('\n地名词排名')
    print_counter(genre_counter['ns'].most_common(10))
    # 时间排名
    print('\n时间词排名')
    print_counter(genre_counter['t'].most_common(10))
    # 场景排名
    print('\n场景词排名')
    print_counter(genre_counter['s'].most_common(10))

    def main():
        # song_path: 原始歌词 来自mysql
        song_path = "C:\\Users\\dell\\Desktop\\ERGproj\\broadTextMining\\lijianlyrics2.txt"
        words_path = "C:\\Users\\dell\\Desktop\\ERGproj\\broadTextMining"
        char_counter, genre_counter = cut_song_to_words(song_path, words_path)
        vector_model = word2vec(args.words_path)

        print_stat_results(char_counter, author_counter, genre_counter, vector_model)


if __name__ == '__main__':
    main()
