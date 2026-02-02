import csv
import pandas as pd
from gensim import corpora, models, similarities
from tqdm import tqdm

tqdm.pandas()

INPUT_CSV = "src/dataset/clean.csv"
OUTPUT_CSV = "src/dataset/keywords.csv"

N_ROWS = 100_000

dataframe = pd.read_csv(INPUT_CSV, index_col=0)
size = len(dataframe)

def token_stream():
    for speech in dataframe.clean_speech:
        tokens = speech.split()
        yield tokens

try:
    dictionary = corpora.Dictionary.load("src/models/greek.dict")
    print("Dictionary loaded from file.")
except FileNotFoundError:
    print("No existing dictionary found. Creating a new one.")
    dictionary = corpora.Dictionary(prune_at=None)
    for tokens in tqdm(token_stream(), total=size):
        dictionary.add_documents([tokens])

    FILTER_PERCENTAGE = 0.05
    
    # Write to a csv the tokens that appear in more than 5% of the documents
    with open("src/dataset/filtered_tokens.csv", "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["token"])
        for token_id, doc_freq in dictionary.dfs.items():
            if doc_freq > FILTER_PERCENTAGE * size:
                print(f"Filtering out token: {dictionary[token_id]} with doc freq: {doc_freq}")
                writer.writerow([dictionary[token_id]])

    dictionary.filter_extremes(no_above=FILTER_PERCENTAGE)
    dictionary.compactify()
    dictionary.save("src/models/greek.dict")   
    
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
    tfidf_model = models.TfidfModel.load("src/models/greek.tfidf")
    print("TF-IDF model loaded from file.")
except FileNotFoundError:
    print("No existing TF-IDF model found. Creating a new one.")
    tfidf_model = models.TfidfModel(corpus)
    tfidf_model.save("src/models/greek.tfidf")

try:
    lsi_model = models.LsiModel.load("src/models/greek.lsi")
    print("LSI model loaded from file.")
except FileNotFoundError:
    print("No existing LSI model found. Creating a new one.")
    lsi_model = models.LsiModel(corpus, num_topics=100, id2word=dictionary, random_seed=42)
    lsi_model.save("src/models/greek.lsi")


try:
    index = similarities.Similarity.load("src/models/index/greek.lsi", mmap='r')
    print("Similarity index loaded from file.")
except FileNotFoundError:
    print("No existing similarity index found. Creating a new one.")
    index = similarities.Similarity(
        output_prefix="src/models/index/greek.lsi",
        num_best=10,
        corpus=lsi_model[tfidf_model[corpus]],
        num_features=len(dictionary),
    )
    index.save("src/models/index/greek.lsi")


# Extract most important topics from LSI model
topic_scores = [(index, score) for index, score in enumerate(lsi_model.projection.s)]
topic_scores.sort(key=lambda x: abs(x[1]), reverse=True)
print("Most important topics by score:")
for topic_id, score in topic_scores[:10]:
    topic_str = " ".join(word for word, _ in lsi_model.show_topic(topic_id))
    print(f"\tTopic {topic_id}: {score:.4f} : {topic_str}")