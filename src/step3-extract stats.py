from gensim import corpora, models, similarities
import pandas as pd

N_ROWS = None
# Load data and models
dataset = pd.read_csv("dataset/clean.csv", index_col=0, nrows=N_ROWS)

try:
    dictionary = corpora.Dictionary.load("models/greek.dict")
    print("Dictionary loaded from file.")
except FileNotFoundError:
    raise Exception("Dictionary file not found. Please build the models first.")

try:
    tfidf_model = models.TfidfModel.load("models/greek.tfidf")
    print("TF-IDF model loaded from file.")
except FileNotFoundError:
    raise Exception("TF-IDF model file not found. Please build the models first.")

try:
    lsi_model = models.LsiModel.load("models/greek.lsi")
    print("LSI model loaded from file.")
except FileNotFoundError:
    raise Exception("LSI model file not found. Please build the models first.")

try:
    index = similarities.Similarity.load("models/index/greek.lsi", mmap='r')
    print("Similarity index loaded from file.")
except FileNotFoundError:
    raise Exception("Similarity index file not found. Please build the models first.")

# Extract top topics

with open("stats/Top Topics.txt","w") as f:
    tVectors = lsi_model.projection.s
    for t in range(10):
        top_words_with_contribution = lsi_model.show_topic(t)
        top_words = []
        for word, contr in top_words_with_contribution:
            top_words.append(word)
        print(  f"Topic {t} \n" + \
                f"\tScore: {tVectors[t]:6.2f}\n" + \
                f"\tTop Words: {" ".join(top_words)}",
                file=f)
    
# Cluster speeches and plot 3D

import sklearn
import matplotlib.pyplot as plt

lsi_speeches = lsi_model.projection.u

# Drop to 3D using PCA
pca = sklearn.decomposition.PCA(n_components=3)
lsi_speeches = pca.fit_transform(lsi_speeches)

# k-means to standard clusters
num_clusters = 20
kmeans = sklearn.cluster.KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(lsi_speeches)
labels = kmeans.labels_

# Plot using PCA representation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    lsi_speeches[:,0],
    lsi_speeches[:,1],
    lsi_speeches[:,2],
    c=labels,
    cmap='tab20',
    s=20,
    alpha=0.6
)
plt.title("K-Means Clustering of Speeches in PCA-LSI Space")
plt.show()
