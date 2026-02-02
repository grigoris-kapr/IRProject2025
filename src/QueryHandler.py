from src.Models import Models
import pandas as pd
import heapq
import numpy as np
from scipy.spatial.distance import cosine

class QueryHandler:
	def __init__(self):
		self.models = Models()

	def get_keywords_for_index(self, index):
		row = self.models.keywords.loc[index]
		keywords = row['keywords'] if pd.notna(row['keywords']).all() else []
		return keywords
		
	def get_relevant_documents(self, query_text):
		processed_query = self.models.light_pipeline.annotate(query_text)["clean_lemma"]
		query_bow = self.models.dictionary.doc2bow(processed_query)
		query_tfidf = self.models.tfidf[query_bow]
		query_lsi = self.models.lsi[query_tfidf]
		
		results = []
		for doc_position, _ in self.models.index[query_lsi]:
			speech = self.models.dataset.speech.iloc[doc_position]
			keywords = self.get_keywords_for_index(doc_position)
			results.append((speech, keywords))
		
		return results
	
	def get_keywords_for_member(self, member_name):
		member_rows = self.models.keywords[self.models.keywords['member_name'] == member_name]
		grouped = member_rows.groupby('government', sort = False)
		result = {}
		for government, group in grouped:
			heap = []
			for _, row in group.iterrows():
				if pd.notna(row['keywords']).all() and pd.notna(row['keyword_scores']).all():
					keywords = row['keywords']
					scores = list(map(float, row['keyword_scores']))
					for keyword, score in zip(keywords, scores):
						heapq.heappush(heap, (-score, keyword))  # Use negative score for max-heap behavior
			top_keywords = []
			seen = set()
			while heap and len(top_keywords) < 5:
				score, keyword = heapq.heappop(heap)
				if keyword not in seen:
					seen.add(keyword)
					top_keywords.append(keyword)

			result[government] = top_keywords

		return result
	
	def get_keywords_for_party(self, political_party):
		party_rows = self.models.keywords[self.models.keywords['political_party'] == political_party]
		grouped = party_rows.groupby('government', sort = False)
		result = {}
		for government, group in grouped:
			heap = []
			for _, row in group.iterrows():
				if pd.notna(row['keywords']).all() and pd.notna(row['keyword_scores']).all():
					keywords = row['keywords']
					scores = list(map(float, row['keyword_scores']))
					for keyword, score in zip(keywords, scores):
						heapq.heappush(heap, (-score, keyword))  # Use negative score for max-heap behavior
			top_keywords = []
			seen = set()
			while heap and len(top_keywords) < 5:
				score, keyword = heapq.heappop(heap)
				if keyword not in seen:
					seen.add(keyword)
					top_keywords.append(keyword)

			result[government] = top_keywords

		return result

	def get_member_errors(self, member_name):
		member_lsi_rows = self.models.lsis[self.models.lsis['member_name'] == member_name]

		errors = {}
		for _, row in member_lsi_rows.iterrows():
			government = row['government']
			party = row['political_party']
			member_vector = np.array(row['average_lsi_vector'])
			
			government_party_rows = self.models.lsis[(self.models.lsis['government'] == government) & (self.models.lsis['political_party'] == party)]
			vectors = []
			for _, group in government_party_rows.iterrows():
				vectors.append(np.array(group["average_lsi_vector"]))
			if vectors:
				mean_vector = np.mean(vectors, axis=0)
				error = cosine(member_vector, mean_vector)
				errors[government] = error
				
		return errors