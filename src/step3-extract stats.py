from gensim import models
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from Models import Models


models = Models()    

# Extract top topics

with open("src/stats/Top Topics.txt","w") as f:
    tVectors = models.lsi.projection.s
    for t in range(10):
        top_words_with_contribution = models.lsi.show_topic(t)
        top_words = []
        for word, contr in top_words_with_contribution:
            top_words.append(word)
        print(  f"Topic {t} \n" + \
                f"\tScore: {tVectors[t]:6.2f}\n" + \
                f"\tTop Words: {' '.join(top_words)}",
                file=f)
    
# =================================================
# Cluster speeches and plot 3D
# =================================================

import sklearn
import matplotlib.pyplot as plt

# Get LSI vectors for all speeches as numpy array
lsi_speeches = models.lsi[models.tfidf[models.corpus]]

speeches_dense = np.zeros((len(models.dataset), models.lsi.num_topics))
for i, vec in enumerate(lsi_speeches):
    for idx, value in vec:
        speeches_dense[i, idx] = value


# Drop to 3D by selecting some LSI dimensions
# [2,3,4,5,6,8] seem good
speeches_dense_subset = speeches_dense[:, [2,3,4,5,6,8]]

# Drop to 3D using PCA
pca = sklearn.decomposition.PCA(n_components=3)
speeches_dense_subset = pca.fit_transform(speeches_dense_subset)

# k-means to standard clusters
num_clusters = 10
kmeans = sklearn.cluster.KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(speeches_dense_subset)
labels = kmeans.labels_

# Plot using PCA representation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    speeches_dense_subset[:,0],
    speeches_dense_subset[:,1],
    speeches_dense_subset[:,2],
    c=labels,
    cmap='tab20',
    s=20,
    alpha=0.6
)
plt.title("K-Means Clustering of Speeches in PCA-LSI Space")
plt.show()

# =================================================
# Closest speakers
# =================================================

# Store speeches of each speaker as its own set of speech ids to be used as mask on the DF and speeches_dense matrixes
speakers = models.dataset['member_name'].unique().to_numpy()

print(speeches_dense.shape)
print(len(speakers))
print(len(models.dataset))
speaker_vectors = {}
all_ids_count = 0
for speaker in speakers:
    speech_ids = np.where(models.dataset['member_name'] == speaker)[0]
    all_ids_count += len(speech_ids)
    try:
        speaker_vectors[speaker] = speeches_dense[speech_ids].mean(axis=0)
    except IndexError:
        print(f"Speaker {speaker} ids: {speech_ids}")
        continue
print(f"Total speeches counted in speaker vectors: {all_ids_count}")

speaker_name_to_id = {name: idx for idx, name in enumerate(speakers)}
speaker_id_to_name = {idx: name for name, idx in speaker_name_to_id.items()}
speaker_vectors_dense = np.zeros((len(speakers), speeches_dense.shape[1]))
for speaker, vec in speaker_vectors.items():
    speaker_id = speaker_name_to_id[speaker]
    speaker_vectors_dense[speaker_id, :] = vec

K_CLOSEST_SPEAKER_PAIRS = 5

# using cosine similarity to find closest speakers because of high dimensionality
speaker_distances = cosine_similarity(speaker_vectors_dense)

# Find the K_CLOSEST_SPEAKER_PAIRS closest speaker pairs
# We set the diagonal to -inf to avoid self-matches
np.fill_diagonal(speaker_distances, -np.inf)
# upper triangle indices
upper_tri_indices = np.triu_indices_from(speaker_distances, k=1)
upper_tri_values = speaker_distances[upper_tri_indices]
# get indices of the top K closest pairs
top_k_indices = np.argpartition(upper_tri_values, -K_CLOSEST_SPEAKER_PAIRS)[-K_CLOSEST_SPEAKER_PAIRS:]
closest_pairs = [(upper_tri_indices[0][i], upper_tri_indices[1][i], upper_tri_values[i]) for i in top_k_indices]

with open("src/stats/Closest Speakers.txt","w") as f:
    for speaker_id1, speaker_id2, similarity in sorted(closest_pairs, key=lambda x: -x[2]):
        speaker_name1 = speaker_id_to_name[speaker_id1]
        speaker_name2 = speaker_id_to_name[speaker_id2]
        print(f"{speaker_name1} <-> {speaker_name2} : Similarity = {similarity:.4f}", file=f)
