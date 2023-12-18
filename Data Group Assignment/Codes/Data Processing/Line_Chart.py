import pandas as pd
import matplotlib.pyplot as plt


# 重新加载处理后的Excel文件进行检查
data_reloaded = pd.read_csv('天津单独_处理后.csv', index_col=0)

# 绘制折线图时，检查数据是否正确转换为数值类型
plt.figure(figsize=(15, 8))

# 遍历每个城市，绘制其每周的数据变化
for city in data_reloaded.index:
    # 确保数据为数值类型
    city_data = pd.to_numeric(data_reloaded.loc[city], errors='coerce')
    plt.plot(city_data.index, city_data, label=city)

plt.title('Trends over time in various categories in TianJin and its neighboring cities')
plt.xlabel('order of weeks')
plt.ylabel('Migratory scale')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
