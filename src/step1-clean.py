import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *

import pandas as pd

spark = sparknlp.start()

INPUT_CSV = "src/dataset/original.csv"
OUTPUT_PARQUET = "src/dataset/clean.parquet"

df = spark.read.option("header", "true").csv(INPUT_CSV)

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
finisher = (
    Finisher()
    .setInputCols(["lemma"])
    .setOutputCols(["clean_speech"])
    .setCleanAnnotations(True)
    .setOutputAsArray(False)
    .setAnnotationSplitSymbol(" ")
)
pipeline = Pipeline(
    stages=[document_assembler, tokenizer, normalizer, stopwords, lemmatizer, finisher]
)

model = pipeline.fit(df)
model.write().overwrite().save("src/models/sparknlp_pipeline")
processed_df = model.transform(df)

print("Converting to Pandas DataFrame")
pdf = processed_df.toPandas()
pdf = pdf[pdf.clean_speech.str.len() > 0].reset_index(drop=True)
print("Saving cleaned data to Parquet")
pdf.to_parquet(OUTPUT_PARQUET)