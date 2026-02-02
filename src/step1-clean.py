import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *

# from dataset.removed_terms_3 import custom_stopwords
import pandas as pd

spark = sparknlp.start()

INPUT_CSV = "src/dataset/Greek_Parliament_Proceedings_1989_2020.csv"
OUTPUT_CSV = "src/dataset/clean.csv"

df = spark.read.option("header", "true").csv(INPUT_CSV)

dropped_columns = [
    "parliamentary_period",
    "parliamentary_session",
    "parliamentary_sitting",
    "member_region",
    "roles",
]
wanted_columns_df = df.drop(*dropped_columns).dropna()

filtered_tokens_df = pd.read_csv("src/dataset/filtered_tokens.csv")
custom_stopwords_list = filtered_tokens_df.iloc[:, 0].tolist()

# Create the preprocessing pipeline
document_assembler = DocumentAssembler().setInputCol("speech").setOutputCol("document")
tokenizer = (
	Tokenizer()
	.setInputCols(["document"])
	.setOutputCol("token")
	.setMinLength(3)
)
normalizer = (
    Normalizer()
	.setInputCols(["token"])
	.setOutputCol("normalized")
	.setLowercase(True)
	.setMinLength(3)
)
stopwords = (
    StopWordsCleaner()
    .pretrained("stopwords_iso", "el")
    .setInputCols(["normalized"])
    .setOutputCol("clean_normalized")
    .setCaseSensitive(False)
)
lemmatizer = (
    LemmatizerModel.pretrained("lemma", "el")
    .setInputCols(["clean_normalized"])
    .setOutputCol("lemma")
)
custom_stopwords = (
    StopWordsCleaner()
    .setStopWords(custom_stopwords_list)
    .setInputCols(["lemma"])
    .setOutputCol("clean_lemma")
    .setCaseSensitive(False)
)
finisher = (
    Finisher()
    .setInputCols(["clean_lemma"])
    .setOutputCols(["clean_speech"])
    .setCleanAnnotations(True)
    .setOutputAsArray(False)
    .setAnnotationSplitSymbol(" ")
)
pipeline = Pipeline(
    stages=[document_assembler, tokenizer, normalizer, stopwords, lemmatizer, custom_stopwords, finisher]
)

model = pipeline.fit(wanted_columns_df)
model.write().overwrite().save("src/models/sparknlp_pipeline")
processed_df = model.transform(wanted_columns_df)

clean_df = processed_df.dropna().filter(processed_df.clean_speech != "")

print("Converting to Pandas DataFrame")
pd_df = clean_df.toPandas()
print("Saving cleaned data to CSV")
pd_df.to_csv(OUTPUT_CSV)