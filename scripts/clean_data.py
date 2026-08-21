import pandas as pd  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
import os

# ============================================================
# SUPERSTORE DATA CLEANING
# ============================================================

INPUT_FILE = "data/raw/superstore.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "data/processed/superstore_cleaned.csv"


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD DATASET
# ============================================================

try:
    df = pd.read_csv(INPUT_FILE, encoding="utf-8")

except UnicodeDecodeError:
    print("UTF-8 encoding failed.")
    print("Trying Latin-1 encoding...")
    df = pd.read_csv(INPUT_FILE, encoding="latin1")


# ============================================================
# START
# ============================================================

print("\n" + "=" * 70)
print("SUPERSTORE DATA CLEANING")
print("=" * 70)

print("\nOriginal rows:", len(df))
print("Original columns:", len(df.columns))


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)

print("\nColumn names cleaned.")


# ============================================================
# REMOVE DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

df = df.drop_duplicates()

print("Duplicate rows after cleaning:", df.duplicated().sum())


# ============================================================
# CONVERT DATES
# ============================================================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["ship_date"] = pd.to_datetime(
    df["ship_date"],
    errors="coerce"
)

print("\nOrder Date and Ship Date converted.")


# ============================================================
# CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "row_id",
    "postal_code",
    "sales",
    "quantity",
    "discount",
    "profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("Numeric columns converted.")


# ============================================================
# MISSING VALUES
# ============================================================

print("\nMissing values before final cleaning:")

print(df.isnull().sum())


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

for column in df.columns:

    if df[column].isnull().sum() > 0:

        if pd.api.types.is_numeric_dtype(df[column]):

            df[column] = df[column].fillna(
                df[column].median()
            )

        else:

            df[column] = df[column].fillna("Unknown")


# ============================================================
# CREATE NEW ANALYTICAL COLUMNS
# ============================================================

df["shipping_days"] = (
    df["ship_date"] - df["order_date"]
).dt.days


df["profit_margin"] = (
    df["profit"] / df["sales"]
) * 100


df["profit_margin"] = df["profit_margin"].replace(
    [float("inf"), float("-inf")],
    0
)


df["order_year"] = df["order_date"].dt.year

df["order_month"] = df["order_date"].dt.month

df["order_month_name"] = (
    df["order_date"].dt.month_name()
)

df["order_quarter"] = (
    "Q" + df["order_date"].dt.quarter.astype(str)
)


# ============================================================
# RESET INDEX
# ============================================================

df = df.reset_index(drop=True)


# ============================================================
# SAVE CLEAN DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFinal rows:", len(df))
print("Final columns:", len(df.columns))

print("\nRemaining missing values:")
print(df.isnull().sum().sum())

print("\nNew analytical columns:")
print("- shipping_days")
print("- profit_margin")
print("- order_year")
print("- order_month")
print("- order_month_name")
print("- order_quarter")

print("\nCleaned dataset saved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)