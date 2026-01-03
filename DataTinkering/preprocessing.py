import pandas as pd
import re
import unicodedata
from collections import defaultdict
from multiprocessing import Pool, cpu_count
import pickle

INPUT_CSV = "~/CSD/7ο εξ/IR/Greek_Parliament_Proceedings_1989_2020.csv"
OUTPUT_CSV = "~/CSD/7ο εξ/IR/normalized_proceedings.csv"
SHORT_OUTPUT_CSV = "~/CSD/7ο εξ/IR/short_normalized_proceedings.csv"

# needs to be a file containing the words to be deleted, 
# normalized the same as the text, split one word per line
COMMON_TERMS_FILE = "./DataTinkering/removed_terms 1.txt"

MAX_CPUS = 6
CHUNK_SIZE = 50_000        # processes one CHUNK per CPU; make sure not to overload RAM
REPORT_EVERY = 1           # report progress every X chunks


def loadCommonWords():
    with open(COMMON_TERMS_FILE, "r", encoding="utf-8") as f:
        return set(
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        )

# Normalize the text. Each section of the code does a different type of normalization (lowercase, character-set, whitespace...)
# Could make toggles for each bit...
def normalize_text(text):
    if not isinstance(text, str):
        return ""

    # lowercase
    text = text.lower()

    # remove accents
    # text = unicodedata.normalize("NFD", text)
    # text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")

    # keep only greek letters and spaces
    text = re.sub(r"[^α-ωάέήίόύώϊΐϋΰ\s]", " ", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text

def removeCommonWords(text, commonWordsSet):
    if not text:
        return ""
    
    tokens = text.split()
    filteredTokens = [ tok for tok in tokens if tok not in commonWordsSet and len(tok) >= 3]

    return " ".join(filteredTokens)

def preprocess_speech(text, commonWordsSet):
    text = normalize_text(text)
    text = removeCommonWords(text, commonWordsSet)
    return text

def process_chunk(df_chunk):
    # filter rows without assigned member 
    df_chunk = df_chunk[df_chunk.iloc[:, 0].notna()].copy()

    if df_chunk.empty:
        return df_chunk

    # 2. format text (in last column)
    speech_col = df_chunk.columns[-1]
    df_chunk[speech_col] = df_chunk[speech_col].apply(preprocess_speech, args=(commonWordsSet,))

    # some speaches contain only common words. filter those rows
    df_chunk = df_chunk[df_chunk[speech_col].str.len() > 0].copy()

    return df_chunk

commonWordsSet = loadCommonWords()

reader = pd.read_csv(INPUT_CSV, chunksize=CHUNK_SIZE)
with Pool(processes=min(MAX_CPUS, cpu_count())) as pool:
    for i, res in enumerate(pool.imap_unordered(process_chunk, reader), start=1):
        if res.empty:
                continue

        res.to_csv(
            OUTPUT_CSV,
            mode="a",
            index=False,
            header=(i == 1)
        )

        if i == 1:
            res.to_csv(
            SHORT_OUTPUT_CSV,
            mode="a",
            index=False,
            header=(i == 1)
        )

        if i % REPORT_EVERY == 0:
            print(f"Processed {i} chunks")



