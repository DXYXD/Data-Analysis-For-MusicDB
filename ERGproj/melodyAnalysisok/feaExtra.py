import subprocess
import csv
import wave
import struct
import numpy as np
import csv
import sys
import os

def read_wav(wav_file):
    """Returns two chunks of sound data from wave file."""
    w = wave.open(wav_file)
    n = 60 * 10000

    # 每一帧的数据数 二进制格式
    if w.getnframes() < n * 2:
        raise ValueError('Wave file too short')

    frames = w.readframes(n)
    # frames.shape = -1, 2
    # frames = frames.T
    wav_data = np.array(struct.unpack('%di' % n, frames), dtype = 'int')
    wav_data.shape = -1, 2
    wav_data = wav_data.T
    wav_data1 = wav_data[0]
    wav_data2 = wav_data[1]
    return wav_data1, wav_data2

def compute_chunk_features(wav_file):
    """Return feature vectors for two chunks of an MP3 file."""
    # Read in chunks of data from WAV file
    wav_data1, wav_data2 = read_wav(wav_file)
    # We'll cover how the features are computed in the next section!
    return features(wav_data1), features(wav_data2)


def moments(x):
    mean = x.mean()
    std = x.var()**0.5
    skewness = ((x - mean)**3).mean() / std**3
    kurtosis = ((x - mean)**4).mean() / std**4
    return [mean, std, skewness, kurtosis]
 
def fftfeatures(wavdata):
    # 傅里叶变化
    f = np.fft.fft(wavdata)
    f = f[2:(int(f.size / 2) + 1)]
    f = abs(f)
    total_power = f.sum()
    f = np.array_split(f, 10)
    return [e.sum() / total_power for e in f]
 
def features(x):
    x = np.array(x)
    f = []
 
    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
 
    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
 
    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
 
    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))
 
    f.extend(fftfeatures(x))
    return f

def main():
    with open("test.csv","w", encoding = 'utf-8-sig',newline='') as csvfile: 
        writer = csv.writer(csvfile)
        #先写入columns_name
        writer.writerow(["artist","name","tag","amp1mean", "amp1std", "amp1skew", "amp1kurt", "amp1dmean", "amp1dstd", "amp1dskew", 
                         "amp1dkurt", "amp10mean", "amp10std", "amp10skew", "amp10kurt", "amp10dmean", "amp10dstd", 
                         "amp10dskew", "amp10dkurt", "amp100mean", "amp100std", "amp100skew", "amp100kurt", 
                         "amp100dmean", "amp100dstd", "amp100dskew", "amp100dkurt", "amp1000mean", "amp1000std", 
                         "amp1000skew", "amp1000kurt", "amp1000dmean", "amp1000dstd", "amp1000dskew", "amp1000dkurt", 
                         "power1", "power2", "power3", "power4", "power5", "power6", "power7", "power8", "power9", "power10"])

        count = 0
        for path, dirs, files in os.walk('D:\\Academic_work\\00_music\\ZWAV'):
            # print(files)
            for f in files:
                wav_file = os.path.join(path, f)
                # Extract the track name (i.e. the file name) plus the names
                # of the two preceding directories. This will be useful
                # later for plotting.
                tail, track = os.path.split(wav_file)
                tail, dir1 = os.path.split(tail)
                tail, dir2 = os.path.split(tail)
                # Compute features. feature_vec1 and feature_vec2 are lists of floating
                # point numbers representing the statistical features we have extracted
                # from the raw sound data.
                try:
                    feature_vec1, feature_vec2 = compute_chunk_features(wav_file)
                except:
                    continue
                artist = f.split('-')[0]
                name = f.split('-')[1] + ' ' + dir1.split('-')[0]
                tag = dir1.split('-')[0]
                feature_vec1 = list(feature_vec1)
                line = [artist, name, tag]
                line = line + feature_vec1
                writer.writerow(line)

            
if __name__ == "__main__":
    main()

# f will be a list of 42 floating point features with the following names:
# amp1mean amp1std amp1skew amp1kurt amp1dmean amp1dstd amp1dskew amp1dkurt amp10mean amp10std amp10skew amp10kurt amp10dmean amp10dstd amp10dskew amp10dkurt amp100mean amp100std amp100skew amp100kurt amp100dmean amp100dstd amp100dskew amp100dkurt amp1000mean amp1000std amp1000skew amp1000kurt amp1000dmean amp1000dstd amp1000dskew amp1000dkurt power1 power2 power3 power4 power5 power6 power7 power8 power9 power10