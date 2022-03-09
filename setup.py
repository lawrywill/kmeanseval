import setuptools

setuptools.setup(
    name="kmeanseval",
    version="1.0.0",
    author="Ryan Williams",
    author_email="lrw0102@uw.edu",
    description="A package for calculating and plotting evaluation metrics for k-means clustering.",
    url="https://github.com/lawrywill/kmeanseval",
    packages=['kmeanseval'],
    install_requires=[
        'numpy',
        'matplotlib',
        'scikit-learn'
    ],
    keywords=['data science', 'unsupervised learning', 'k-means', 'clustering'],
    classifiers=[
        'Intended Audience :: Decision Scientists, Data Scientists, Business Analysts',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)