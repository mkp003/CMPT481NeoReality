import scipy.stats as stat
import pandas as pd

data = pd.read_csv('../AnalysisResults/design_speeds_dataset.csv')



hex = data["Hexagon"]
circle = data["Circle"]
tube = data["Tube"]

print(stat.mannwhitneyu(hex, circle))
print(stat.mannwhitneyu(hex, tube))
print(stat.mannwhitneyu(circle, tube))
print(stat.mstats.kruskalwallis([hex, circle, tube]))