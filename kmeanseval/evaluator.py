"""
This module defines the KMeansEvaluator class, which is used for calculating and plotting evaluation metrics for
k-means clustering over a range of different k values in order to help select the ideal number of clusters.
"""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class KMeansEvaluator():
    def __init__(self, data, k_range = range(2, 11), **kwargs):
        self._data = data
        self._k_range = k_range
        self._models = self._fit_models(**kwargs)

    def _fit_models(self, **kwargs):
        """
        Private function to to create a dictionary of fitted models for the KMeansEvaluator when it is instantiated.
        Input:
            - metric: "wss", "silhouette_score", or "silhouette_sample" (defaults to "wss")
        Output:
            - models: A dictionary of fitted models in the form of {k: K-means model for K = k} over the range of k
        """

        models = {}
        for k in self._k_range:
            # instantiate and fit the model
            model = KMeans(n_clusters=k, **kwargs)
            model.fit_predict(self._data)
            models.update({k: model})

        return models

    def _generic_plot(self, metric, title, figsize, textsize):
        """
        Private function to create the generic plots used for WSS elbow plots and silhouette score averages.
        Input:
            - k_range: sequence of potential values for k
            - y: y-axis value, either wss or silhouette score
            - title: name of the metric used on which to base the title of the plot
            - figsize: length of width of the plot to produce, based on pyplot 'figsize'
            - textsize: size of text in the plot, based on pyplot 'size'
        Output:
            - A matplotlib pyplot visualizing how the evaluation metric varies over values of k
        """

        plt.figure(figsize=figsize)
        plt.plot(self._k_range, metric, marker='o')
        plt.xlabel('k', size=textsize)
        plt.ylabel(title, size=textsize)
        plt.title(f'{title} for K = {self._k_range[0]} through {self._k_range[-1]}', size=textsize)
        plt.show()

    def get_metrics(self, metric='wss'):
        """
        Function to calculate the desired evaluation metric (wss, silhouette score, or silhouette coefficients)
        for k-means clustering over a range of potential values for k.
        Input:
            - metric: "wss", "silhouette_score", or "silhouette_sample" (defaults to "wss")
        Output:
            - metric_list: The list of values for the chosen evaluation metric over the range of k
        """

        metric_list = []

        # loop through all values of k in the supplied k range
        for k in self._k_range:

            # depending on the method passed, calculate the desired evaluation metric
            if metric == 'wss':
                score = self._models[k].inertia_
            elif metric == 'silhouette_score':
                score = silhouette_score(self._data, self._models[k].labels_)
            elif metric == 'silhouette_sample':
                score = silhouette_samples(self._data, self._models[k].labels_)
            else:  # handle the case where user passes a bad value for 'metric'
                score = self._models[k].inertia_

                # inform user what happened
                if k == min(self._k_range): print("invalid method supplied, defaulting to wss")

            metric_list.append(score)

        return metric_list

    def plot_elbow(self, figsize=(16, 8), textsize=15):
        """
        Function to create an elbow plot of within-cluster-sum of squared errors for k-means clustering over
        a range of potential values for k.
        Input:
            - figsize: length of width of the plot to produce, based on pyplot 'figsize'
            - textsize: size of text in the plot, based on pyplot 'size'
        Output:
            - A matplotlib pyplot visualizing how the evaluation metric varies over values of k
        """

        # calculate the list of evaluation metrics
        metric_list = self.get_metrics(metric = 'wss')

        # plot the values
        self._generic_plot(metric_list, 'Within-cluster-sum of squared errors', figsize, textsize)

    def plot_avg_silhouette_scores(self, figsize=(16, 8), textsize=15):
        """
        Function to create a plot of average silhouette scores for each cluster in k-means clustering over
        a range of potential values for k.
        Input:
            - figsize: length of width of the plot to produce, based on pyplot 'figsize'
            - textsize: size of text in the plot, based on pyplot 'size'
        Output:
            - A matplotlib pyplot visualizing how the evaluation metric varies over values of k
        """

        # calculate the list of evaluation metrics
        metric_list = self.get_metrics(metric = 'silhouette_score')

        # plot the values
        self._generic_plot(metric_list, 'Average silhouette score', figsize, textsize)

    def plot_silhouette_scores(self, figsize = (10, 5), textsize = 12):
        """
        Function to create a plot of silhouette scores for each sample in each cluster in k-means clustering over
        a range of potential values for k.
        Input:
            - figsize: length of width of the plot to produce, based on pyplot 'figsize'
            - textsize: size of text in the plot, based on pyplot 'size'
        Output:
            - A matplotlib pyplot visualizing how the evaluation metric varies over values of k
        """

        for k_clusters in self._k_range:
            fig, ax = plt.subplots(figsize = figsize)


            # The silhouette coefficient can range from -1, 1
            ax.set_xlim([-1, 1])

            # Inserting blank space between silhouette plots of individual clusters
            ax.set_ylim([0, len(self._data) + (k_clusters + 1) * 10])

            # get model to use
            cluster_labels = self._models[k_clusters].labels_

            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(self._data, cluster_labels)

            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(self._data, cluster_labels)

            y_lower = 10
            for i in range(k_clusters):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

                ith_cluster_silhouette_values.sort()

                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.nipy_spectral(float(i) / k_clusters)
                ax.fill_betweenx(
                    np.arange(y_lower, y_upper),
                    0,
                    ith_cluster_silhouette_values,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.7,
                )

                # Label the silhouette plots with their cluster numbers at the middle
                ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                # Compute the new y_lower for next plot
                y_lower = y_upper + 10  # 10 for the 0 samples

            ax.set_title(f"Silhouette plot for the various clusters for k = {k_clusters}", size = textsize)
            ax.set_xlabel("Silhouette coefficient values", size = textsize)
            ax.set_ylabel("Cluster label", size = textsize)

            # The vertical line for average silhouette score of all the values
            ax.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax.set_yticks([])  # Clear the yaxis labels / ticks
            ax.set_xticks([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.show()