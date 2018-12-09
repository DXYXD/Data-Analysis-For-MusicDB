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





