# -*- coding: utf-8 -*-
"""РК2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LmOIH0aoGFhgbcUoTw6VgKSVYrSWLJ3i
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from scipy import stats
from IPython.display import Image
from sklearn.datasets import load_wine
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import homogeneity_completeness_v_measure
from sklearn.metrics import silhouette_score
from itertools import cycle, islice
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline 
sns.set(style="ticks")

#Создадим DataFrame для датасета wine
wine = load_wine()
data = pd.DataFrame(data=wine['data'], columns=wine['feature_names'])
data.head()

iris_X = iris.data[:, :2]

boston_x = df_boston['RM'].values
boston_y = df_boston['target'].values

data.info()

data.isnull().sum()

#Построим корреляционную матрицу
fig, ax = plt.subplots(figsize=(15,7))
sns.heatmap(data.corr(method='pearson'), ax=ax, annot=True, fmt='.2f')

X = data

clusters = []

for i in range(1, 11):
    km = KMeans(n_clusters=i).fit(X)
    clusters.append(km.inertia_)
    
fig, ax = plt.subplots(figsize=(6, 4))
sns.lineplot(x=list(range(1, 11)), y=clusters, ax=ax)
ax.set_title('Searching for Elbow')
ax.set_xlabel('Clusters')
ax.set_ylabel('Inertia')

plt.show()

km4 = KMeans(n_clusters=4).fit(X)

X['Labels'] = km4.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', 4))
plt.title('KMeans with 4 Clusters')
plt.show()

km3 = KMeans(n_clusters=3).fit(X)

X['Labels'] = km3.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', 3))
plt.title('KMeans with 3 Clusters')
plt.show()

km8 = KMeans(n_clusters=8).fit(X)

X['Labels'] = km8.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', 8))
plt.title('KMeans with 8 Clusters')
plt.show()

from sklearn.cluster import DBSCAN 

db = DBSCAN(eps=20, min_samples=6).fit(X)

X['Labels'] = db.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', np.unique(db.labels_).shape[0]))
plt.title('DBSCAN with epsilon 20, min samples 6')
plt.show()

db = DBSCAN(eps=30, min_samples=10).fit(X)

X['Labels'] = db.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', np.unique(db.labels_).shape[0]))
plt.title('DBSCAN with epsilon 30, min samples 10')
plt.show()

db = DBSCAN(eps=30, min_samples=6).fit(X)

X['Labels'] = db.labels_
plt.figure(figsize=(12, 8))
sns.scatterplot(X['flavanoids'], X['total_phenols'], hue=X['Labels'], 
                palette=sns.color_palette('hls', np.unique(db.labels_).shape[0]))
plt.title('DBSCAN with epsilon 30, min samples 5')
plt.show()

y= wine.target

from sklearn import metrics
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN

algorithms = []
algorithms.append(KMeans(n_clusters=3, random_state=1))
algorithms.append(DBSCAN(eps=30, min_samples=10))


y= wine.target
data = []
for algo in algorithms:
    algo.fit(X)
    data.append(({
        'ARI': metrics.adjusted_rand_score(y, algo.labels_),
        'AMI': metrics.adjusted_mutual_info_score(y, algo.labels_),
        'Homogenity': metrics.homogeneity_score(y, algo.labels_),
        'Completeness': metrics.completeness_score(y, algo.labels_),
        'V-measure': metrics.v_measure_score(y, algo.labels_),
        'Silhouette': metrics.silhouette_score(X, algo.labels_)}))

results = pd.DataFrame(data=data, columns=['ARI', 'AMI', 'Homogenity',
                                           'Completeness', 'V-measure', 
                                           'Silhouette'],
                       index=['K-means', 'DBSCAN'])

results