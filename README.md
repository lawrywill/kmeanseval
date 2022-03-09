# kmeanseval
kmeanseval is a lightweight package that wraps around the scikit-learn KMeans model interface to provide users with the ability to easily get within-cluster-sum of squared errors and silhouette scores. This allows users to evaluate K-means clusteirng models without the need for boilerplate code that loops through the creation of multiple models and plots the results.

## Project organization
```
kmeanseval/

	|- .github/
		|- workflows
			|- kmeanseval-ci.yml
	|- data/
		|- movies-metadata-sample.csv
	|- docs/
		|- project_writeup.pdf
	|- examples/
		|- example_usage.ipynb
	|- kmeanseval/
		|- \_\_init\_\_.py
		|- evaluator.py
		|- test_evaluator.py
	|- .coverage
	|- .gitignore
	|- LICENSE.txt
	|- README.md
	|- requirements.txt
	|- setup.py
```

## Usage
Users who wish to evaluate a series of K-means models to choose an ideal k will need to follow these steps:
* Create a KMeansEvaluator object, specifying your data set and the range of k you want to analyze
* Use the get_metrics method from the object to get WSS or silhouette scores in a list
* Use the plot_elbow, plot_silhouette_scores, and plot_avg_silhouette_scores methods to create visualizations for how these metrics vary with k

For an example of this workflow in practice, see [example_usage.ipynb](https://github.com/lawrywill/kmeanseval/blob/master/example_usage.ipynb)

## Installation
1. Clone the kmeanseval repo from github.
2. Navigate to the top level of the directory and install using the command:
```bash
pip install .
```

## Continuous Integration
Pushes to, and pull requests from, the master branch result in tests for flake8 adherance and test coverage through Github Actions.

## License Information
[MIT License](https://github.com/lawrywill/kmeanseval/blob/master/LICENSE.txt)