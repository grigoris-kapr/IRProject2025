import gensim
from gensim.corpora import Dictionary
from gensim.models import LsiModel
import pandas as pd


INPUT_CSV = "~/CSD/7ο εξ/IR/normalized_proceedings.csv"
TEMP_MODEL_FNAME = "./DataTinkering/lsi.model"
NUM_TOPICS = 20

# speeches in the last column of the csv
# Need to have already been preprocessed. 
# Assumptions made while writing this code include:
#   1. lowercase
#   2. only valid greek letters (no punctuation, numbers)
#   3. removed common words
df = pd.read_csv(INPUT_CSV)
tokenized_speeches = [speech.split(" ") for speech in df.iloc[0:200000, -1].tolist()]

print(f"Analysing {len(tokenized_speeches):,} speches consisting of {tokenized_speeches.__sizeof__():,} bytes of data")
print(f"First speech date: {df.iloc[0,1]}\nLast speech date: {df.iloc[200000,1]}")

# TODO test with hashdictionary for effectiveness and size
dct = Dictionary(tokenized_speeches)

print(f"Found to contain {len(dct):,} unique tokens")

corpus = [dct.doc2bow(text) for text in tokenized_speeches]

# run the LSI
model = LsiModel(corpus, num_topics=NUM_TOPICS, id2word=dct)
vect_corpus = model[corpus]

model.save(TEMP_MODEL_FNAME)  # save model

topics = model.get_topics()

# For each topic, print the 10 words most closely associated with it.
# Vectorized for efficiency
for topic_id, topic in enumerate(topics):
    top_words = [dct[id] for id in topic.argsort()[-10:][::-1]]
    print(f"Topic #{topic_id}: {', '.join(top_words)}")
