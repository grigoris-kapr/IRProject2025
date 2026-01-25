import sparknlp
from sparknlp.base import *
from sparknlp.annotator import *

spark = sparknlp.start()

INPUT_CSV = "dataset/Greek_Parliament_Proceedings_1989_2020.csv"
OUTPUT_CSV = "dataset/clean.csv"

df = spark.read.option("header", "true").csv(INPUT_CSV)

dropped_columns = [
    "parliamentary_period",
    "parliamentary_session",
    "parliamentary_sitting",
    "member_region",
    "roles",
]
wanted_columns_df = df.drop(*dropped_columns).dropna()

# Create the preprocessing pipeline
document_assembler = DocumentAssembler().setInputCol("speech").setOutputCol("document")
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
normalizer = (
    Normalizer()
	.setInputCols(["token"])
	.setOutputCol("normalized")
	.setLowercase(True)
	.setCleanupPatterns(["\\p{M}"])
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

model = pipeline.fit(wanted_columns_df)
model.write().overwrite().save("models/sparknlp_pipeline")
processed_df = model.transform(wanted_columns_df)

clean_df = processed_df.dropna().filter(processed_df.clean_speech != "")

pd_df = clean_df.toPandas()
pd_df.to_csv(OUTPUT_CSV)