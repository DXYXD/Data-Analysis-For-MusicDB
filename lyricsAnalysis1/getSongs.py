# Get a singer's all of lyrics
# Those lyrics are listed in a txt file
import os
onpath = os.getcwd()
nextpath = 'songs_lyrics'

f = open("李健.txt", 'r', encoding = 'utf-8-sig')
for line in f.readlines():
    line = line.strip('\n')
    with open(os.path.join(onpath, nextpath, line+'.txt'), 'r', encoding = 'utf-8-sig',  errors='ignore') as f2:
        lyrics = f2.readlines()
    with open("李健lyrics.txt", 'a', encoding = 'utf-8-sig') as f3:
        f3.writelines(lyrics)