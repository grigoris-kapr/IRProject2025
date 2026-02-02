from Models import Models
import csv
from tqdm import tqdm

models = Models()

def extract_keywords(bow, top_n = 5):
	tfidf_vector = models.tfidf[bow]
	# get the top scoring keywords from the tfidf vector
	keyword_scores = [(keyword, score) for term_id, score in tfidf_vector for keyword in [models.dictionary[term_id]]]
	sorted_keywords = sorted(keyword_scores, key=lambda x: x[1], reverse=True)
	return sorted_keywords[:top_n]

with open("src/stats/keywords.csv","w") as f:
	writer = csv.writer(f)
	writer.writerow(["index", "member_name", "political_party","government", "keywords", "keyword_scores"])

	for idx, bow in enumerate(tqdm(models.corpus)):

		top_keywords = extract_keywords(bow)
		keywords, scores = zip(*top_keywords) if top_keywords else ([], [])
		member_name = models.dataset.iloc[idx]['member_name']
		political_party = models.dataset.iloc[idx]['political_party']
		government = models.dataset.iloc[idx]['government']
		writer.writerow([idx, member_name, political_party, government, "|".join(keywords), "|".join(f"{score:.4f}" for score in scores)])