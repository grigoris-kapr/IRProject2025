import pickle
import re
import unicodedata
from collections import defaultdict
from multiprocessing import Pool, cpu_count

import pandas as pd

INPUT_CSV = "~/CSD/7ο εξ/IR/Greek_Parliament_Proceedings_1989_2020.csv"
OUTPUT_FILE = "./DataTinkering/proposed_stopwords.txt"

MAX_CPUS = 6
CHUNK_SIZE = 50_000  # processes one CHUNK per CPU; make sure not to overload RAM
CHECKPOINT_EVERY = 1000  # checkpoint every X chunks
REPORT_EVERY = 1  # report progress every X chunks
K = 5000  # number of top terms to output


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


# Process one chunk of data. Chunk size defined at top of file.
def process_chunk(df_chunk):
    local_df = defaultdict(int)
    speech_col = df_chunk.columns[-1]
    local_processed_docs = 0

    for speech in df_chunk[speech_col]:
        text = normalize_text(speech)
        # extract unique terms of size >= 3
        terms = set(t for t in text.split() if len(t) >= 3)

        for term in terms:
            local_df[term] += 1

        local_processed_docs += 1

    return local_df, local_processed_docs


# Merge local_df into global_df term by term
def merge_df_dicts(global_df, local_df):
    for term, count in local_df.items():
        global_df[term] += count


def compute_document_frequencies(reader):
    global_df = defaultdict(int)
    global_processed_docs = 0

    with Pool(processes=min(MAX_CPUS, cpu_count())) as pool:
        for i, res in enumerate(pool.imap_unordered(process_chunk, reader), start=1):
            local_df = res[0]
            local_processed_docs = res[1]
            # merge dicts
            merge_df_dicts(global_df, local_df)
            # count all docs
            global_processed_docs += local_processed_docs

            if i % REPORT_EVERY == 0:
                print(f"Processed {i} chunks")

            # Optional checkpoint
            if i % CHECKPOINT_EVERY == 0:
                with open("df_checkpoint.pkl", "wb") as f:
                    pickle.dump(global_df, f)

                print(f"Checkpoint saved after {i * CHUNK_SIZE:,} documents")

    return global_df, global_processed_docs


# ============================================
# ============= EXEC STARTS HERE =============
# ============================================

reader = pd.read_csv(INPUT_CSV, chunksize=CHUNK_SIZE)
df_counts, processed_docs = compute_document_frequencies(reader)

sorted_terms = sorted(df_counts.items(), key=lambda x: x[1], reverse=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("term\tdocument_frequency\n")
    for term, df in sorted_terms[:K]:
        f.write(f"{term}\t{df}\n")

print(
    f"Finished analysing {processed_docs:,} documents containing {len(df_counts):,} unique terms."
)
