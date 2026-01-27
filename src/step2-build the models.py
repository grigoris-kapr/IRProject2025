import pandas as pd
from gensim import corpora, models, similarities
from tqdm import tqdm

tqdm.pandas()

INPUT_CSV = "dataset/clean.csv"
N_ROWS = 100_000

dataframe = pd.read_csv(INPUT_CSV, index_col=0, nrows=N_ROWS)
size = len(dataframe)

def token_stream():
    for speech in dataframe.clean_speech:
        tokens = speech.split()
        yield tokens

try:
    dictionary = corpora.Dictionary.load("models/greek.dict")
    print("Dictionary loaded from file.")
except FileNotFoundError:
    print("No existing dictionary found. Creating a new one.")
    dictionary = corpora.Dictionary(prune_at=None)
    for tokens in tqdm(token_stream(), total=size):
        dictionary.add_documents([tokens])
    dictionary.save("models/greek.dict")   
    
class BowCorpus:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for tokens in token_stream():
            yield self.dictionary.doc2bow(tokens)

    def __getitem__(self, index):
        tokens = dataframe.clean_speech[index].split()
        return self.dictionary.doc2bow(tokens)
    
corpus = BowCorpus(dictionary)

try:
    tfidf_model = models.TfidfModel.load("models/greek.tfidf")
    print("TF-IDF model loaded from file.")
except FileNotFoundError:
    print("No existing TF-IDF model found. Creating a new one.")
    tfidf_model = models.TfidfModel(corpus)
    tfidf_model.save("models/greek.tfidf")

try:
    lsi_model = models.LsiModel.load("models/greek.lsi")
    print("LSI model loaded from file.")
except FileNotFoundError:
    print("No existing LSI model found. Creating a new one.")
    lsi_model = models.LsiModel(corpus, id2word=dictionary, random_seed=42)
    lsi_model.save("models/greek.lsi")


try:
    index = similarities.Similarity.load("models/index/greek.lsi", mmap='r')
    print("Similarity index loaded from file.")
except FileNotFoundError:
    print("No existing similarity index found. Creating a new one.")
    index = similarities.Similarity(
        output_prefix="models/index/greek.lsi",
        num_best=10,
        corpus=lsi_model[tfidf_model[corpus]],
        num_features=len(dictionary),
    )
    index.save("models/index/greek.lsi")