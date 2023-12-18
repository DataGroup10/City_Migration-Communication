import pandas as pd
import xlrd

# 加载Excel文件
file_path = '黔东南临近城市.xlsx'  # 请替换为您的文件路径
data = pd.read_excel(file_path, index_col=0)  # 假设第一列为索引列

# 获取总列数
total_columns = len(data.columns)

# 循环处理每7列
for i in range(0, total_columns, 7):
    # 确保不超出列的范围
    end_col = min(i + 7, total_columns)
    week_number = (i // 7) + 1
    column_name = f"第{week_number}周"
    # 计算当前7列的和
    data[column_name] = data.iloc[:, i:end_col].sum(axis=1)

# 展示修改后的数据的前几行
print(data.head())

# 可选：保存处理后的数据到新文件
output_file_path = '黔东南周数据.xlsx'  # 请替换为您希望保存的文件路径
data.to_excel(output_file_path)
