import pandas as pd  # type: ignore[reportMissingModuleSource]
import os

# ============================================================
# SUPERSTORE DATA CLEANING
# ============================================================

print("=" * 60)
print("SUPERSTORE DATA CLEANING")
print("=" * 60)

# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

input_file = "data/raw/superstore.csv"
output_file = "data/processed/superstore_cleaned.csv"

# ------------------------------------------------------------
# 2. Create processed folder
# ------------------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

# ------------------------------------------------------------
# 3. Load dataset
# ------------------------------------------------------------

print("\nLoading dataset...")

try:
    df = pd.read_csv(
        input_file,
        encoding="utf-8"
    )

except UnicodeDecodeError:
    print("UTF-8 encoding failed.")
    print("Trying Latin-1 encoding...")

    df = pd.read_csv(
        input_file,
        encoding="latin1"
    )

print("Dataset loaded successfully!")

# ------------------------------------------------------------
# 4. Original dataset information
# ------------------------------------------------------------

print("\nOriginal dataset:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# ------------------------------------------------------------
# 5. Clean column names
# ------------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
)

# ------------------------------------------------------------
# 6. Remove duplicate rows
# ------------------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

if duplicate_count > 0:

    df = df.drop_duplicates()

    print("Duplicate rows removed:", duplicate_count)

else:

    print("No duplicate rows found.")

# ------------------------------------------------------------
# 7. Check missing values
# ------------------------------------------------------------

print("\nMissing values before cleaning:")

print(df.isnull().sum())

# ------------------------------------------------------------
# 8. Convert Order Date
# ------------------------------------------------------------

print("\nConverting Order Date...")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

# ------------------------------------------------------------
# 9. Convert Ship Date
# ------------------------------------------------------------

print("Converting Ship Date...")

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    errors="coerce"
)

# ------------------------------------------------------------
# 10. Check invalid dates
# ------------------------------------------------------------

invalid_order_dates = df["Order Date"].isnull().sum()
invalid_ship_dates = df["Ship Date"].isnull().sum()

print("\nInvalid Order Dates:", invalid_order_dates)
print("Invalid Ship Dates:", invalid_ship_dates)

# ------------------------------------------------------------
# 11. Convert numeric columns
# ------------------------------------------------------------

numeric_columns = [
    "Row ID",
    "Postal Code",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

print("\nChecking numeric columns...")

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("Numeric columns checked.")

# ------------------------------------------------------------
# 12. Check missing values after conversion
# ------------------------------------------------------------

print("\nMissing values after conversion:")

print(df.isnull().sum())

# ------------------------------------------------------------
# 13. Handle missing values
# ------------------------------------------------------------

for column in df.columns:

    if df[column].isnull().sum() > 0:

        if pd.api.types.is_numeric_dtype(df[column]):

            df[column] = df[column].fillna(
                df[column].median()
            )

        else:

            df[column] = df[column].fillna(
                "Unknown"
            )

# ------------------------------------------------------------
# 14. Create useful analytical columns
# ------------------------------------------------------------

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

df["Profit Margin"] = (
    df["Profit"] / df["Sales"]
) * 100

df["Profit Margin"] = df["Profit Margin"].replace(
    [float("inf"), float("-inf")],
    0
)

df["Order Year"] = df["Order Date"].dt.year

df["Order Month"] = df["Order Date"].dt.month

df["Order Month Name"] = (
    df["Order Date"].dt.month_name()
)

df["Order Quarter"] = (
    "Q" + df["Order Date"].dt.quarter.astype(str)
)

# ------------------------------------------------------------
# 15. Reset index
# ------------------------------------------------------------

df = df.reset_index(drop=True)

# ------------------------------------------------------------
# 16. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print("\nCleaned dataset saved successfully!")

print("Location:")
print(output_file)

# ------------------------------------------------------------
# 17. Final dataset information
# ------------------------------------------------------------

print("\nFinal dataset:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nRemaining missing values:")

print(df.isnull().sum().sum())

print("\nNew analytical columns:")

print("- Shipping Days")
print("- Profit Margin")
print("- Order Year")
print("- Order Month")
print("- Order Month Name")
print("- Order Quarter")

print("\nFinal data types:")

print(df.dtypes)

# ------------------------------------------------------------
# 18. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)