"""
Unit tests for the KMeansEvaluator class in evaluator.py
"""

import unittest
import evaluator
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans


class TestKMeansEvaluator(unittest.TestCase):
    """
    Test the KMeansEvaluator class's functions
    """

    def test_instantiation(self):
        """
        Testing that instantiating the KMeansEvaluator results in
        an object containing the correct number of models
        """

        # set number of models and create data
        models = 9
        X, y = make_blobs(n_samples=5000, centers=10,
                          n_features=300, cluster_std=0.001, random_state=123)

        # instantiate KMeansEvaluator
        kme = evaluator.KMeansEvaluator(data=X, k_range=range(2, 11))

        # test whether KMeansEvaluator contains the expected number of models
        self.assertTrue(models == len(kme._models))

    def test_get_metrics(self):
        """
        Testing that get_metrics for wss provides the same values
        we'd get by looping through sklearn models
        """

        # set k range and create data
        k_range = range(2, 11)
        X, y = make_blobs(n_samples=5000, centers=10,
                          n_features=300, cluster_std=0.001, random_state=123)

        # get wss by looping through sklearn models
        wss = []
        for k in k_range:
            model = KMeans(n_clusters=k, random_state=123)
            model.fit_predict(X)
            wss.append(model.inertia_)

        # instantiate evaluator
        kme = evaluator.KMeansEvaluator(data=X, k_range=k_range,
                                        random_state=123)

        # test whether sums of wss are nearly equal
        self.assertAlmostEqual(sum(wss), sum(kme.get_metrics(metric='wss')))

    def test_plot_elbow(self):
        """
        Testing that plot_elbow creates a plot
        """

        plt.close()
        # create data
        X, y = make_blobs(n_samples=5000, centers=10,
                          n_features=300, cluster_std=0.001, random_state=123)

        # instantiate evaluator and create plot
        kme = evaluator.KMeansEvaluator(data=X, k_range=range(2, 11),
                                        random_state=123)
        kme.plot_elbow()

        # assert that one plot was created
        self.assertTrue(plt.gcf().number == 1)

    def test_plot_avg_silhouette_scores(self):
        """
        Testing that plot_avg_silhouette_scores creates a plot
        """

        plt.close()
        # create data
        X, y = make_blobs(n_samples=5000, centers=10,
                          n_features=300, cluster_std=0.001, random_state=123)

        # instantiate evaluator and create plot
        kme = evaluator.KMeansEvaluator(data=X, k_range=range(2, 11),
                                        random_state=123)
        kme.plot_avg_silhouette_scores()

        # assert that one plot was created
        self.assertTrue(plt.gcf().number == 1)

    def test_plot_silhouette_scores(self):
        """
        Testing that plot_silhouette_scores creates the correct
        number of plots
        """

        plt.close()
        models = 9

        # create data
        X, y = make_blobs(n_samples=5000, centers=10,
                          n_features=300, cluster_std=0.001, random_state=123)

        # instantiate evaluator and create plot
        kme = evaluator.KMeansEvaluator(data=X, k_range=range(2, 11),
                                        random_state=123)
        kme.plot_silhouette_scores()

        # assert that one plot was created
        self.assertTrue(plt.gcf().number == models)


if __name__ == "__main__":
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestKMeansEvaluator)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
