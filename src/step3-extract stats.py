import csv
from gensim import models
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from Models import Models
from tqdm import tqdm

# N_ROWS = 100_000
# Load data and models
# dataset = pd.read_csv("src/dataset/clean.csv", index_col=0, nrows=N_ROWS)

models = Models()

# =================================================
# Extract keywords
# =================================================
def extract_keywords(bow, top_n = 5):
    tfidf_vector = models.tfidf[bow]
    # get the top scoring keywords from the tfidf vector
    keyword_scores = [(keyword, score) for term_id, score in tfidf_vector for keyword in [models.dictionary[term_id]]]
    sorted_keywords = sorted(keyword_scores, key=lambda x: x[1], reverse=True)
    return sorted_keywords[:top_n]
with open("src/stats/keywords.csv","w") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "member_name", "government", "keywords", "keyword_scores"])

    for idx, bow in enumerate(tqdm(models.corpus)):
        top_keywords = extract_keywords(bow)
        keywords, scores = zip(*top_keywords) if top_keywords else ([], [])
        member_name = models.dataset.iloc[idx]['member_name']
        government = models.dataset.iloc[idx]['government']
        writer.writerow([idx, member_name, government, "|".join(keywords), "|".join(f"{score:.4f}" for score in scores)])


    

# Extract top topics

NUM_TOPICS = 10

with open("src/stats/Top Topics.txt","w") as f:
    tVectors = models.lsi.projection.s
    for t in range(NUM_TOPICS):
        top_words_with_contribution = models.lsi.show_topic(t)
        top_words = []
        for word, contr in top_words_with_contribution:
            top_words.append(word)
        print(  f"Topic {t} \n" + \
                f"\tScore: {tVectors[t]:6.2f}\n" + \
                f"\tTop Words: {' '.join(top_words)}\n\n",
                file=f)
        
    # Also, print salient words for topics by capturing the LSI model's log
    import io
    import logging

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)   # ignore DEBUG messages
    handler.setFormatter(logging.Formatter('%(message)s'))

    logger = logging.getLogger('gensim')
    logger.addHandler(handler)

    models.lsi.print_debug(num_topics=NUM_TOPICS, num_words=10)

    logger.removeHandler(handler)

    # print to same file
    print(log_stream.getvalue(), file=f)


    
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
