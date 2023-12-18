import pandas as pd

# 读取CSV文件
df = pd.read_csv("黔东南.csv")

# 检查并处理content列
# 如果content列的字符数大于140，则isLongText为1，否则为0
df['isLongText'] = df['content'].apply(lambda x: 1 if len(str(x)) > 140 else 0)

# 接下来，您可以继续处理df或将其保存回CSV
# 例如，保存修改后的DataFrame到新的CSV文件
df.to_csv("modified_黔东南.csv", index=False)