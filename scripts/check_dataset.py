import importlib
import os


try:
    pd = importlib.import_module("pandas")
except ImportError:
    print("ERROR: pandas is not installed in the active Python environment.")
    print("Install it with: python -m pip install pandas")
    raise SystemExit(1)

# ============================================================
# DATASET PATH
# ============================================================

file_path = "data/raw/superstore.csv"


# ============================================================
# CHECK FILE EXISTS
# ============================================================

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    print("Expected file:")
    print(file_path)
    exit()


# ============================================================
# LOAD DATASET
# ============================================================

try:
    df = pd.read_csv(file_path, encoding="utf-8")

except UnicodeDecodeError:
    print("UTF-8 encoding failed.")
    print("Trying Latin-1 encoding...")
    df = pd.read_csv(file_path, encoding="latin1")


# ============================================================
# DATASET CHECK
# ============================================================

print("\n" + "=" * 60)
print("SUPERSTORE DATASET CHECK")
print("=" * 60)

print("\nDataset loaded successfully!")

print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# COLUMN NAMES
# ============================================================

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

for column in df.columns:
    print("-", column)


# ============================================================
# DATA TYPES
# ============================================================

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print(df.dtypes)


# ============================================================
# MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())


# ============================================================
# DUPLICATE ROWS
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

print("Duplicate rows:", df.duplicated().sum())


# ============================================================
# FIRST 5 RECORDS
# ============================================================

print("\n" + "=" * 60)
print("FIRST 5 RECORDS")
print("=" * 60)

print(df.head())


# ============================================================
# BASIC STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("BASIC STATISTICS")
print("=" * 60)

print(df.describe(include="all"))


# ============================================================
# DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

df.info()


# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("DATASET CHECK COMPLETED SUCCESSFULLY")
print("=" * 60)