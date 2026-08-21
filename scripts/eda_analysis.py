import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore[reportMissingModuleSource]
import os

# ============================================================
# SUPERSTORE EXPLORATORY DATA ANALYSIS
# ============================================================

print("=" * 70)
print("SUPERSTORE EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# ============================================================
# 1. FILE PATHS
# ============================================================

input_file = "data/processed/superstore_cleaned.csv"
output_dir = "reports/eda"

os.makedirs(output_dir, exist_ok=True)


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")

print("\nRows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# 3. CONVERT DATE COLUMNS
# ============================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    errors="coerce"
)


# ============================================================
# 4. BASIC BUSINESS METRICS
# ============================================================

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

total_quantity = df["Quantity"].sum()

total_orders = df["Order ID"].nunique()

total_customers = df["Customer ID"].nunique()

average_order_value = (
    total_sales / total_orders
)


print("\n" + "=" * 70)
print("KEY BUSINESS METRICS")
print("=" * 70)

print("\nTotal Sales:", round(total_sales, 2))

print("Total Profit:", round(total_profit, 2))

print("Total Quantity Sold:", total_quantity)

print("Total Orders:", total_orders)

print("Total Customers:", total_customers)

print(
    "Average Order Value:",
    round(average_order_value, 2)
)


# ============================================================
# 5. SALES BY CATEGORY
# ============================================================

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("SALES BY CATEGORY")
print("=" * 70)

print(category_sales)


plt.figure(figsize=(10, 6))

category_sales.plot(
    kind="bar"
)

plt.title("Sales by Category")

plt.xlabel("Category")

plt.ylabel("Sales")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_by_category.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. PROFIT BY CATEGORY
# ============================================================

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("PROFIT BY CATEGORY")
print("=" * 70)

print(category_profit)


plt.figure(figsize=(10, 6))

category_profit.plot(
    kind="bar"
)

plt.title("Profit by Category")

plt.xlabel("Category")

plt.ylabel("Profit")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/profit_by_category.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. SALES BY REGION
# ============================================================

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("SALES BY REGION")
print("=" * 70)

print(region_sales)


plt.figure(figsize=(10, 6))

region_sales.plot(
    kind="bar"
)

plt.title("Sales by Region")

plt.xlabel("Region")

plt.ylabel("Sales")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_by_region.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. PROFIT BY REGION
# ============================================================

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("PROFIT BY REGION")
print("=" * 70)

print(region_profit)


plt.figure(figsize=(10, 6))

region_profit.plot(
    kind="bar"
)

plt.title("Profit by Region")

plt.xlabel("Region")

plt.ylabel("Profit")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/profit_by_region.png",
    dpi=300
)

plt.close()


# ============================================================
# 9. SALES BY CUSTOMER SEGMENT
# ============================================================

segment_sales = (
    df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("SALES BY CUSTOMER SEGMENT")
print("=" * 70)

print(segment_sales)


plt.figure(figsize=(10, 6))

segment_sales.plot(
    kind="bar"
)

plt.title("Sales by Customer Segment")

plt.xlabel("Segment")

plt.ylabel("Sales")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_by_segment.png",
    dpi=300
)

plt.close()


# ============================================================
# 10. SALES BY SHIP MODE
# ============================================================

ship_mode_sales = (
    df.groupby("Ship Mode")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("SALES BY SHIP MODE")
print("=" * 70)

print(ship_mode_sales)


plt.figure(figsize=(10, 6))

ship_mode_sales.plot(
    kind="bar"
)

plt.title("Sales by Ship Mode")

plt.xlabel("Ship Mode")

plt.ylabel("Sales")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_by_ship_mode.png",
    dpi=300
)

plt.close()


# ============================================================
# 11. SALES TREND BY YEAR
# ============================================================

year_sales = (
    df.groupby("Order Year")["Sales"]
    .sum()
)

print("\n" + "=" * 70)
print("SALES BY YEAR")
print("=" * 70)

print(year_sales)


plt.figure(figsize=(10, 6))

year_sales.plot(
    kind="line",
    marker="o"
)

plt.title("Sales Trend by Year")

plt.xlabel("Year")

plt.ylabel("Sales")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_trend_year.png",
    dpi=300
)

plt.close()


# ============================================================
# 12. PROFIT TREND BY YEAR
# ============================================================

year_profit = (
    df.groupby("Order Year")["Profit"]
    .sum()
)

print("\n" + "=" * 70)
print("PROFIT BY YEAR")
print("=" * 70)

print(year_profit)


plt.figure(figsize=(10, 6))

year_profit.plot(
    kind="line",
    marker="o"
)

plt.title("Profit Trend by Year")

plt.xlabel("Year")

plt.ylabel("Profit")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/profit_trend_year.png",
    dpi=300
)

plt.close()


# ============================================================
# 13. MONTHLY SALES TREND
# ============================================================

monthly_sales = (
    df.groupby("Order Month")["Sales"]
    .sum()
)

print("\n" + "=" * 70)
print("MONTHLY SALES")
print("=" * 70)

print(monthly_sales)


plt.figure(figsize=(12, 6))

monthly_sales.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Sales Trend")

plt.xlabel("Month")

plt.ylabel("Sales")

plt.xticks(range(1, 13))

plt.grid(True)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/monthly_sales_trend.png",
    dpi=300
)

plt.close()


# ============================================================
# 14. SALES BY SUB-CATEGORY
# ============================================================

subcategory_sales = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("SALES BY SUB-CATEGORY")
print("=" * 70)

print(subcategory_sales)


plt.figure(figsize=(12, 7))

subcategory_sales.plot(
    kind="bar"
)

plt.title("Sales by Sub-Category")

plt.xlabel("Sub-Category")

plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_by_subcategory.png",
    dpi=300
)

plt.close()


# ============================================================
# 15. PROFIT BY SUB-CATEGORY
# ============================================================

subcategory_profit = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n" + "=" * 70)
print("PROFIT BY SUB-CATEGORY")
print("=" * 70)

print(subcategory_profit)


plt.figure(figsize=(12, 7))

subcategory_profit.plot(
    kind="bar"
)

plt.title("Profit by Sub-Category")

plt.xlabel("Sub-Category")

plt.ylabel("Profit")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    f"{output_dir}/profit_by_subcategory.png",
    dpi=300
)

plt.close()


# ============================================================
# 16. TOP 10 PRODUCTS BY SALES
# ============================================================

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY SALES")
print("=" * 70)

print(top_products)


plt.figure(figsize=(12, 7))

top_products.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Products by Sales")

plt.xlabel("Sales")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/top_10_products_sales.png",
    dpi=300
)

plt.close()


# ============================================================
# 17. TOP 10 PRODUCTS BY PROFIT
# ============================================================

top_profit_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY PROFIT")
print("=" * 70)

print(top_profit_products)


plt.figure(figsize=(12, 7))

top_profit_products.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Products by Profit")

plt.xlabel("Profit")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/top_10_products_profit.png",
    dpi=300
)

plt.close()


# ============================================================
# 18. LOSS-MAKING SUB-CATEGORIES
# ============================================================

loss_subcategories = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values()
)

loss_subcategories = loss_subcategories[
    loss_subcategories < 0
]

print("\n" + "=" * 70)
print("LOSS-MAKING SUB-CATEGORIES")
print("=" * 70)

print(loss_subcategories)


# ============================================================
# 19. DISCOUNT VS PROFIT
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(df["Discount"], df["Profit"], alpha=0.6)

plt.title("Discount vs Profit")

plt.xlabel("Discount")

plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/discount_vs_profit.png",
    dpi=300
)

plt.close()


# ============================================================
# 20. SALES DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(df["Sales"].dropna(), bins=40)

plt.title("Sales Distribution")

plt.xlabel("Sales")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/sales_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 21. PROFIT DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(df["Profit"].dropna(), bins=40)

plt.title("Profit Distribution")

plt.xlabel("Profit")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/profit_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 22. CORRELATION HEATMAP
# ============================================================

numeric_data = df[
    [
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "Shipping Days",
        "Profit Margin"
    ]
]

correlation = numeric_data.corr()

plt.figure(figsize=(10, 7))

plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Correlation")
plt.xticks(range(len(correlation.columns)), correlation.columns, rotation=45, ha="right")
plt.yticks(range(len(correlation.index)), correlation.index)
for row in range(len(correlation.index)):
    for col in range(len(correlation.columns)):
        plt.text(col, row, f"{correlation.iloc[row, col]:.2f}",
                 ha="center", va="center")

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    f"{output_dir}/correlation_heatmap.png",
    dpi=300
)

plt.close()


# ============================================================
# 23. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nCharts saved in:")

print(output_dir)

print("\nGenerated charts:")

print("- sales_by_category.png")
print("- profit_by_category.png")
print("- sales_by_region.png")
print("- profit_by_region.png")
print("- sales_by_segment.png")
print("- sales_by_ship_mode.png")
print("- sales_trend_year.png")
print("- profit_trend_year.png")
print("- monthly_sales_trend.png")
print("- sales_by_subcategory.png")
print("- profit_by_subcategory.png")
print("- top_10_products_sales.png")
print("- top_10_products_profit.png")
print("- discount_vs_profit.png")
print("- sales_distribution.png")
print("- profit_distribution.png")
print("- correlation_heatmap.png")

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)