# Design Specifications for kmeanseval

## Project Background & Motivation
When clustering data using the k-means algorithm, one of the most important decisions to make is how many clusters to use ("k"). This is typically done using within-cluster-sum of squared errors ("WSS") or silhouette scores ("SS"). However, the selection of "k" is subjective and usually involves creating a chart showing how WSS and/or SS change at different values of k. This means that every k-means analysis involves some boilerplate code to loop through the creation of multiple k-means models at different values of k, calculate WSS or SS for them, and finally plot these results.

## Project Idea
The goal of this package is to reduce the amount of boilerplate code that goes into selecting a value for k when using k-means. Rather than creating loops to capture WSS and SS and plot them from scratch, this will be handled by a single function.

## Design Considerations
* Only support k-means clustering, and only support WSS and silhouette scores as evaluation metrics. This simplifies the scope of the project but still provides support for the most common use cases.
* Write code with enough abstraction that additional evaluation metrics for k-means could be added relatively easily at a later point.
* Wrap the scikit-learn k-means functions so that any user familiar with the k-means interface in sklearn will also be familiar with the interface for the kmeanseval functions.
* The end goal of kmeanseval is to provide either a plot or list of cluster evaluation metrics. Plotting functionality will be kept simple since the goal of WSS/SS plots is usually to simply decide on the value of k; users can use the list of values to make more complex plots if desired.

## Usage

### Workflow using kmeanseval to get a list of WSS for k = 1 through 10, and plot those results
from kmeanseval import getmetrics, plotmetrics
import pandas as pd

data = read_csv('data.csv', sep=',')
wss = getmetrics(data, method = 'wss', range = [1, 10])
plotmetrics(data, method = 'wss', range = [1, 10])

### Workflow using scikit-learn and matplotlib to do the same
from sklearn.cluster import KMeans

def calculate_WSS(points, kmax):
  sse = []
  for k in range(1, kmax+1):
    kmeans = KMeans(n_clusters = k).fit(points)
    centroids = kmeans.cluster_centers_
    pred_clusters = kmeans.predict(points)
    curr_sse = 0
    
    for i in range(len(points)):
      curr_center = centroids[pred_clusters[i]]
      curr_sse += (points[i, 0] - curr_center[0]) ** 2 + (points[i, 1] - curr_center[1]) ** 2
      
    sse.append(curr_sse)
  return sse


## Comparison: clusteval (https://pypi.org/project/clusteval/)
clusteval as described on PyPi: "clusteval is a Python package for unsupervised cluster evaluation. Three evaluation methods are implemented that can be used to evalute clusterings; silhouette, dbindex, and derivative. Four clustering methods can be used: agglomerative, kmeans, dbscan and hdbscan."

clusteval differs from kmeans eval:
* clusteval supports agglomerative clustering, dbscan, and hdbscan in addition to kmeans