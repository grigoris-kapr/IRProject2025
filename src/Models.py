from gensim import corpora, models, similarities
import pandas as pd
import sparknlp
from sparknlp.base import LightPipeline, PipelineModel


class Models:
	def __init__(self):
		DATASET_CSV = "src/dataset/clean.csv"
		KEYWORDS_CSV = "src/stats/keywords.csv"
		LSI_VECTORS_PARQUET = "src/dataset/average_member_government_party_lsi_vectors.parquet"

		self.dataset = pd.read_csv(DATASET_CSV, index_col=0)
		self.keywords = pd.read_csv(KEYWORDS_CSV, index_col=0)
		self.lsis = pd.read_parquet(LSI_VECTORS_PARQUET)
		self.spark = sparknlp.start()
		self.light_pipeline = LightPipeline(PipelineModel.load("src/models/sparknlp_pipeline"))

		try:
			self.dictionary = corpora.Dictionary.load("src/models/greek.dict")
			print("Dictionary loaded from file.")
		except FileNotFoundError:
			raise Exception("Dictionary file not found. Please build the models first.")

		try:
			self.tfidf = models.TfidfModel.load("src/models/greek.tfidf")
			print("TF-IDF model loaded from file.")
		except FileNotFoundError:
			raise Exception("TF-IDF model file not found. Please build the models first.")

		try:
			self.lsi = models.LsiModel.load("src/models/greek.lsi")
			print("LSI model loaded from file.")
		except FileNotFoundError:
			raise Exception("LSI model file not found. Please build the models first.")

		try:
			self.index = similarities.Similarity.load("src/models/index/greek.lsi")
			print("Similarity index loaded from file.")
		except FileNotFoundError:
			raise Exception("Similarity index file not found. Please build the models first.")

		class BowCorpus:
			def __init__(self, dictionary, dataset):
				self.dictionary = dictionary
				self.dataset = dataset

			def __iter__(self):

				def token_stream():
					for speech in self.dataset.clean_speech:
						tokens = speech.split()
						yield tokens
				
				for tokens in token_stream():
					yield self.dictionary.doc2bow(tokens)

			def __getitem__(self, index):
				tokens = self.dataset.clean_speech[index].split()
				return self.dictionary.doc2bow(tokens)

			def __len__(self):
				return len(self.dataset)
			
		self.corpus = BowCorpus(self.dictionary, self.dataset)