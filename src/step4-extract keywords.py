from Models import Models
from tqdm import tqdm
import pyarrow as pa
import pyarrow.parquet as pq

models = Models()

def extract_keywords(bow, top_n = 5):
	tfidf_vector = models.tfidf[bow]
	keyword_scores = [(keyword, score) for term_id, score in tfidf_vector for keyword in [models.dictionary[term_id]]]
	sorted_keywords = sorted(keyword_scores, key=lambda x: x[1], reverse=True)
	return sorted_keywords[:top_n]

rows = []

members = models.dataset["member_name"].to_numpy()
political_parties = models.dataset["political_party"].to_numpy()
governments = models.dataset["government"].to_numpy()

for idx, bow in enumerate(tqdm(models.corpus)):
    top_keywords = extract_keywords(bow)
    keywords, scores = zip(*top_keywords) if top_keywords else ([], [])

    rows.append({
        "index": idx,
        "member_name": members[idx],
        "political_party": political_parties[idx],
        "government": governments[idx],
        "keywords": list(keywords),
        "keyword_scores": [float(s) for s in scores],
    })

table = pa.Table.from_pylist(rows)
pq.write_table(table, "src/stats/keywords.parquet", compression="snappy")