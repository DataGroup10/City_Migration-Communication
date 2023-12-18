import pandas as pd
from collections import Counter

# 读取CSV文件
df = pd.read_csv('keyword_天津_过滤.csv')

# 假设词语位于名为 'words' 的列
# 如果词语位于不同的列，请将 'words' 替换为实际的列名
words = df['keyword']

# 统计每个词语的出现频次
word_counts = Counter(words)

# 获取出现频次最高的前100个词语
top_100_words = word_counts.most_common(100)

# 打印结果
for word, frequency in top_100_words:
    print(f"{word}: {frequency}")

pd.DataFrame(top_100_words).to_csv('天津top_100_words.csv', index=False)
