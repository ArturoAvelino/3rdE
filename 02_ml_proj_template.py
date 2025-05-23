# My main template for end-to-end ml projects based on Ch2.

from pathlib import Path
import pandas as pd
import tarfile
import urllib.request

def load_housing_data():
    tarball_path = Path("datasets/housing.tgz")
    if not tarball_path.is_file():
        Path("datasets").mkdir(parents=True, exist_ok=True)
        url = "https://github.com/ageron/data/raw/main/housing.tgz"
        urllib.request.urlretrieve(url, tarball_path)
    with tarfile.open(tarball_path) as housing_tarball:
            housing_tarball.extractall(path="datasets")
    return pd.read_csv(Path("datasets/housing/housing.csv"))

housing = load_housing_data()
# print("housing.head()\n", housing.head())
#     longitude  latitude  ...  median_house_value  ocean_proximity
# 0    -122.23     37.88  ...            452600.0         NEAR BAY
# 1    -122.22     37.86  ...            358500.0         NEAR BAY
# 2    -122.24     37.85  ...            352100.0         NEAR BAY
# 3    -122.25     37.85  ...            341300.0         NEAR BAY
# 4    -122.25     37.85  ...            342200.0         NEAR BAY
# [5 rows x 10 columns]


# print("\nhousing.info()\n",housing.info())
# RangeIndex: 20640 entries, 0 to 20639
# Data columns (total 10 columns):
#  #   Column              Non-Null Count  Dtype
# ---  ------              --------------  -----
#  0   longitude           20640 non-null  float64
#  1   latitude            20640 non-null  float64
#  2   housing_median_age  20640 non-null  float64
#  3   total_rooms         20640 non-null  float64
#  4   total_bedrooms      20433 non-null  float64
#  5   population          20640 non-null  float64
#  6   households          20640 non-null  float64
#  7   median_income       20640 non-null  float64
#  8   median_house_value  20640 non-null  float64
#  9   ocean_proximity     20640 non-null  object
# dtypes: float64(9), object(1)
# memory usage: 1.6+ MB


# print("\nhousing.describe()\n", housing.describe())
#            longitude      latitude  ...  median_income  median_house_value
# count  20640.000000  20640.000000  ...   20640.000000        20640.000000
# mean    -119.569704     35.631861  ...       3.870671       206855.816909
# std        2.003532      2.135952  ...       1.899822       115395.615874
# min     -124.350000     32.540000  ...       0.499900        14999.000000
# 25%     -121.800000     33.930000  ...       2.563400       119600.000000
# 50%     -118.490000     34.260000  ...       3.534800       179700.000000
# 75%     -118.010000     37.710000  ...       4.743250       264725.000000
# max     -114.310000     41.950000  ...      15.000100       500001.000000
# [8 rows x 9 columns]

# ----------------------------------------------------------------------------80
# Plotting setup

# The following cell creates the
# images/end_to_end_project folder (if it doesn't already exist), and it
# defines the save_fig() function which is used through this notebook to
# save the figures in high-res for the book.
import matplotlib.pyplot as plt


# extra code – code to save the figures as high-res PNGs for the book
IMAGES_PATH = Path() / "images" / "02_end_to_end_project"
IMAGES_PATH.mkdir(parents=True, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = IMAGES_PATH / f"{fig_id}.{fig_extension}"
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

# extra code – the next 5 lines define the default font sizes
plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

"""
# Plotting
housing.hist(bins=50, figsize=(12, 8))
save_fig("attribute_histogram_plots")  # extra code
plt.show()"""

# ----------------------------------------------------------------------------80
# Stratified sampling

import numpy as np


housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                               labels=[1, 2, 3, 4, 5])

# Plotting
#c housing["income_cat"].value_counts().sort_index().plot.bar(rot=0, grid=True)
#c plt.xlabel("Income category")
#c plt.ylabel("Number of districts")
#c save_fig("housing_income_cat_bar_plot")  # extra code
#c plt.show()


from sklearn.model_selection import train_test_split

# For most of the ML models use this stratified split.
#c strat_train_set, strat_test_set = train_test_split(
#c     housing, test_size=0.2, stratify=housing["income_cat"], random_state=42)

# For Support Vector Machine (svm) use this split. It create a smaller training
# datasets becaust svm takes a lot of time to be trained.
strat_train_set, strat_test_set = train_test_split(
    housing, train_size=2000, test_size=0.2,
    stratify=housing["income_cat"], random_state=42)

#c print("\nstrat_train_set.info():\n", strat_train_set.info())
# <class 'pandas.core.frame.DataFrame'>
# Index: 2000 entries, 6906 to 12504
# Data columns (total 11 columns):
#  #   Column              Non-Null Count  Dtype
# ---  ------              --------------  -----
#  0   longitude           2000 non-null   float64
#  1   latitude            2000 non-null   float64
#  2   housing_median_age  2000 non-null   float64
#  3   total_rooms         2000 non-null   float64
#  4   total_bedrooms      1978 non-null   float64
#  5   population          2000 non-null   float64
#  6   households          2000 non-null   float64
#  7   median_income       2000 non-null   float64
#  8   median_house_value  2000 non-null   float64
#  9   ocean_proximity     2000 non-null   object
#  10  income_cat          2000 non-null   category
# dtypes: category(1), float64(9), object(1)
# memory usage: 174.0+ KB

#c print("\nstrat_test_set.info():\n", strat_test_set.info())
# <class 'pandas.core.frame.DataFrame'>
# Index: 4128 entries, 16524 to 10768
# Data columns (total 11 columns):
#  #   Column              Non-Null Count  Dtype
# ---  ------              --------------  -----
#  0   longitude           4128 non-null   float64
#  1   latitude            4128 non-null   float64
#  2   housing_median_age  4128 non-null   float64
#  3   total_rooms         4128 non-null   float64
#  4   total_bedrooms      4091 non-null   float64
#  5   population          4128 non-null   float64
#  6   households          4128 non-null   float64
#  7   median_income       4128 non-null   float64
#  8   median_house_value  4128 non-null   float64
#  9   ocean_proximity     4128 non-null   object
#  10  income_cat          4128 non-null   category
# dtypes: category(1), float64(9), object(1)
# memory usage: 359.0+ KB

# the income category proportions in the training set:
strat_train_ratio = strat_train_set["income_cat"].value_counts() / len(strat_train_set)

# the income category proportions in the test set:
strat_test_ratio = strat_test_set["income_cat"].value_counts() / len(strat_test_set)

# Print the result to verify that the stratified sampling is done
# print(strat_train_ratio)
# income_cat
# 3    0.350594
# 2    0.318859
# 4    0.176296
# 5    0.114462
# 1    0.039789
# Name: count, dtype: float64

# print(strat_test_ratio)
# income_cat
# 3    0.350533
# 2    0.318798
# 4    0.176357
# 5    0.114341
# 1    0.039971
# Name: count, dtype: float64

# You won’t use the income_cat column again, so you might as well drop it,
# reverting the data back to its original state:
for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)

# Since you’re going to experiment with various transformations of the full
# training set, you should make a copy of the original so you can revert to
# it afterwards:
#c housing = strat_train_set.copy()

# --------------------------------------------------------60
# # Discover and Visualize the Data to Gain Insights


# Visualizing Geographical Data
#pl housing.plot(kind="scatter", x="longitude", y="latitude", grid=True, alpha=0.2)
#pl save_fig("better_visualization_plot")  # extra code
#pl plt.show()

#pl housing.plot(kind="scatter", x="longitude", y="latitude", grid=True,
#pl              s=housing["population"] / 100, label="population",
#pl              c="median_house_value", cmap="jet", colorbar=True,
#pl              legend=True, sharex=False, figsize=(10, 7))
#pl save_fig("housing_prices_scatterplot")  # extra code
#pl plt.show()

# --------------------------30
# # Looking for Correlations

# Print and plot the correlations between the attributes.
# Explore what attributes have a stronger correlation with the
# target feature, "median_house_value".

# Note: since Pandas 2.0.0, the `numeric_only` argument defaults to
# `False`, so we need to set it explicitly to True to avoid an
# error.
#c corr_matrix = housing.corr(numeric_only=True)
#c print(corr_matrix["median_house_value"].sort_values(ascending=False))
#c print(" ") # whiteline
# median_house_value    1.000000
# median_income         0.688380
# total_rooms           0.137455
# housing_median_age    0.102175
# households            0.071426
# total_bedrooms        0.054635
# population           -0.020153
# longitude            -0.050859
# latitude             -0.139584
# Name: median_house_value, dtype: float64


#c from pandas.plotting import scatter_matrix

# attributes = ["median_house_value", "median_income", "total_rooms",
#               "housing_median_age"]
# scatter_matrix(housing[attributes], figsize=(12, 8))
# save_fig("scatter_matrix_plot")  # extra code
# plt.show()
#
# # Scatter plot the "median_income" and "median_house_value" to
# # better explore the correlation
# housing.plot(kind="scatter", x="median_income", y="median_house_value",
#              alpha=0.1, grid=True)
# save_fig("income_vs_house_value_scatterplot")  # extra code
# plt.show()

# --------------------------30
# Experimenting with Attribute Combinations

#c housing["rooms_per_house"] = housing["total_rooms"] / housing["households"]
#c housing["bedrooms_ratio"] = housing["total_bedrooms"] / housing["total_rooms"]
#c housing["people_per_house"] = housing["population"] / housing["households"]

#c corr_matrix = housing.corr(numeric_only=True)
#c print(corr_matrix["median_house_value"].sort_values(ascending=False))
#c print(" ") # whiteline
# median_house_value    1.000000
# median_income         0.688380
# rooms_per_house       0.143663 <---
# total_rooms           0.137455
# housing_median_age    0.102175
# households            0.071426
# total_bedrooms        0.054635
# population           -0.020153
# people_per_house     -0.038224 <---
# longitude            -0.050859
# latitude             -0.139584
# bedrooms_ratio       -0.256397 <---
# Name: median_house_value, dtype: float64

# --------------------------------------------------------60
# 4. Prepare the Data for Machine-Learning Algorithms

# Let's revert to the original training set and separate the target (note
# that `strat_train_set.drop()` creates a copy of `strat_train_set` without
# the column, it doesn't actually modify `strat_train_set` itself, unless
# you pass `inplace=True`):
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# --------------------------30

# Data Cleaning

# ------------
# Missing values. Imputation

# ------------
# Drop some outliers:

#c from sklearn.ensemble import IsolationForest

#c isolation_forest = IsolationForest(random_state=42)
#c outlier_pred = isolation_forest.fit_predict(X)

#c outlier_pred

# If you wanted to drop outliers, you would run the following code:
#c housing = housing.iloc[outlier_pred == 1]
#c housing_labels = housing_labels.iloc[outlier_pred == 1]

# ------------
# Handling Text and Categorical Attributes


# ------------
# Feature Scaling and transformations

# Exploring the logarithm transformation of data distributed with long tail
# to find out if it gets into a more bell-shape distribution after the
# transformation.
# Figure 2–17 -->
#c fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
#c housing["population"].hist(ax=axs[0], bins=50)
#c housing["population"].apply(np.log).hist(ax=axs[1], bins=50)
#c axs[0].set_xlabel("Population")
#c axs[1].set_xlabel("Log of population")
#c axs[0].set_ylabel("Number of districts")
#c save_fig("long_tail_population")
# plt.show()
# These plots are primarily -histograms-. So the y-axis label “Number of
# districts” highlights that the histogram is counting the recurrence of
# events or number of times that the population attribute has certain
# number of instances with a value in a given range, and that number of
# instances are the “Number of districts”.
# <-- Figure 2–17

# Plot the transformed "median_income" attribute
#c fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
#c housing["median_income"].hist(ax=axs[0], bins=50)
#c housing["median_income"].apply(np.log).hist(ax=axs[1], bins=50)
#c axs[0].set_xlabel("median_income")
#c axs[1].set_xlabel("Log of median_income")
#c axs[0].set_ylabel("Number of districts")
#c save_fig("long_tail_median_income")
# plt.show()

# Plot the transformed "total_bedrooms" attribute
#c fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
#c housing["total_bedrooms"].hist(ax=axs[0], bins=50)
#c housing["total_bedrooms"].apply(np.log).hist(ax=axs[1], bins=50)
#c axs[0].set_xlabel("total_bedrooms")
#c axs[1].set_xlabel("Log of total_bedrooms")
#c axs[0].set_ylabel("Number of districts")
#c save_fig("long_tail_total_bedrooms")
# plt.show()

# Plot the transformed "total_rooms" attribute
#c fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
#c housing["total_rooms"].hist(ax=axs[0], bins=50)
#c housing["total_rooms"].apply(np.log).hist(ax=axs[1], bins=50)
#c axs[0].set_xlabel("total_rooms")
#c axs[1].set_xlabel("Log of total_rooms")
#c axs[0].set_ylabel("Number of districts")
#c save_fig("long_tail_total_rooms")
# plt.show()

# Plot the transformed "households" attribute
#c fig, axs = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
#c housing["households"].hist(ax=axs[0], bins=50)
#c housing["households"].apply(np.log).hist(ax=axs[1], bins=50)
#c axs[0].set_xlabel("households")
#c axs[1].set_xlabel("Log of households")
#c axs[0].set_ylabel("Number of districts")
#c save_fig("long_tail_households")
# plt.show()


# Bucketizing.
# What if we replace each value with its percentile?

# extra code – just shows that we get a uniform distribution
#c percentiles = [np.percentile(housing["median_income"], p)
#c                for p in range(1, 100)]
#c flattened_median_income = pd.cut(housing["median_income"],
#c                                  bins=[-np.inf] + percentiles + [np.inf],
#c                                  labels=range(1, 100 + 1))

#pl flattened_median_income.hist(bins=50)
#pl plt.xlabel("Median income percentile")
#pl plt.ylabel("Number of districts")
#pl save_fig("bucketizing_median_income")
#pl plt.show()
# Note: incomes below the 1st percentile are labeled 1, and incomes above the
# 99th percentile are labeled 100. This is why the distribution below ranges
# from 1 to 100 (not 0 to 100).

# --------------------------30
# RBF to transform multimodal distributions

#c from sklearn.metrics.pairwise import rbf_kernel

#c age_simil_35 = rbf_kernel(housing[["housing_median_age"]], [[35]], gamma=0.1)

# Figure 2–18. It is a histogram.

# # - The `rbf_kernel` function calculates the similarity between each
# district's median age (from `housing["housing_median_age"]`) and the
# target value `35` (in years).
# # - `gamma=0.1` controls the "spread" of the similarity function. A
# higher gamma value leads to more localized similarity (a sharper peak
# around 35), while a lower gamma leads to broader similarity across
# values.
# # - The result (`age_simil_35`) is an array of similarity scores.

#c ages = np.linspace(housing["housing_median_age"].min(),
#c                    housing["housing_median_age"].max(),
#c                    500).reshape(-1, 1)
#c gamma1 = 0.1
#c gamma2 = 0.03
#c rbf1 = rbf_kernel(ages, [[35]], gamma=gamma1)
#c rbf2 = rbf_kernel(ages, [[35]], gamma=gamma2)

#c fig, ax1 = plt.subplots()

#c ax1.set_xlabel("Housing median age")
#c ax1.set_ylabel("Number of districts")
#c ax1.hist(housing["housing_median_age"], bins=50)

#c ax2 = ax1.twinx()  # create a twin axis that shares the same x-axis
#c color = "blue"
#c ax2.plot(ages, rbf1, color=color, label="gamma = 0.10")
#c ax2.plot(ages, rbf2, color=color, label="gamma = 0.03", linestyle="--")
#c ax2.tick_params(axis='y', labelcolor=color)
#c ax2.set_ylabel("Age similarity", color=color)

#c plt.legend(loc="upper left")
#c save_fig("RBF_age_similarity")
# plt.show()

# --------------------------30
# Custom Transformers

# This code creates a ClusterSimilarity transformer, setting the number of
# clusters to 10. Then it calls fit_transform() with the latitude and
# longitude of every district in the training set, weighting each district
# by its median house value. The transformer uses k-means to locate the
# clusters, then measures the Gaussian RBF similarity between each district
# and all 10 cluster centers. The result is a matrix with one row per
# district, and one column per cluster.

# ---> Version proposed by the AI Assistance of PyCharm to fix an issue when
# the using "HalvingRandomSearchCV()" for hyperparameter tunning.
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel


class ClusterSimilarity(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state

    def fit(self, x, y=None, sample_weight=None):
        # Dynamically adjust n_clusters if there are fewer samples than clusters
        n_samples = x.shape[0]
        effective_n_clusters = min(self.n_clusters, n_samples)
        if effective_n_clusters != self.n_clusters:
            print(
                f"Warning: Adjusting number of clusters from {self.n_clusters} "
                f"to {effective_n_clusters}"
                f"to match the available number of samples ({n_samples}).")
        self.n_clusters = effective_n_clusters

        self.kmeans_ = KMeans(self.n_clusters, n_init=10,
                              random_state=self.random_state)
        self.kmeans_.fit(x, sample_weight=sample_weight)
        return self  # Always return self!

    def transform(self, x):
        return rbf_kernel(x, self.kmeans_.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, names=None):
        return [f"Cluster {i} similarity" for i in range(self.n_clusters)]
# <---

# ---> Original version by Aurélien Géron. It works well, except when trying
# to use it for hyperparameter tuning using "HalvingRandomSearchCV()".

#old from sklearn.base import BaseEstimator, TransformerMixin
#old from sklearn.cluster import KMeans
#old from sklearn.metrics.pairwise import rbf_kernel
#old class ClusterSimilarity(BaseEstimator, TransformerMixin):
#old     def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
#old         self.n_clusters = n_clusters
#old         self.gamma = gamma
#old         self.random_state = random_state
#old
#old     def fit(self, x, y=None, sample_weight=None):
#old         self.kmeans_ = KMeans(self.n_clusters, n_init=10,
#old                               random_state=self.random_state)
#old         self.kmeans_.fit(x, sample_weight=sample_weight)
#old         return self  # always return self!
#old
#old     def transform(self, x):
#old         return rbf_kernel(x, self.kmeans_.cluster_centers_, gamma=self.gamma)
#old
#old     def get_feature_names_out(self, names=None):
#old         return [f"Cluster {i} similarity" for i in range(self.n_clusters)]
# <---

# ---> Fig. 2-29
#c cluster_simil = ClusterSimilarity(n_clusters=10, gamma=1., random_state=42)
#c similarities = cluster_simil.fit_transform(housing[["latitude", "longitude"]],
#c                                            sample_weight=housing_labels)

#c housing_renamed = housing.rename(columns={
#c     "latitude": "Latitude", "longitude": "Longitude",
#c     "population": "Population",
#c     "median_house_value": "Median house value (ᴜsᴅ)"})
#c housing_renamed["Max cluster similarity"] = similarities.max(axis=1)

#c housing_renamed.plot(kind="scatter", x="Longitude", y="Latitude", grid=True,
#c                      s=housing_renamed["Population"] / 100, label="Population",
#c                      c="Max cluster similarity",
#c                      cmap="jet", colorbar=True,
#c                      legend=True, sharex=False, figsize=(10, 7))
#c plt.plot(cluster_simil.kmeans_.cluster_centers_[:, 1],
#c          cluster_simil.kmeans_.cluster_centers_[:, 0],
#c          linestyle="", color="black", marker="X", markersize=20,
#c          label="Cluster centers")
#c plt.legend(loc="upper right")
#c save_fig("district_cluster_plot")
# plt.show() # <---

# ------------------------------------------------------------------70
# Pipelines

def monkey_patch_get_signature_names_out():
    """Monkey patch some classes which did not handle get_feature_names_out()
       correctly in Scikit-Learn 1.0.*."""
    from inspect import Signature, signature, Parameter
    # import pandas as pd # Not actually used in this function definition
    from sklearn.impute import SimpleImputer
    # from sklearn.pipeline import make_pipeline, Pipeline # Not actually used in this function
    from sklearn.preprocessing import FunctionTransformer, StandardScaler

    default_get_feature_names_out = StandardScaler.get_feature_names_out

    if not hasattr(SimpleImputer, "get_feature_names_out"):
      print("Monkey-patching SimpleImputer.get_feature_names_out()")
      SimpleImputer.get_feature_names_out = default_get_feature_names_out

    if not hasattr(FunctionTransformer, "get_feature_names_out"):
        print("Monkey-patching FunctionTransformer.get_feature_names_out()")
        orig_init = FunctionTransformer.__init__
        orig_sig = signature(orig_init)

        def __init__(*args, feature_names_out=None, **kwargs):
            orig_sig.bind(*args, **kwargs)
            orig_init(*args, **kwargs)
            args[0].feature_names_out = feature_names_out

        __init__.__signature__ = Signature(
            list(signature(orig_init).parameters.values()) + [
                Parameter("feature_names_out", Parameter.KEYWORD_ONLY)])

        def get_feature_names_out(self, names=None):
            if callable(self.feature_names_out):
                return self.feature_names_out(self, names)
            assert self.feature_names_out == "one-to-one"
            return default_get_feature_names_out(self, names)

        FunctionTransformer.__init__ = __init__
        FunctionTransformer.get_feature_names_out = get_feature_names_out

monkey_patch_get_signature_names_out()

# --------------------------30
# The main functions and pipeline

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_selection import SelectFromModel


cat_pipeline = make_pipeline(
    SimpleImputer(strategy="most_frequent"),
    OneHotEncoder(handle_unknown="ignore"))

def column_ratio(x):
    return x[:, [0]] / x[:, [1]]

def ratio_name(function_transformer, feature_names_in):
    return ["ratio"]  # feature names out

def ratio_pipeline():
    return make_pipeline(
        SimpleImputer(strategy="median"),
        FunctionTransformer(column_ratio, feature_names_out=ratio_name),
        StandardScaler())

log_pipeline = make_pipeline(
    SimpleImputer(strategy="median"),
    FunctionTransformer(np.log, feature_names_out="one-to-one"),
    StandardScaler())
cluster_simil = ClusterSimilarity(n_clusters=10, gamma=1., random_state=42)
default_num_pipeline = make_pipeline(SimpleImputer(strategy="median"),
                                     StandardScaler())
# Defining the main pipeline:
preprocessing = ColumnTransformer([
        ("bedrooms", ratio_pipeline(), ["total_bedrooms", "total_rooms"]),
        ("rooms_per_house", ratio_pipeline(), ["total_rooms", "households"]),
        ("people_per_house", ratio_pipeline(), ["population", "households"]),
        ("log", log_pipeline, ["total_bedrooms", "total_rooms", "population",
                               "households", "median_income"]),
        ("geo", cluster_simil, ["latitude", "longitude"]),
        ("cat", cat_pipeline, make_column_selector(dtype_include=object)),
    ],
    remainder=default_num_pipeline)  # one column remaining: housing_median_age

# Test the pipeline above
#c housing_prepared = preprocessing.fit_transform(housing)
# print(housing_prepared.shape)
# (16512, 24)

#pr print(preprocessing.get_feature_names_out())
#out ['bedrooms__ratio' 'rooms_per_house__ratio' 'people_per_house__ratio'
#out  'log__total_bedrooms' 'log__total_rooms' 'log__population'
#out  'log__households' 'log__median_income' 'geo__Cluster 0 similarity'
#out  'geo__Cluster 1 similarity' 'geo__Cluster 2 similarity'
#out  'geo__Cluster 3 similarity' 'geo__Cluster 4 similarity'
#out  'geo__Cluster 5 similarity' 'geo__Cluster 6 similarity'
#out  'geo__Cluster 7 similarity' 'geo__Cluster 8 similarity'
#out  'geo__Cluster 9 similarity' 'cat__ocean_proximity_<1H OCEAN'
#out  'cat__ocean_proximity_INLAND' 'cat__ocean_proximity_ISLAND'
#out  'cat__ocean_proximity_NEAR BAY' 'cat__ocean_proximity_NEAR OCEAN'
#out  'remainder__housing_median_age']

# ############################################################################80

# Select and Train a Model

# ----------------------------------------------------------------------------80
# Train and Evaluate on the Training Set

# For computing the RMSE of models
# Warning: In recent versions of Scikit-Learn, you must use
# `root_mean_squared_error(labels, predictions)` to compute the RMSE,
# instead of `mean_squared_error(labels, predictions, squared=False)`. The
# following `try`/`except` block tries to import `root_mean_squared_error`,
# and if it fails it just defines it.
try:
    from sklearn.metrics import root_mean_squared_error
except ImportError:
    from sklearn.metrics import mean_squared_error

    def root_mean_squared_error(labels, predictions):
        return mean_squared_error(labels, predictions, squared=False)

# --------------------------30
# Linear regression model

#c from sklearn.linear_model import LinearRegression

#c lin_reg = make_pipeline(preprocessing, LinearRegression())
#c lin_reg.fit(housing, housing_labels)

# Let's try the full preprocessing pipeline on a few training instances:
#c housing_predictions = lin_reg.predict(housing)
#c print(housing_predictions[:5].round(-2))  # -2 = rounded to the nearest hundred
# [242800. 375900. 127500.  99400. 324600.]

# Compare against the actual values:
#c print(housing_labels.iloc[:5].values)
# [458300. 483800. 101700.  96100. 361800.]

# Computes the error ratios discussed in the book
#c error_ratios = housing_predictions[:5].round(-2) / housing_labels.iloc[:5].values - 1
#c print(", ".join([f"{100 * ratio:.1f}%" for ratio in error_ratios]))
# -47.0%, -22.3%, 25.4%, 3.4%, -10.3%

#c lin_rmse = root_mean_squared_error(housing_labels, housing_predictions)
#c print(round(lin_rmse, 4))
# 68647.9569

# --------------------------30
# Decision Tree

#c from sklearn.tree import DecisionTreeRegressor
#c tree_reg = make_pipeline(preprocessing, DecisionTreeRegressor(random_state=42))
#c tree_reg.fit(housing, housing_labels)

#c tree_predictions = tree_reg.predict(housing)
# Print the predictions for the first 5 districts
#c print(tree_predictions[:5].round(-2))
# [458300. 483800. 101700.  96100. 361800.]

# Compare the predictions against the actual values
#c print(housing_labels.iloc[:5].values)
# [458300. 483800. 101700.  96100. 361800.]

# Compute the RMSE
#c tree_rmse = root_mean_squared_error(housing_labels, tree_predictions)
#c print(tree_rmse)
# 0.0

# ----------------------------------------------------------------------------80
# Better Evaluation Using Cross-Validation

#c from sklearn.model_selection import cross_val_score
#c from sklearn.model_selection import cross_validate

# Note:
# The `cross_val_score()` function itself does not directly provide
# training scores, as it is designed to return only the validation scores
# for each fold during cross-validation. However, to track **both**
# training and validation scores for each fold explicitly, you can use the
# `cross_validate()` function from `sklearn.model_selection`
#
# Using `cross_validate` to Track More Details**
# The `cross_validate()` function allows you to see both training and
# validation scores by specifying "return_train_score=True". For more
# customization, it even supports tracking additional metrics, giving you a
# better understanding of the model's behavior.

# --------------------------30
# Linear regression with Cross-Validation

# Using "cross_validate()".

# Note. The `cross_validate` function from `scikit-learn` returns a
# dictionary, not a numeric value. So, it cannot be put a negative sign
# before the function like for "cross_val_score" because Negation (`-`) can
# only be applied to numeric types, like integers or floats, not
# dictionaries.
# The `cross_validate` function returns a dictionary containing keys like:
#   - `test_score` (cross-validation scores).
#   - `fit_time`, `score_time` (time metrics).
#c lin_reg_cv =  cross_validate(lin_reg, housing, housing_labels,
#c                              scoring="neg_root_mean_squared_error", cv=10,
#c                              return_train_score=True)

# Access negative validation and training scores
#c lin_reg_cv_val_scores   = -lin_reg_cv["test_score"]
#c lin_reg_cv_train_scores = -lin_reg_cv["train_score"]

#c print("\nValidation scores (RMSE):\n", lin_reg_cv_val_scores)
# Validation scores (RMSE):
#  [69629.27198277 68386.63041132 65659.76107851 80685.25483204
#  68585.89530719 68809.28761851 67695.97974629 71179.43136955
#  67989.5220715  69858.19782376]

#c print("\nTrain scores (RMSE):\n", lin_reg_cv_train_scores)
# Train scores (RMSE):
#  [68564.51827873 68739.26961825 69021.65268125 68134.12536066
#  68702.84570954 68641.30094392 68620.92441724 68442.93161763
#  68759.50173313 68549.47253429]

# Compute mean and standard deviation of RMSE values
#c lin_cv_val_score_mean = np.mean(lin_reg_cv_val_scores)
#c lin_cv_val_score_std = np.std(lin_reg_cv_val_scores)
#c lin_cv_train_score_mean = np.mean(lin_reg_cv_train_scores)
#c lin_cv_train_score_std = np.std(lin_reg_cv_train_scores)

#c print(f"Mean RMSE valid: {round(lin_cv_val_score_mean, 4)}")
#c print(f"Mean RMSE train: {round(lin_cv_train_score_mean, 4)}")
#c print(f"Standard Deviation of RMSE valid: {round(lin_cv_val_score_std, 4)}")
#c print(f"Standard Deviation of RMSE train: {round(lin_cv_train_score_std, 4)}")
# Mean RMSE valid: 69847.9232
# Mean RMSE train: 68617.6543
# Standard Deviation of RMSE valid: 3869.1169
# Standard Deviation of RMSE train: 218.5757


# Using "cross_val_score()". (Optional but 'cross_validate()' is better)

#c lin_rmse_cv_scores = -cross_val_score(lin_reg, housing, housing_labels,
#c                                scoring="neg_root_mean_squared_error", cv=10)
#c print(pd.Series(lin_rmse_cv_scores).describe(),"\n")
# count       10.000000
# mean     69847.923224 <---
# std       4078.407329 <---
# min      65659.761079
# 25%      68088.799156
# 50%      68697.591463
# 75%      69800.966364
# max      80685.254832
# dtype: float64

# --------------------------30
# Decision Tree with Cross-Validation

#c tree_rmse_cv = -cross_val_score(tree_reg, housing, housing_labels,
#c                                 scoring="neg_root_mean_squared_error", cv=10)

#c print(pd.Series(tree_rmse_cv).describe(),"\n")
# count       10.000000
# mean     66366.983603 <---
# std       1976.844743 <---
# min      63557.655007
# 25%      65004.623899
# 50%      65886.897085
# 75%      68129.026040
# max      69530.301101
# dtype: float64

# --------------------------30
# Random Forest with Cross-Validation

#c from sklearn.ensemble import RandomForestRegressor

# Using "cross_validate()". (Best)

#c forest_reg = make_pipeline(preprocessing,
#c                             RandomForestRegressor(random_state=42))

#c forest_cv = cross_validate(forest_reg, housing, housing_labels,
#c                                scoring="neg_root_mean_squared_error", cv=5,
#c                                return_train_score=True)

# Validation and training scores
#c forest_cv_valid_scores = -forest_cv["test_score"]
#c forest_cv_train_scores = -forest_cv["train_score"]

#c print("\nValidation scores (RMSE):\n", forest_cv_valid_scores)
# Validation scores (RMSE):
#  [47084.127283   46407.88148756 47113.69767434 47971.2931094
#  47203.91945207]

#c print("\nTraining scores (RMSE):\n", forest_cv_train_scores)
# Train scores (RMSE):
#  [17801.40568169 17848.52928243 17788.07476118 17770.88262586
#  17671.97085742]

# Compute mean and standard deviation of RMSE values
#c forest_cv_valid_score_mean = np.mean(forest_cv_valid_scores)
#c forest_cv_valid_score_std = np.std(forest_cv_valid_scores)
#c forest_cv_train_score_mean = np.mean(forest_cv_train_scores)
#c forest_cv_train_score_std = np.std(forest_cv_train_scores)

#c print(f"Mean RMSE valid: {round(forest_cv_valid_score_mean, 4)}")
#c print(f"Mean RMSE train: {round(forest_cv_train_score_mean, 4)}")
#c print(f"Standard Deviation of RMSE valid: {round(forest_cv_valid_score_std, 4)}")
#c print(f"Standard Deviation of RMSE train: {round(forest_cv_train_score_std, 4)}")
# Mean RMSE valid: 47156.1838
# Mean RMSE train: 17776.1726
# Standard Deviation of RMSE valid: 496.7163
# Standard Deviation of RMSE train: 58.1375


# Using "cross_val_score()". (Optional but 'cross_validate()' is better)

# Warning: the following cell may take a few minutes to run:
#c forest_rmse_cv_scores = -cross_val_score(forest_reg, housing, housing_labels,
#c                                    scoring="neg_root_mean_squared_error", cv=5)
#c print(pd.Series(forest_rmse_cv_scores).describe(),"\n")
# count        5.000000
# mean     47156.183801 <---
# std        555.345713 <---
# min      46407.881488
# 25%      47084.127283
# 50%      47113.697674
# 75%      47203.919452
# max      47971.293109
# dtype: float64
# (old. count       10.000000
# mean     46938.209246 <---
# std       1018.397196 <---
# min      45522.649195
# 25%      46291.334639
# 50%      47021.703303
# 75%      47321.521991
# max      49140.832210
# dtype: float64 )

# Let's compare this RMSE measured using cross-validation (the
# "validation error") with the RMSE measured on the training set (the
# "training error"):
#c forest_reg.fit(housing, housing_labels)
#c forest_predictions = forest_reg.predict(housing)
#c forest_rmse_train = root_mean_squared_error(housing_labels, forest_predictions)

#c print(forest_rmse_train)
# 17521.565358779884
# The training error is much lower than the mean validation error, which usually
# means that the model has overfit the training set. Another possible
# explanation may be that there's a mismatch between the training data and
# the validation data, but it's not the case here, since both came from the
# same dataset that we shuffled and split in two parts.


# --------------------------30
#  Support Vector Machine with Cross-Validation

# Support vector machine regressor (sklearn.svm.SVR) with various
# hyperparameters, such as kernel="linear" (with various values for the C
# hyperparameter) or kernel="rbf" (with various values for the C and gamma
# hyperparameters). Note that support vector machines don’t scale well to
# large datasets, so you should probably train your model on just the first
# 5,000 instances of the training set and use only 3-fold cross-validation,
# or else it will take hours. How does the best SVR predictor
# perform?

#c from sklearn.svm import SVR

#c svm_reg = make_pipeline(preprocessing, SVR(kernel="rbf"))

# DONE: Create a training dataset composed of only 5000 instances or less but
# ensuring that is stratified.

#c svm_cv = cross_validate(svm_reg, housing, housing_labels,
#c                         scoring="neg_root_mean_squared_error", cv=3,
#c                         return_train_score=True)

# Validation and training scores
#c svm_cv_valid_scores = -svm_cv["test_score"]
#c svm_cv_train_scores = -svm_cv["train_score"]

#c print("\nValidation scores (RMSE):\n", svm_cv_valid_scores.round(4))
# [111004.3185 123842.5436 121918.2488]

#c print("\nTraining scores (RMSE):\n", svm_cv_train_scores.round(4))
# [122059.9159 116629.976  118174.5277]

# Compute mean and standard deviation of RMSE values
#c svm_cv_valid_score_mean = np.mean(svm_cv_valid_scores)
#c svm_cv_valid_score_std = np.std(svm_cv_valid_scores)
#c svm_cv_train_score_mean = np.mean(svm_cv_train_scores)
#c svm_cv_train_score_std = np.std(svm_cv_train_scores)

#c print(f"Mean RMSE valid: {round(svm_cv_valid_score_mean, 4)}")
#c print(f"Mean RMSE train: {round(svm_cv_train_score_mean, 4)}")
#c print(f"Standard Deviation of RMSE valid: {round(svm_cv_valid_score_std, 4)}")
#c print(f"Standard Deviation of RMSE train: {round(svm_cv_train_score_std, 4)}")
# Mean RMSE valid: 118921.7036
# Mean RMSE train: 118954.8066
# Standard Deviation of RMSE valid: 5653.2862
# Standard Deviation of RMSE train: 2284.3946


# ############################################################################80
# Hyperparameters fine-tunning ("Fine-Tune Your Model")

# Let’s assume that you now have a shortlist of promising models. You now
# need to fine-tune them.

# ============================================================================80
# Random forest

from sklearn.ensemble import RandomForestRegressor

forest_pipe = Pipeline([
    ("preprocessing", preprocessing),
    ("random_forest", RandomForestRegressor(random_state=42)),
])

# --------------------------------------------------------60
# Grid Search

#c from sklearn.model_selection import GridSearchCV

#c forest_param_grid = [
#c     {"preprocessing__geo__n_clusters": [5, 8, 10],
#c      "random_forest__max_features": [4, 6, 8]},
#c     {"preprocessing__geo__n_clusters": [10, 15],
#c      "random_forest__max_features": [6, 8, 10]},
#c ]

#c forest_grid_srch = GridSearchCV(forest_pipe, forest_param_grid, cv=3,
#c                            scoring="neg_root_mean_squared_error",
#c                                 return_train_score=True)

# Warning: This line may take some few minutes to run:
#c forest_grid_srch.fit(housing, housing_labels)

# The best hyperparameter combination found:
#c print(forest_grid_srch.best_params_)
# {'preprocessing__geo__n_clusters': 15, 'random_forest__max_features': 6}
#c print(forest_grid_srch.best_score_)
# -43617.70350797693

#c print(forest_grid_srch.best_estimator_)
# Pipeline(steps=[('preprocessing',
#    ColumnTransformer(remainder=Pipeline(steps=[('simpleimputer',
#                               SimpleImputer(strategy='median')),
#                              ('standardscaler',
#                               StandardScaler())]),
#    transformers=[('bedrooms',
#                   Pipeline(steps=[('simpleimputer',
#                                    SimpleImputer(strategy='median')),
#                                   ('functiontransformer',
#                                    FunctionTransformer(feature_names_out=
#                                           <function ratio_name at 0x144b4fb...
#                   ClusterSimilarity(n_clusters=15,
#                                     random_state=42),
#                   ['latitude', 'longitude']),
#                  ('cat',
#                   Pipeline(steps=[('simpleimputer',
#                                    SimpleImputer(strategy='most_frequent')),
#                                   ('onehotencoder',
#                                    OneHotEncoder(handle_unknown='ignore'))]),
#                   <sklearn.compose._column_transformer.make_column_selector o
#                                                       bject at 0x144fca610>)])),
#   ('random_forest',
#    RandomForestRegressor(max_features=6, random_state=42))])

# Look at the score of each hyperparameter combination tested during
# the grid search:
#c forest_grid_cv_val_scores = pd.DataFrame(forest_grid_srch.cv_results_)
#c forest_grid_cv_val_scores.sort_values(by="mean_test_score", ascending=False,
#c                                       inplace=True)
# extra code – these few lines of code just make the DataFrame look nicer
#c forest_grid_cv_val_scores = forest_grid_cv_val_scores[["param_preprocessing__geo__n_clusters",
#c                  "param_random_forest__max_features",
                 # "split0_test_score", "split1_test_score", "split2_test_score",
#c                  "mean_test_score", "mean_train_score"
                 # , "std_test_score", "std_train_score"
#c                  ]]

# Rename the columns so it is clearer what they are about:
#c score_cols = [ #"split0", "split1", "split2",
#c                 "mean_test_rmse" , "mean_train_rmse"
                #, "std_test_rmse", "std_train_rmse"
#c              ]
#c forest_grid_cv_val_scores.columns = ["n_clusters", "max_features"] + score_cols
#c forest_grid_cv_val_scores[score_cols] = \
#c   -forest_grid_cv_val_scores[score_cols].round().astype(np.int64)

#c print(forest_grid_cv_val_scores.head())
#     n_clusters  max_features  mean_test_rmse  mean_train_rmse
# 12          15             6           43618            16455
# 13          15             8           44178            16649
# 7           10             6           44360            16745
# 9           10             6           44360            16745
# 6           10             4           44376            16755

# (OLD:     n_clusters  max_features  split0  split1  split2  mean_test_rmse
# 12          15             6   43012   43683   44158           43618
# 13          15             8   43697   44017   44819           44178
# 7           10             6   43710   44133   45238           44360
# 9           10             6   43710   44133   45238           44360
# 6           10             4   43803   44232   45094           44376)


# --------------------------------------------------------60
# Summary of probability distributions that may be used for the random search

# Bonus section: how to choose the sampling distribution for a
# hyperparameter
#
# * `scipy.stats.randint(a, b+1)`: for hyperparameters with _discrete_
# values that range from a to b, and all values in that range seem equally
# likely.
# * `scipy.stats.uniform(a, b)`: this is very similar, but for _continuous_
# hyperparameters.
# * `scipy.stats.geom(1 / scale)`: for discrete values, when you want to
# sample roughly in a given scale. E.g., with scale=1000 most samples will
# be in this ballpark, but ~10% of all samples will be <100 and ~10% will
# be >2300.
# * `scipy.stats.expon(scale)`: this is the continuous equivalent of
# `geom`. Just set `scale` to the most likely value.
# * `scipy.stats.loguniform(a, b)`: when you have almost no idea what the
# optimal hyperparameter value's scale is. If you set a=0.01 and b=100,
# then you're just as likely to sample a value between 0.01 and 0.1 as a
# value between 10 and 100.
#
# Here are plots of the probability mass functions (for discrete
# variables), and probability density functions (for continuous variables)
# for `randint()`, `uniform()`, `geom()` and `expon()`:
#
# extra code – plots a few distributions you can use in randomized search

#c from scipy.stats import randint, uniform, geom, expon

#c xs1 = np.arange(0, 7 + 1)
#c randint_distrib = randint(0, 7 + 1).pmf(xs1)

#c xs2 = np.linspace(0, 7, 500)
#c uniform_distrib = uniform(0, 7).pdf(xs2)

#c xs3 = np.arange(0, 7 + 1)
#c geom_distrib = geom(0.5).pmf(xs3)

#c xs4 = np.linspace(0, 7, 500)
#c expon_distrib = expon(scale=1).pdf(xs4)

#c plt.figure(figsize=(12, 7))

#c plt.subplot(2, 2, 1)
#c plt.bar(xs1, randint_distrib, label="scipy.randint(0, 7 + 1)")
#c plt.ylabel("Probability")
#c plt.legend()
#c plt.axis([-1, 8, 0, 0.2])

#c plt.subplot(2, 2, 2)
#c plt.fill_between(xs2, uniform_distrib, label="scipy.uniform(0, 7)")
#c plt.ylabel("PDF")
#c plt.legend()
#c plt.axis([-1, 8, 0, 0.2])

#c plt.subplot(2, 2, 3)
#c plt.bar(xs3, geom_distrib, label="scipy.geom(0.5)")
#c plt.xlabel("Hyperparameter value")
#c plt.ylabel("Probability")
#c plt.legend()
#c plt.axis([0, 7, 0, 1])

#c plt.subplot(2, 2, 4)
#c plt.fill_between(xs4, expon_distrib, label="scipy.expon(scale=1)")
#c plt.xlabel("Hyperparameter value")
#c plt.ylabel("PDF")
#c plt.legend()
#c plt.axis([0, 7, 0, 1])

#c save_fig("probability_functions_for_random_search")
# plt.show()


# Here are the PDF for `expon()` and `loguniform()` (left column), as well
# as the PDF of log(X) (right column). The right column shows the
# distribution of hyperparameter _scales_. You can see that `expon()`
# favors hyperparameters with roughly the desired scale, with a longer tail
# towards the smaller scales. But `loguniform()` does not favor any scale,
# they are all equally likely:

# extra code – shows the difference between expon and loguniform

#c from scipy.stats import loguniform

#c xs1 = np.linspace(0, 7, 500)
#c expon_distrib = expon(scale=1).pdf(xs1)

#c log_xs2 = np.linspace(-5, 3, 500)
#c log_expon_distrib = np.exp(log_xs2 - np.exp(log_xs2))

#c xs3 = np.linspace(0.001, 1000, 500)
#c loguniform_distrib = loguniform(0.001, 1000).pdf(xs3)

#c log_xs4 = np.linspace(np.log(0.001), np.log(1000), 500)
#c log_loguniform_distrib = uniform(np.log(0.001), np.log(1000)).pdf(log_xs4)

#c plt.figure(figsize=(12, 7))

#c plt.subplot(2, 2, 1)
#c plt.fill_between(xs1, expon_distrib,
#c                  label="scipy.expon(scale=1)")
#c plt.ylabel("PDF")
#c plt.legend()
#c plt.axis([0, 7, 0, 1])

#c plt.subplot(2, 2, 2)
#c plt.fill_between(log_xs2, log_expon_distrib,
#c                  label="log(X) with X ~ expon")
#c plt.legend()
#c plt.axis([-5, 3, 0, 1])

#c plt.subplot(2, 2, 3)
#c plt.fill_between(xs3, loguniform_distrib,
#c                  label="scipy.loguniform(0.001, 1000)")
#c plt.xlabel("Hyperparameter value")
#c plt.ylabel("PDF")
#c plt.legend()
#c plt.axis([0.001, 1000, 0, 0.005])

#c plt.subplot(2, 2, 4)
#c plt.fill_between(log_xs4, log_loguniform_distrib,
#c                  label="log(X) with X ~ loguniform")
#c plt.xlabel("Log of hyperparameter value")
#c plt.legend()
#c plt.axis([-8, 1, 0, 0.2])

#c save_fig("probability_functions_exp_loguniform_for_random_search")
# plt.show()

# --------------------------------------------------------60
# Randomized Search with "RandomizedSearchCV()" (Best option)

# The grid search approach is fine when you are exploring relatively few
# combinations, like in the previous example, but "RandomizedSearchCV()" is
# often preferable, especially when the hyperparameter search space is
# large.


from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

forest_param_distr = {"preprocessing__geo__n_clusters": randint(low=3, high=50),
                       "random_forest__max_features": randint(low=2, high=20)}

forest_rand_srch = RandomizedSearchCV(forest_pipe,
                                param_distributions=forest_param_distr,
                                n_iter=10, cv=3,
                                scoring="neg_root_mean_squared_error",
                                return_train_score=True,
                                random_state=42)

# Warning: This line may take some few minutes to run:
forest_rand_srch.fit(housing, housing_labels)

# The best hyperparameter combination found:
print(forest_rand_srch.best_params_)
# {'preprocessing__geo__n_clusters': 45, 'random_forest__max_features': 9}

print(forest_rand_srch.best_score_)
# -42110.69399511482

print(forest_rand_srch.best_estimator_)
# Pipeline(steps=[('preprocessing',
#    ColumnTransformer(remainder=Pipeline(steps=[('simpleimputer',
#                         SimpleImputer(strategy='median')),
#                        ('standardscaler',
#                         StandardScaler())]),
#        transformers=[('bedrooms',
#                       Pipeline(steps=[('simpleimputer',
#                            SimpleImputer(strategy='median')),
#                           ('functiontransformer',
#                            FunctionTransformer(feature_names_out=
#                                       <function ratio_name at 0x11ac28b...
#                       ClusterSimilarity(n_clusters=45,
#                                         random_state=42),
#                       ['latitude', 'longitude']),
#                      ('cat',
#                       Pipeline(steps=[('simpleimputer',
#                            SimpleImputer(strategy='most_frequent')),
#                           ('onehotencoder',
#                            OneHotEncoder(handle_unknown='ignore'))]),
#                       <sklearn.compose._column_transformer.make_column_selector
#                                                       object at 0x11dbf6f10>)])),
#   ('random_forest',
#    RandomForestRegressor(max_features=9, random_state=42))])

# Look at the score of each hyperparameter combination tested during
# the grid search:
forest_rand_cv_val_scores = pd.DataFrame(forest_rand_srch.cv_results_)
forest_rand_cv_val_scores.sort_values(by="mean_test_score", ascending=False,
                                      inplace=True)
# extra code – these few lines of code just make the DataFrame look nicer
forest_rand_cv_val_scores = forest_rand_cv_val_scores[["param_preprocessing__geo__n_clusters",
                 "param_random_forest__max_features",
                 # "split0_test_score", "split1_test_score", "split2_test_score",
                 "mean_test_score", "mean_train_score"
                 # , "std_test_score", "std_train_score"
                 ]]

# Rename the columns so it is clearer what they are about:
score_cols = [ #"split0", "split1", "split2",
                "mean_valid_rmse" , "mean_train_rmse"
                #, "std_valid_rmse", "std_train_rmse"
             ]
forest_rand_cv_val_scores.columns = ["n_clusters", "max_features"] + score_cols
forest_rand_cv_val_scores[score_cols] = \
    -forest_rand_cv_val_scores[score_cols].round().astype(np.int64)

print(forest_rand_cv_val_scores.head())
#    n_clusters  max_features  mean_valid_rmse  mean_train_rmse
# 1          45             9           42111            15908
# 8          32             7           42396            16023
# 0          41            16           42736            16161
# 5          42             4           42953            16104
# 2          23             8           43044            16263


# --------------------------------------------------------60
# Randomized Search with "HalvingRandomSearchCV()". (Experimental) (It didn't work)

# (April 2025) The module "enable_halving_search_cv" is required to run the
# # "HalvingRandomSearchCV()" class.

#c from sklearn.experimental import enable_halving_search_cv
#c from sklearn.model_selection import HalvingRandomSearchCV
#c from scipy.stats import randint

#c forest_param_distr = {"preprocessing__geo__n_clusters": randint(low=3, high=50),
#c                       "random_forest__max_features": randint(low=2, high=10)}

#c forest_halvrand_srch = HalvingRandomSearchCV(forest_pipe,
#c                                              param_distributions=forest_param_distr,
#c                                              cv=3,
#c                                              scoring="neg_root_mean_squared_error",
#c                                              return_train_score=True,
#c                                              random_state=42)

# Warning: This line may take some few minutes to run:
#c forest_halvrand_srch.fit(housing, housing_labels)

# The best hyperparameter combination found:
#c print(forest_halvrand_srch.best_params_)

#c print(forest_halvrand_srch.best_score_)


#c print(forest_halvrand_srch.best_estimator_)


# Look at the score of each hyperparameter combination tested during
# the grid search:
#c forest_halv_cv_val_scores = pd.DataFrame(forest_halvrand_srch.cv_results_)
#c forest_halv_cv_val_scores.sort_values(by="mean_test_score", ascending=False,
#c                                       inplace=True)
# extra code – these few lines of code just make the DataFrame look nicer
#c forest_halv_cv_val_scores = forest_halv_cv_val_scores[["param_preprocessing__geo__n_clusters",
#c                  "param_random_forest__max_features",
                 # "split0_test_score", "split1_test_score", "split2_test_score",
#c                  "mean_test_score", "mean_train_score"
                 # , "std_test_score", "std_train_score"
#c                  ]]

# Rename the columns so it is clearer what they are about:
#c score_cols = [ #"split0", "split1", "split2",
#c                 "mean_test_rmse" , "mean_train_rmse"
                #, "std_test_rmse", "std_train_rmse"
#c              ]
#c forest_halv_cv_val_scores.columns = ["n_clusters", "max_features"] + score_cols
#c forest_halv_cv_val_scores[score_cols] = \
#c     -forest_halv_cv_val_scores[score_cols].round().astype(np.int64)

#c print(forest_halv_cv_val_scores.head())

# ============================================================================80
# Support Vector Machine with "RandomizedSearchCV()"

from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVR
from scipy.stats import expon, loguniform, randint

svr_pipe = Pipeline([
    ("preprocessing", preprocessing),
    ("svr", SVR()),
])

svr_param_distr = {
        'svr__kernel': ['linear', 'rbf'],
        'svr__C': loguniform(20, 200_000),
        'svr__gamma': expon(scale=1.0),
        "preprocessing__geo__n_clusters": randint(low=3, high=50)
    }

svr_rand_srch = RandomizedSearchCV(svr_pipe,
                                   param_distributions=svr_param_distr,
                                   n_iter=10, cv=3,
                                   scoring="neg_root_mean_squared_error",
                                   return_train_score=True,
                                   random_state=42)

# Warning: This line may take some few minutes to run:
svr_rand_srch.fit(housing, housing_labels)

# The best hyperparameter combination found:
print(svr_rand_srch.best_params_)
# {'preprocessing__geo__n_clusters': 30,
# 'svr__C': np.float64(157055.10989448498),
# 'svr__gamma': np.float64(0.26497040005002437),
# 'svr__kernel': 'rbf'}
#tmp {'preprocessing__geo__n_clusters': 38, 'supportvm__C': 872}

print(svr_rand_srch.best_score_)
# -60956.471760103675

print(svr_rand_srch.best_estimator_)
#out Pipeline(steps=[('preprocessing',
#out    ColumnTransformer(remainder=Pipeline(steps=[('simpleimputer',
#out                                   SimpleImputer(strategy='median')),
#out                                  ('standardscaler',
#out                                   StandardScaler())]),
#out        transformers=[('bedrooms',
#out                       Pipeline(steps=[('simpleimputer',
#out                                        SimpleImputer(strategy='median')),
#out                                       ('functiontransformer',
#out                                        FunctionTransformer(feature_names_out=
#out                                           <function ratio_name at 0x1492641...
#out                                         random_state=42),
#out                       ['latitude', 'longitude']),
#out                      ('cat',
#out                       Pipeline(steps=[('simpleimputer',
#out                                        SimpleImputer(strategy='most_frequent')),
#out                                       ('onehotencoder',
#out                                        OneHotEncoder(handle_unknown='ignore'))]),
#out                       <sklearn.compose._column_transformer.make_column_selector
#out                       object at 0x14988c970>)])),
#out   ('svr',
#out    SVR(C=np.float64(157055.10989448498),
#out        gamma=np.float64(0.26497040005002437)))])


# Look at the score of each hyperparameter combination tested during
# the grid search:
svm_rand_cv_val_scores = pd.DataFrame(svr_rand_srch.cv_results_)
svm_rand_cv_val_scores.sort_values(by="mean_test_score", ascending=False,
                                      inplace=True)
# extra code – these few lines of code just make the DataFrame look nicer
svm_rand_cv_val_scores = svm_rand_cv_val_scores[[
        "param_preprocessing__geo__n_clusters",
        "param_svr__C",
        # "split0_test_score", "split1_test_score", "split2_test_score",
        "mean_test_score", "mean_train_score"
        # , "std_test_score", "std_train_score"
    ]]

# Rename the columns so it is clearer what they are about:
score_cols = [ #"split0", "split1", "split2",
                "mean_valid_rmse" , "mean_train_rmse"
                #, "std_valid_rmse", "std_train_rmse"
             ]
svm_rand_cv_val_scores.columns = ["n_clusters", "C_svm"] + score_cols
svm_rand_cv_val_scores[score_cols] = \
    -svm_rand_cv_val_scores[score_cols].round().astype(np.int64)

print(svm_rand_cv_val_scores.head())
#    n_clusters          C_svm  mean_valid_rmse  mean_train_rmse
# 7          30  157055.109894            60956            36000
# 0          41   30704.493884            65698            57676
# 9           5   55054.347859            70831            69906
# 4          32     141.379499            83031            82797
# 2          13   58308.863783            85188            58926

# ----------------------------------------------------------------------------80
# Analyzing the Best Models and Their Errors

final_model = forest_rand_srch.best_estimator_

feature_importances = final_model.named_steps["random_forest"].feature_importances_
print(feature_importances.round(2))
# [0.06 0.05 0.05 0.01 0.01 0.01 0.01 0.19 0.01 0.01 0.02 0.04 0.01 0.
#  0.02 0.01 0.01 0.01 0.02 0.01 0.   0.01 0.01 0.01 0.01 0.02 0.02 0.01
#  0.01 0.01 0.02 0.01 0.01 0.01 0.01 0.01 0.01 0.   0.01 0.01 0.02 0.01
#  0.01 0.02 0.01 0.01 0.01 0.01 0.02 0.02 0.01 0.01 0.01 0.   0.08 0.
#  0.   0.   0.01]

feature_imp_sorted = sorted(zip(feature_importances,
           final_model["preprocessing"].get_feature_names_out()),
       reverse=True)

print(feature_imp_sorted)
# [(np.float64(0.18901772752260965), 'log__median_income'),
# (np.float64(0.07519718294444783), 'cat__ocean_proximity_INLAND'),
# (np.float64(0.06368885514209106), 'bedrooms__ratio'),
# (np.float64(0.052269006448954984), 'rooms_per_house__ratio'),
# (np.float64(0.04648465413462927), 'people_per_house__ratio'),
# (np.float64(0.04284851790565368), 'geo__Cluster 3 similarity'),
# (np.float64(0.023328049652780496), 'geo__Cluster 17 similarity'),
# (np.float64(0.022238253533182), 'geo__Cluster 18 similarity'),
# (np.float64(0.022194673655250526), 'geo__Cluster 22 similarity'),
# (np.float64(0.01859877667208851), 'geo__Cluster 40 similarity'),
# (np.float64(0.01780189964394329), 'geo__Cluster 10 similarity'),
# (np.float64(0.01730806454731114), 'geo__Cluster 41 similarity'),
# (np.float64(0.016888879511081256), 'geo__Cluster 35 similarity'),
# (np.float64(0.01628583573372508), 'geo__Cluster 6 similarity'),
# (np.float64(0.015846054619681672), 'geo__Cluster 2 similarity'),
# (np.float64(0.015393321731047401), 'geo__Cluster 32 similarity'),
# (np.float64(0.014021412676113494), 'geo__Cluster 21 similarity'),
# (np.float64(0.013625993562233386), 'geo__Cluster 43 similarity'),
# (np.float64(0.012944682039851803), 'geo__Cluster 39 similarity'),
# (np.float64(0.012307675124178118), 'geo__Cluster 7 similarity'),
# (np.float64(0.012297144595634062), 'geo__Cluster 31 similarity'),
# (np.float64(0.012088017778021426), 'geo__Cluster 38 similarity'),
# (np.float64(0.012073241980503281), 'geo__Cluster 26 similarity'),
# (np.float64(0.011600272434573013), 'geo__Cluster 14 similarity'),
# (np.float64(0.011499691531676905), 'geo__Cluster 30 similarity'),
# (np.float64(0.011171540423071134), 'geo__Cluster 34 similarity'),
# (np.float64(0.010403408502549864), 'geo__Cluster 0 similarity'),
# (np.float64(0.01038662524332695), 'remainder__housing_median_age'),
# (np.float64(0.010345217182478822), 'geo__Cluster 42 similarity'),
# (np.float64(0.01028728734562454), 'geo__Cluster 4 similarity'),
# (np.float64(0.009922246264068731), 'geo__Cluster 1 similarity'),
# (np.float64(0.00931760536371674), 'geo__Cluster 37 similarity'),
# (np.float64(0.009142833139374095), 'geo__Cluster 44 similarity'),
# (np.float64(0.00904445620150606), 'geo__Cluster 28 similarity'),
# (np.float64(0.00902353483024036), 'geo__Cluster 8 similarity'),
# (np.float64(0.008314124769262958), 'geo__Cluster 25 similarity'),
# (np.float64(0.008237276360095502), 'geo__Cluster 15 similarity'),
# (np.float64(0.008209325573490026), 'geo__Cluster 11 similarity'),
# (np.float64(0.007439196817084087), 'geo__Cluster 36 similarity'),
# (np.float64(0.007265826511074997), 'geo__Cluster 33 similarity'),
# (np.float64(0.0071876019761469975), 'geo__Cluster 23 similarity'),
# (np.float64(0.007056087836479924), 'geo__Cluster 27 similarity'),
# (np.float64(0.006942780755401469), 'log__total_rooms'),
# (np.float64(0.006699376929183603), 'geo__Cluster 16 similarity'),
# (np.float64(0.006674876554855022), 'log__population'),
# (np.float64(0.006627269250787917), 'geo__Cluster 20 similarity'),
# (np.float64(0.006176061385653615), 'geo__Cluster 24 similarity'),
# (np.float64(0.006159285192697616), 'log__total_bedrooms'),
# (np.float64(0.006040094152696972), 'geo__Cluster 19 similarity'),
# (np.float64(0.005957714456374491), 'log__households'),
# (np.float64(0.005862620130221602), 'geo__Cluster 13 similarity'),
# (np.float64(0.005142237508844201), 'geo__Cluster 9 similarity'),
# (np.float64(0.004639366249839571), 'geo__Cluster 12 similarity'),
# (np.float64(0.004392608787329616), 'geo__Cluster 5 similarity'),
# (np.float64(0.0035625780289471397), 'geo__Cluster 29 similarity'),
# (np.float64(0.0024966245281915194), 'cat__ocean_proximity_<1H OCEAN'),
# (np.float64(0.0014963382093688303), 'cat__ocean_proximity_NEAR OCEAN'),
# (np.float64(0.000513409806063684), 'cat__ocean_proximity_NEAR BAY'),
# (np.float64(1.4678612688170039e-05), 'cat__ocean_proximity_ISLAND')]


# ----------------------------------------------------------------------------80
# Evaluate your system on the test set

X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()

testset_predictions = final_model.predict(X_test)

testset_rmse = root_mean_squared_error(y_test, testset_predictions)

print(f"RMSE from test dataset: {testset_rmse:.2f}")
# RMSE from test dataset: 41533.24

# --------------------------------------------------------60
# Compute a 95% confidence interval for the test RMSE:

from scipy import stats

def rmse(squared_errors):
    return np.sqrt(np.mean(squared_errors))

confidence_interv = 0.95
squared_errors = (testset_predictions - y_test) ** 2
boot_result = stats.bootstrap([squared_errors], rmse,
                              confidence_level=confidence_interv,
                              random_state=42)
rmse_lower, rmse_upper = boot_result.confidence_interval

print(f"95% confidence interval for RMSE: [{rmse_lower:.2f}, {rmse_upper:.2f}]")
# 95% confidence interval for RMSE: [39614.92, 43774.66]


# ############################################################################80
# Launch, Monitor, And Maintain Your System

# Save the final model:
import joblib

joblib.dump(final_model, "trained_models/housing_randomforest.pkl")

# ----------------------------------------------------------------------------80
# Now you can deploy this model to production. For example, the following
# code could be a script that would run in production:

# You can load it and use it. For this you must first import any custom
# classes and functions the model relies on you can load it and use it. For
# this you must first import any custom classes and functions the model
# relies on
# --------------------------30
# (Re)definition of the main functions and pipeline

#c from pathlib import Path
#c import pandas as pd
#c import tarfile
#c import urllib.request
#c import matplotlib.pyplot as plt
#c import numpy as np

#c def load_housing_data():
#c     tarball_path = Path("datasets/housing.tgz")
#c     if not tarball_path.is_file():
#c         Path("datasets").mkdir(parents=True, exist_ok=True)
#c         url = "https://github.com/ageron/data/raw/main/housing.tgz"
#c         urllib.request.urlretrieve(url, tarball_path)
#c     with tarfile.open(tarball_path) as housing_tarball:
#c             housing_tarball.extractall(path="datasets")
#c     return pd.read_csv(Path("datasets/housing/housing.csv"))

#c housing = load_housing_data()
#c print("housing.head()\n", housing.head())

#c print("housing.info()\n", housing.info())
#c print("\nhousing.describe()\n", housing.describe())


#c from sklearn.pipeline import make_pipeline, Pipeline
#c from sklearn.impute import SimpleImputer
#c from sklearn.compose import ColumnTransformer
#c from sklearn.compose import make_column_selector
#c from sklearn.preprocessing import StandardScaler
#c from sklearn.preprocessing import OneHotEncoder
#c from sklearn.preprocessing import FunctionTransformer

# --------------------------30
# (Re)definition of the custome class

#c from sklearn.base import BaseEstimator, TransformerMixin
#c from sklearn.cluster import KMeans
#c from sklearn.metrics.pairwise import rbf_kernel


#c class ClusterSimilarity(BaseEstimator, TransformerMixin):
#c     def __init__(self, n_clusters=10, gamma=1.0, random_state=None):
#c         self.n_clusters = n_clusters
#c         self.gamma = gamma
#c         self.random_state = random_state

#c     def fit(self, x, y=None, sample_weight=None):
        # Dynamically adjust n_clusters if there are fewer samples than clusters
#c         n_samples = x.shape[0]
#c         effective_n_clusters = min(self.n_clusters, n_samples)
#c         if effective_n_clusters != self.n_clusters:
#c             print(
#c                 f"Warning: Adjusting number of clusters from {self.n_clusters} "
#c                 f"to {effective_n_clusters}"
#c                 f"to match the available number of samples ({n_samples}).")
#c         self.n_clusters = effective_n_clusters

#c         self.kmeans_ = KMeans(self.n_clusters, n_init=10,
#c                               random_state=self.random_state)
#c         self.kmeans_.fit(x, sample_weight=sample_weight)
#c         return self  # Always return self!

#c     def transform(self, x):
#c         return rbf_kernel(x, self.kmeans_.cluster_centers_, gamma=self.gamma)

#c     def get_feature_names_out(self, names=None):
#c         return [f"Cluster {i} similarity" for i in range(self.n_clusters)]

#c cat_pipeline = make_pipeline(
#c     SimpleImputer(strategy="most_frequent"),
#c     OneHotEncoder(handle_unknown="ignore"))

#c def column_ratio(x):
#c     return x[:, [0]] / x[:, [1]]

#c def ratio_name(function_transformer, feature_names_in):
#c     return ["ratio"]  # feature names out

#c def ratio_pipeline():
#c     return make_pipeline(
#c         SimpleImputer(strategy="median"),
#c         FunctionTransformer(column_ratio, feature_names_out=ratio_name),
#c         StandardScaler())

#c log_pipeline = make_pipeline(
#c     SimpleImputer(strategy="median"),
#c     FunctionTransformer(np.log, feature_names_out="one-to-one"),
#c     StandardScaler())
#c cluster_simil = ClusterSimilarity(n_clusters=10, gamma=1., random_state=42)
#c default_num_pipeline = make_pipeline(SimpleImputer(strategy="median"),
#c                                      StandardScaler())
# Defining the main pipeline:
#c preprocessing = ColumnTransformer([
#c         ("bedrooms", ratio_pipeline(), ["total_bedrooms", "total_rooms"]),
#c         ("rooms_per_house", ratio_pipeline(), ["total_rooms", "households"]),
#c         ("people_per_house", ratio_pipeline(), ["population", "households"]),
#c         ("log", log_pipeline, ["total_bedrooms", "total_rooms", "population",
#c                                "households", "median_income"]),
#c         ("geo", cluster_simil, ["latitude", "longitude"]),
#c         ("cat", cat_pipeline, make_column_selector(dtype_include=object)),
#c     ],
#c     remainder=default_num_pipeline)  # one column remaining: housing_median_age

# --------------------------30
#c import joblib


final_model_reloaded = joblib.load("trained_models/housing_randomforest.pkl")

#c new_data = housing.iloc[:5]  # pretend these are new districts
#c predictions = final_model_reloaded.predict(new_data)

#c print("\nPredictions:\n", predictions)
# [434759.11 376218.06 381842.1  341939.   322989.  ]

# ############################################################################80

print("Stop code here while debugging.")
print("here!")

print("\nEnd of code!")

