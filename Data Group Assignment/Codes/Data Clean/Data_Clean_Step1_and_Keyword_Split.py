import inline
import matplotlib
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import re
import jieba
import jieba.analyse
#1.从数据库导入微博数据并查看
mblog_frame = pd.read_csv('modified_黔东南.csv',index_col=None,low_memory=False)
mblog_frame.head(2)
# 将content列中的非字符串数据转换为字符串
mblog_frame['content'] = mblog_frame['content'].astype(str)

# 现在应用clean_text函数


# 2.清除text中的非微博正文字符并抽取关键词
# 自定义函数
def clean_text(raw):
    """
    清除text中的非微博正文字符
    返回值类型为元组
    """

    if raw['content']:
        text=re.sub('<[^<]*>','',raw['content']) # 清除多余的html语句
        text=re.sub('[#\n]*','',text) # 清除换行符与#符号
        text=re.sub('(http://.*)$','',text) # 清除文末的网址
        return text
    else:
        return None
def get_chinese_text(raw):
    """
    清除text中的非中文字符
    只能提取中文字符，微博中的数字以及英文均会丢失
    """
    if raw['content']:
        res_text=''.join(re.findall(r"[\u4e00-\u9fff]{2,}",raw['text']))
        return (raw['mid'],res_text)
    else:
        return None

def get_keywords(raw):
    """
    使用jieba从中文text抽取关键词
    默认抽取20个关键词
    longtext 提取40个关键词
    """
    if raw['chinese_text']:
        if raw['isLongText'] == 1:
            # 当text为长文本时，提取50个关键词
            keywords = jieba.analyse.extract_tags(raw['chinese_text'],topK=50)
        else:
            # 当text为非长文本时，默认提取20个关键词
            keywords = jieba.analyse.extract_tags(raw['chinese_text'])
        return (raw['mid'],keywords)
    else:
        return None

# def clean_created_date(raw):
#     created_date = raw['created_at']
#     if created_date.endswith('前'):
#         created_date = '09-15'
#     elif created_date.startswith('昨天'):
#         created_date = '09-14'
#     return created_date
# #获取清理后的created_date
# mblog_frame['created_date'] = mblog_frame.apply(clean_created_date,axis=1)
# 获取清理后的text
mblog_frame['chinese_text'] = mblog_frame.apply(clean_text,axis=1)

# 以传入字典items()的形式生成DataFrame，指定列名
res_mblog = pd.DataFrame(mblog_frame,columns=['mid','chinese_text','like_count','comments_count','reposts_count','created_date','user_id'])
# 写入csv文件便于查看数据清洗结果
res_mblog.to_csv('clean_mblog.csv', encoding='utf_8_sig',index=False)
# 获取关键字并转换为分散存储的DataFrame
mid_with_keyword = list(mblog_frame.apply(get_keywords,axis=1))

# 过滤掉 mid_with_keyword 中的 None 值
mid_with_keyword_filtered = [raw for raw in mid_with_keyword if raw is not None]

# 现在进行列表推导
keywords_list = [(raw[0], w) for raw in mid_with_keyword_filtered for w in raw[1]]


# 这里要把keywords列表存储到数据库，因此需要将keywords列表分开，并与mid对应
# keywords_list = [(raw[0],w) for raw in mid_with_keyword for w in raw[1]]
mid_with_keyword = pd.DataFrame(keywords_list,columns=['mid','keyword'])
# 写入csv文件便于查看结果
mid_with_keyword.to_csv('keyword.csv', encoding='utf_8_sig',index=False)

# # 从数据库读取微博数据
# keyword_frame = pd.read_csv('keyword_淄博.csv',index_col=False)
# # 取出全部的关键词，并生成一个列表
# all_keyword = list(keyword_frame.keyword)
#
# # 使用collections模块中的Counter统计每个关键词出现的次数，Counter返回一个字典，keyword：count
# from collections import Counter
# word_freq_frame = pd.DataFrame(Counter(all_keyword).items())
# word_freq_frame.columns=['word','count']
# top100_freq_word = word_freq_frame.sort_values('count',ascending=0).head(100)
# top100_freq_word_dict=dict(list(top100_freq_word.apply(lambda w:(w['word'],w['count']),axis=1)))
#
# from wordcloud import WordCloud,STOPWORDS
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei']#用来显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来显示负号
# import matplotlib.pyplot as plt
# plt.rcParams['figure.dpi'] = 100 #分辨率
# wc = WordCloud(background_color="white",max_words=2000,font_path='微软雅黑.ttf')
# wc.generate_from_frequencies(top100_freq_word_dict)
# plt.imshow(wc)
# plt.axis('off')
# plt.show()

# import pandas as pd
# import re
#
# # 读取CSV文件
# df = pd.read_csv('keyword_淄博.csv')
#
# # 定义一个正则表达式，匹配仅包含数字、英文和标点符号的字符串
# # 这个正则表达式将匹配那些不包含中文字符的行
# regex = re.compile(r'^[A-Za-z0-9\s\.,;:!?"\'`~@#$%^&*()_+=\-/\\<>{}\[\]|]+$')
#
# # 使用正则表达式过滤数据
# filtered_df = df[df['keyword'].astype(str).str.match(regex)]
#
# print(filtered_df)
# # 可选：将结果保存到新的CSV文件
# filtered_df.to_csv('filtered_keyword_淄博.csv', index=False)

# import pandas as pd
# import re
#
# 读取CSV文件
df = pd.read_csv('keyword_天津.csv')

# 定义一个正则表达式，匹配包含至少一个中文字符的字符串
regex = re.compile(r'[\u4e00-\u9fff]+')

# 使用正则表达式过滤数据，保留包含中文的行
filtered_df = df[df['keyword'].astype(str).str.contains(regex)]

# 查看过滤后的结果
print(filtered_df)

# 将结果保存回原始文件
filtered_df.to_csv('keyword_天津_过滤.csv', index=False)

# import pandas as pd
# from collections import Counter
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
#
# # 读取CSV文件
# keyword_frame = pd.read_csv('keyword_江门.csv', index_col=False)
#
# # 生成关键词列表
# all_keyword = list(keyword_frame.keyword)
#
# # 使用Counter统计关键词频率
# word_freq_frame = pd.DataFrame(Counter(all_keyword).items())
# word_freq_frame.columns = ['word', 'count']
#
# # 提取前100个高频关键词
# top100_freq_word = word_freq_frame.sort_values('count', ascending=False).head(100)
# top100_freq_word_dict = dict(list(top100_freq_word.apply(lambda w: (w['word'], w['count']), axis=1)))
#
# # 设置中文字体和分辨率
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['figure.dpi'] = 100
#
# # 创建词云对象，确保字体路径正确
# wc = WordCloud(background_color="white", max_words=2000, font_path='微软雅黑.ttf')
#
# # 生成词云
# wc.generate_from_frequencies(top100_freq_word_dict)
#
# # 显示词云
# plt.imshow(wc, interpolation='bilinear')
# plt.axis('off')
# plt.show()
