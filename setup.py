from distutils.core import setup
setup(
  name = 'kmeanseval',
  packages = ['kmeanseval'],
  version = 'v1.0',
  license = 'MIT',
  description = 'This package allows users to calculate and plot within-cluster-sum of squared errors and silhouette scores for k-means clustering.',
  author = 'Ryan Williams',
  author_email = 'lrw0102@uw.edu',
  url = 'https://github.com/lawrywill/kmeanseval',
  keywords = ['data science', 'unsupervised learning', 'k-means', 'clustering'],
  install_requires = [
          'numpy',
          'matplotlib',
          'scikit-learn'
      ],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Decision Scientists, Data Scientists, Business Analysts',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
