# coding=utf-8

import re
import pandas as pd
from opencc import OpenCC


# 去掉\r \n
def remove(text):
    return text.replace('\n', '').replace('\r', '')


# 去掉链接
def remove_url(text):
    pattern = re.compile(r'[a-zA-Z]*http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    result_text = re.sub(pattern, '', text)
    return result_text


# 繁体转简体
def convert(text):
    openCC1 = OpenCC('tw2s')
    tmp_text = openCC1.convert(text)
    openCC2 = OpenCC('hk2s')
    result_text = openCC2.convert(tmp_text)
    return result_text


# 检测日韩文
def detect_JK(text):
    pattern = re.compile("[\u3040-\u309F\u30A0-\u30FF]|[\u1100-\u11ff\uac00-\ud7af\u3130–\u318F\u3200–\u32FF\uA960–\uA97F\uD7B0–\uD7FF\uFF00–\uFFEF]")
    result = re.search(pattern, text)
    if result is not None:
        return True
    else:
        return False


# 检测日韩文2
def detect_JK2(text):
    JK = re.compile("[\u3040-\u309F\u30A0-\u30FF]|[\u1100-\u11ff\uac00-\ud7af\u3130–\u318F\u3200–\u32FF\uA960–\uA97F\uD7B0–\uD7FF\uFF00–\uFFEF]")
    CH = re.compile(r'[\u4e00-\u9fa5]')

    JK_words = re.findall(JK, text)
    CH_words = re.findall(CH, text)

    if len(JK_words) > len(CH_words):
        return True
    else:
        return False


# 去掉日韩文
def remove_JK(text):
    pattern = re.compile("[\u3040-\u309F\u30A0-\u30FF]|[\u1100-\u11ff\uac00-\ud7af\u3130–\u318F\u3200–\u32FF\uA960–\uA97F\uD7B0–\uD7FF\uFF00–\uFFEF]")
    return re.sub(pattern, '', text)


# 检测英文
def detect_english(text):
    english = re.compile(r'[a-zA-Z]+')
    chinese = re.compile(r'[\u4e00-\u9fa5]')

    english_words = re.findall(english, text)
    chinese_words = re.findall(chinese, text)

    if len(english_words) > len(chinese_words):
        return True
    else:
        return False


# 检测不含日韩文
def detect_no_JK(text):
    pattern = re.compile("[\u3040-\u309F\u30A0-\u30FF]|[\u1100-\u11ff\uac00-\ud7af\u3130–\u318F\u3200–\u32FF\uA960–\uA97F\uD7B0–\uD7FF\uFF00–\uFFEF]")
    words = re.findall(pattern, text)
    if len(words) > 0:
        return False
    else:
        return True


data = pd.read_csv("twitter_key.csv")
print(data.shape)

# data['简体'] = data['内容'].apply(convert)

for i in range(data.shape[0]):
    if type(data.loc[i, '内容']) == type("a"):
        data.loc[i, '内容'] = remove_url(data.loc[i, '内容'])
        data.loc[i, '内容'] = convert(data.loc[i, '内容'])
        if detect_JK2(data['内容'][i]) or detect_english(data['内容'][i]) or detect_no_JK(data['内容'][i]):
            data = data.drop(i, axis=0, inplace=False)

data1 = data.reset_index(drop=True)

print(data1.shape)

data1[['摘要','内容']].to_csv('twitter_data.csv', encoding='utf_8_sig', header=False, index=False, sep='\t')












sentence_list = []
with open('violationNews.json', 'r', encoding='utf-8') as f:
    line = f.readline()
    while line:
        dict = json.loads(line)
        sentence = remove(dict['title'] + " " + dict['content'])
        sentence_list.append(sentence)
        line = f.readline()


label_list = ['涉政'] * 10 + ['涉黄'] * 10 + ['广告'] * 10 + ['正常'] * (len(sentence_list) - 30)


df = pd.DataFrame({'label': label_list, 'sentence': sentence_list})

df.to_csv('violationNews.csv', encoding='utf_8_sig', index=False)















