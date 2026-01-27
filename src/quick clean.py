import pandas as pd

df = pd.read_csv("dataset/old clean.csv", index_col=0)
print(df[:50])
print("After removing custom stopwords:")

# manually selected stopwords
custom_stopwords = []
with open("dataset/removed terms 3.txt", "r") as f:
    for line in f:
        term = line.strip()
        if term:
            custom_stopwords.append(term)

def clean_speech(speech):
    tokens = speech.split()
    cleaned_tokens = [token for token in tokens if token not in custom_stopwords and len(token) > 3]
    return " ".join(cleaned_tokens)

df["clean_speech"] = df["clean_speech"].apply(clean_speech)
clean_df = df[df["clean_speech"].str.strip() != ""]

print(df[:50])
print(f"Original rows: {len(df)}, Cleaned rows: {len(clean_df)}")
print(clean_df[:50])

clean_df.to_csv("dataset/clean.csv")