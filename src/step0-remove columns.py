import pandas as pd

INPUT_CSV = "src/dataset/Greek_Parliament_Proceedings_1989_2020.csv"
OUTPUT_PARQUET = "src/dataset/original.parquet"

df = pd.read_csv(INPUT_CSV)

dropped_columns = [
    "parliamentary_period",
    "parliamentary_session",
    "parliamentary_sitting",
	"sitting_date",
    "member_region",
	"member_gender",
    "roles",
]
wanted_columns_df = df.drop(columns=dropped_columns).dropna()

wanted_columns_df.to_parquet(OUTPUT_PARQUET, index=False)