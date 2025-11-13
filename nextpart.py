import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('/Users/aubreycall/Desktop/stupidthing/air_quality_dataset.csv')

plt.figure(figsize=(10,5))
plt.bar(df['city'], df['aqi'])
plt.xticks(rotation=75)
plt.ylabel("AQI")
plt.title("AQI Levels by City")
plt.show()

pollutants = ["pm25", "pm10", "o3", "no2", "so2", "co"]
df[pollutants].plot(kind="box", figsize=(10,6))
plt.title("Distribution of Pollutants Across All Cities")
plt.ylabel("Concentration")
plt.show()

import seaborn as sns

plt.figure(figsize=(10,6))
sns.heatmap(df[pollutants + ["aqi"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Between AQI and Pollutants")
plt.show()

df.sort_values("aqi", ascending=False)[["city", "aqi"]]

df[pollutants + ["aqi"]].corr()['aqi'].sort_values(ascending=False)

df.sort_values("pm25", ascending=False)[["city", "pm25"]]
