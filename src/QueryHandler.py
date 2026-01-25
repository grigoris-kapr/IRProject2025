from gensim import corpora, models, similarities
import pandas as pd
import sparknlp
from sparknlp.base import LightPipeline, PipelineModel

class QueryHandler:
	def __init__(self):
		self.dataset = pd.read_csv("dataset/clean.csv", index_col=0, nrows=10_000)
		self.spark = sparknlp.start()
		self.light_pipeline = LightPipeline(PipelineModel.load("models/sparknlp_pipeline"))
		try:
			self.dictionary = corpora.Dictionary.load("models/greek.dict")
			print("Dictionary loaded from file.")
		except FileNotFoundError:
			raise Exception("Dictionary file not found. Please build the models first.")

		try:
			self.tfidf_model = models.TfidfModel.load("models/greek.tfidf")
			print("TF-IDF model loaded from file.")
		except FileNotFoundError:
			raise Exception("TF-IDF model file not found. Please build the models first.")

		try:
			self.lsi_model = models.LsiModel.load("models/greek.lsi")
			print("LSI model loaded from file.")
		except FileNotFoundError:
			raise Exception("LSI model file not found. Please build the models first.")

		try:
			self.index = similarities.Similarity.load("models/index/greek.lsi", mmap='r')
			print("Similarity index loaded from file.")
		except FileNotFoundError:
			raise Exception("Similarity index file not found. Please build the models first.")
		
	def query(self, query_text):
		processed_query = self.light_pipeline.annotate(query_text)["lemma"]
		query_bow = self.dictionary.doc2bow(processed_query)
		query_tfidf = self.tfidf_model[query_bow]
		query_lsi = self.lsi_model[query_tfidf]
		
		results = []
		for doc_position, doc_score in self.index[query_lsi]:
			speech_text = self.dataset.speech[doc_position]
			results.append(speech_text)
		
		return results

qh = QueryHandler()
results = qh.query("Παράδειγμα ερώτησης για αναζήτηση.")
for res in results[:5]:
	print(res)