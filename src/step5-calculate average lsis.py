from Models import Models
import numpy as np
from collections import defaultdict
from tqdm import tqdm
import pandas as pd


models = Models()

def dense_lsi(lsi_vector):
	dense_vector = np.zeros(models.lsi.num_topics)
	for idx, value in lsi_vector:
		dense_vector[idx] = value
	return dense_vector

average_vectors = defaultdict(list)

group = models.dataset.groupby(['member_name', 'government', 'political_party'], sort=False)
for (member_name, government, political_party), group_rows in tqdm(group):
    lsi_vectors = []
    for idx, row in group_rows.iterrows():
        bow = models.corpus[idx]
        if not bow:
            continue
        tfidf_vector = models.tfidf[bow]
        lsi_vector = models.lsi[tfidf_vector]
        dense_vector = dense_lsi(lsi_vector)
        lsi_vectors.append(dense_vector)
    if lsi_vectors:
        average_vector = np.mean(lsi_vectors, axis=0)
        average_vectors[(member_name, government, political_party)] = average_vector
    
average_vectors_df = pd.DataFrame([
    {
        'member_name': member_name,
        'government': government,
        'political_party': political_party,
        'average_lsi_vector': average_vector.tolist()
    }
    for (member_name, government, political_party), average_vector in average_vectors.items()
])

average_vectors_df.to_parquet("src/dataset/average_member_government_party_lsi_vectors.parquet", index=False)