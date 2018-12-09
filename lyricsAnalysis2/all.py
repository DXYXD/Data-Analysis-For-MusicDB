'''

all lyrics of Lijian

'''

import csv  
import requests
from bs4 import BeautifulSoup
import re
import json

def get_html(url):
    proxy_addr = {'http': '61.135.217.7:80'}
    # 用的代理 ip，如果被封的，在http://www.xicidaili.com/换一个
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, proxies=proxy_addr).text
        return html
    except BaseException:
        print('request error')
        pass

def get_song_infos(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    info = soup.select('#song-list-pre-cache .f-hide a')
    songname = []
    songids = []
    for sn in info:
        songnames = sn.getText()
        songname.append(songnames)
    for si in info:
        songid = str(re.findall('href="(.*?)"', str(si))).strip().split('=')[-1].split('\'')[0]    # 用re查找，查找对象一定要是str类型
        songids.append(songid)
    # print(songname, songids)
    return zip(songname, songids)

def get_lyrics(songids):
    try:
        url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(songids)
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        html = requests.get(url, headers=headers).text
        json_obj = json.loads(html)
        initial_lyric = json_obj['lrc']['lyric']
        reg = re.compile(r'\[.*\]')
        lyric = re.sub(reg, '', initial_lyric).strip()
        return lyric
    except:
        lyric = url
        return lyric

def save2txt(songname, lyric):
    print('正在保存歌曲：{}'.format(songname))
    songname = songname.replace('/', '1')
    songname = songname.replace(' ','')
    songname = songname.replace('-', '')
    songname = songname.replace('"', '_')
    try:
        with open('D:\\Academic_work\\01_ERG3010\\Project\\lyricAnalysis2\\lijianlyrics2.txt', 'a', encoding='utf-8') as f:
            f.write("\n+" + songname + '\n')
            f.write(lyric)
    except:
        return 

if __name__ == '__main__':
    album_id = [39792229, 39723736, 38299153, 37099186, 37029362, 36784319, 35420188, 34921171, 34670170,
                3266696, 3233232, 2615004, 10887, 2261090, 10888, 10892, 10894, 34555224, 3068016, 10897, 10901, 
                10903, 10906, 10908, 10912, 10916, 10921]
    for aid in album_id:
        album_url = 'https://music.163.com/album?id={}'.format(aid) 
        html = get_html(album_url)
        song_infos = get_song_infos(html)
        songs = []
        for song_info in song_infos:
            if song_info[1] not in songs:
                songs.append(song_info[1])
                lyric = get_lyrics(song_info[1])
                save2txt(song_info[0], lyric)
len(songs)