# ============================================================
# SUPERSTORE EXECUTIVE INTELLIGENCE DASHBOARD
# ApexPlanet Data Analytics Internship
# Professional Dark Executive Dashboard
# ============================================================

import io
import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Superstore Executive Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PROFESSIONAL DARK THEME
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(45, 75, 160, 0.16), transparent 25%),
                radial-gradient(circle at 90% 15%, rgba(120, 50, 180, 0.13), transparent 25%),
                #070b13;
            color: #f4f7ff;
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        [data-testid="stToolbar"] {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1550px;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(
                145deg,
                rgba(20,29,48,0.96),
                rgba(10,17,30,0.96)
            );
            border: 1px solid rgba(100,130,180,0.20);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        }

        div[data-testid="stMetric"] label {
            color: #aab6ce !important;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
        }

        div[data-testid="stMetricDelta"] {
            color: #63e6a7 !important;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 22px;
            margin-bottom: 12px;
            color: #f5f7ff;
        }

        .small-label {
            color: #8f9bb3;
            font-size: 0.82rem;
        }

        .hero-caption {
            color: #aeb9cf;
            font-size: 0.98rem;
        }

        div[data-baseweb="select"] > div {
            background: #111827;
            border: 1px solid #293750;
            border-radius: 10px;
        }

        div[data-baseweb="select"] span {
            color: #f5f7ff !important;
        }

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #33425e;
            background: #121c2e;
            color: white;
            font-weight: 600;
        }

        .stButton > button:hover {
            border-color: #6d7cff;
            color: white;
        }

        .stDownloadButton > button {
            border-radius: 10px;
            background: #24335c;
            border: 1px solid #425a9b;
            color: white;
            font-weight: 600;
        }

        div[data-testid="stExpander"] {
            background: #0d1422;
            border: 1px solid #243149;
            border-radius: 14px;
        }

        .insight-card {
            background: linear-gradient(
                145deg,
                rgba(20,30,50,0.95),
                rgba(11,17,30,0.95)
            );
            border: 1px solid rgba(100,130,180,0.18);
            border-radius: 16px;
            padding: 18px;
            min-height: 130px;
        }

        .insight-title {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 8px;
        }

        .insight-text {
            color: #aeb9cf;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA PATH
# ============================================================

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "processed",
    "superstore_cleaned.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    # --------------------------------------------------------
    # Date conversion
    # --------------------------------------------------------

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Create year if missing
    # --------------------------------------------------------

    if "Order Year" not in df.columns and "Order Date" in df.columns:
        df["Order Year"] = df["Order Date"].dt.year

    # --------------------------------------------------------
    # Create month number if missing
    # --------------------------------------------------------

    if "Order Month" not in df.columns and "Order Date" in df.columns:
        df["Order Month"] = df["Order Date"].dt.month

    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


# ============================================================
# LOAD DATA SAFELY
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error("Unable to load the Superstore dataset.")

    st.code(str(e))

    st.stop()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):

    if pd.isna(value):
        return "$0"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"

    return f"${value:,.0f}"


def percentage(value):

    if pd.isna(value):
        return "0.0%"

    return f"{value:.2f}%"


def make_hero_image():

    width = 1450
    height = 300

    img = Image.new(
        "RGB",
        (width, height),
        (8, 14, 28)
    )

    draw = ImageDraw.Draw(img)

    # --------------------------------------------------------
    # Background gradient
    # --------------------------------------------------------

    for x in range(width):

        ratio = x / width

        r = int(8 + ratio * 20)
        g = int(14 + ratio * 10)
        b = int(28 + ratio * 45)

        draw.line(
            [(x, 0), (x, height)],
            fill=(r, g, b)
        )

    # --------------------------------------------------------
    # Decorative circles
    # --------------------------------------------------------

    circles = [
        (1180, 70, 70),
        (1270, 150, 42),
        (1080, 170, 35),
        (1340, 70, 24),
        (1030, 65, 18)
    ]

    for cx, cy, radius in circles:

        draw.ellipse(
            (
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius
            ),
            outline=(75, 110, 220),
            width=3
        )

    # --------------------------------------------------------
    # Shopping cart
    # --------------------------------------------------------

    cart_x = 1050
    cart_y = 105

    draw.line(
        [
            (cart_x, cart_y),
            (cart_x + 45, cart_y)
        ],
        fill=(80, 180, 255),
        width=7
    )

    draw.line(
        [
            (cart_x + 45, cart_y),
            (cart_x + 75, cart_y + 90)
        ],
        fill=(80, 180, 255),
        width=7
    )

    draw.line(
        [
            (cart_x + 75, cart_y + 90),
            (cart_x + 230, cart_y + 90)
        ],
        fill=(80, 180, 255),
        width=7
    )

    draw.line(
        [
            (cart_x + 55, cart_y + 25),
            (cart_x + 210, cart_y + 25)
        ],
        fill=(130, 90, 255),
        width=6
    )

    draw.line(
        [
            (cart_x + 210, cart_y + 25),
            (cart_x + 230, cart_y + 90)
        ],
        fill=(130, 90, 255),
        width=6
    )

    # wheels

    draw.ellipse(
        (
            cart_x + 85,
            cart_y + 105,
            cart_x + 115,
            cart_y + 135
        ),
        fill=(230, 235, 255)
    )

    draw.ellipse(
        (
            cart_x + 190,
            cart_y + 105,
            cart_x + 220,
            cart_y + 135
        ),
        fill=(230, 235, 255)
    )

    # --------------------------------------------------------
    # Product boxes
    # --------------------------------------------------------

    boxes = [
        (1190, 60, 1250, 110),
        (1260, 110, 1320, 160),
        (1100, 40, 1155, 95)
    ]

    for x1, y1, x2, y2 in boxes:

        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=8,
            outline=(130, 90, 255),
            width=4
        )

    # --------------------------------------------------------
    # Analytics chart
    # --------------------------------------------------------

    points = [
        (780, 215),
        (825, 190),
        (870, 205),
        (915, 145),
        (960, 165),
        (1000, 105)
    ]

    draw.line(
        points,
        fill=(80, 210, 150),
        width=6
    )

    for x, y in points:

        draw.ellipse(
            (
                x - 6,
                y - 6,
                x + 6,
                y + 6
            ),
            fill=(80, 210, 150)
        )

    # --------------------------------------------------------
    # Vertical bars
    # --------------------------------------------------------

    bars = [
        (720, 180, 740, 240),
        (750, 145, 770, 240),
        (780, 160, 800, 240),
        (810, 125, 830, 240)
    ]

    for x1, y1, x2, y2 in bars:

        draw.rounded_rectangle(
            (x1, y1, x2, y2),
            radius=5,
            fill=(65, 105, 220)
        )

    return img


# ============================================================
# HERO IMAGE
# ============================================================

hero_image = make_hero_image()

st.image(
    hero_image,
    width="stretch"
)


# ============================================================
# HERO TITLE
# ============================================================

title_col, button_col = st.columns(
    [5, 1]
)

with title_col:

    st.caption("SUPERSTORE • BUSINESS ANALYTICS")

    st.title("Executive Intelligence")

    st.markdown(
        "Sales  •  Profit  •  Customers  •  Products  •  Regional Performance"
    )


with button_col:

    st.write("")

    csv_buffer = io.BytesIO()

    df.to_csv(
        csv_buffer,
        index=False
    )

    st.download_button(
        label="📥 Download Data",
        data=csv_buffer.getvalue(),
        file_name="superstore_analysis.csv",
        mime="text/csv"
    )


# ============================================================
# FILTER AREA
# ============================================================

st.markdown(
    '<div class="section-title">🎛️ Quick Analysis</div>',
    unsafe_allow_html=True
)

filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(
    [1, 1, 1, 1, 0.8]
)


# ============================================================
# YEAR FILTER
# ============================================================

with filter_col1:

    if "Order Year" in df.columns:

        years = sorted(
            df["Order Year"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_year = st.selectbox(
            "📅 Year",
            ["All Years"] + years
        )

    else:

        selected_year = "All Years"


# ============================================================
# REGION FILTER
# ============================================================

with filter_col2:

    if "Region" in df.columns:

        regions = sorted(
            df["Region"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_region = st.selectbox(
            "🌎 Region",
            ["All Regions"] + regions
        )

    else:

        selected_region = "All Regions"


# ============================================================
# CATEGORY FILTER
# ============================================================

with filter_col3:

    if "Category" in df.columns:

        categories = sorted(
            df["Category"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "📦 Category",
            ["All Categories"] + categories
        )

    else:

        selected_category = "All Categories"


# ============================================================
# SEGMENT FILTER
# ============================================================

with filter_col4:

    if "Segment" in df.columns:

        segments = sorted(
            df["Segment"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_segment = st.selectbox(
            "👥 Segment",
            ["All Segments"] + segments
        )

    else:

        selected_segment = "All Segments"


# ============================================================
# RESET
# ============================================================

with filter_col5:

    st.write("")

    if st.button(
        "🔄 Reset",
        width="stretch"
    ):

        st.rerun()


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if (
    selected_year != "All Years"
    and "Order Year" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Order Year"] == selected_year
    ]


if (
    selected_region != "All Regions"
    and "Region" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if (
    selected_category != "All Categories"
    and "Category" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


if (
    selected_segment != "All Segments"
    and "Segment" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Segment"] == selected_segment
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = (
    filtered_df["Sales"].sum()
    if "Sales" in filtered_df.columns
    else 0
)

total_profit = (
    filtered_df["Profit"].sum()
    if "Profit" in filtered_df.columns
    else 0
)

total_quantity = (
    filtered_df["Quantity"].sum()
    if "Quantity" in filtered_df.columns
    else 0
)

if "Order ID" in filtered_df.columns:

    total_orders = filtered_df["Order ID"].nunique()

else:

    total_orders = len(filtered_df)


if "Customer ID" in filtered_df.columns:

    total_customers = filtered_df["Customer ID"].nunique()

else:

    total_customers = 0


if total_sales != 0:

    profit_margin = (
        total_profit / total_sales
    ) * 100

else:

    profit_margin = 0


if total_orders > 0:

    average_order_value = (
        total_sales / total_orders
    )

else:

    average_order_value = 0


# ============================================================
# BUSINESS PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">📊 Business Performance</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5, k6 = st.columns(6)


with k1:

    st.metric(
        "💰 Total Sales",
        money(total_sales)
    )


with k2:

    st.metric(
        "💵 Total Profit",
        money(total_profit)
    )


with k3:

    st.metric(
        "📦 Units Sold",
        f"{total_quantity:,.0f}"
    )


with k4:

    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,}"
    )


with k5:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


with k6:

    st.metric(
        "📈 Profit Margin",
        percentage(profit_margin)
    )


# ============================================================
# TREND SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📈 Performance Trends</div>',
    unsafe_allow_html=True
)

trend1, trend2 = st.columns(2)


# ============================================================
# SALES TREND
# ============================================================

with trend1:

    if "Order Date" in filtered_df.columns:

        sales_trend = (
            filtered_df
            .dropna(subset=["Order Date"])
            .set_index("Order Date")
            .resample("ME")["Sales"]
            .sum()
            .reset_index()
        )

        fig_sales = go.Figure()

        fig_sales.add_trace(
            go.Scatter(
                x=sales_trend["Order Date"],
                y=sales_trend["Sales"],
                mode="lines",
                line=dict(
                    width=3
                ),
                fill="tozeroy",
                name="Sales"
            )
        )

        fig_sales.update_layout(
            title="Sales Momentum",
            height=360,
            template="plotly_dark",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_sales,
            width="stretch"
        )


# ============================================================
# PROFIT TREND
# ============================================================

with trend2:

    if "Order Date" in filtered_df.columns:

        profit_trend = (
            filtered_df
            .dropna(subset=["Order Date"])
            .set_index("Order Date")
            .resample("ME")["Profit"]
            .sum()
            .reset_index()
        )

        fig_profit = go.Figure()

        fig_profit.add_trace(
            go.Scatter(
                x=profit_trend["Order Date"],
                y=profit_trend["Profit"],
                mode="lines",
                line=dict(
                    width=3
                ),
                fill="tozeroy",
                name="Profit"
            )
        )

        fig_profit.update_layout(
            title="Profit Momentum",
            height=360,
            template="plotly_dark",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_profit,
            width="stretch"
        )


# ============================================================
# REGIONAL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🌎 Regional Intelligence</div>',
    unsafe_allow_html=True
)

region_col1, region_col2 = st.columns(
    [1.6, 1]
)


# ============================================================
# STATE MAP
# ============================================================

with region_col1:

    if (
        "State" in filtered_df.columns
        and "Sales" in filtered_df.columns
    ):

        state_sales = (
            filtered_df
            .groupby("State")["Sales"]
            .sum()
            .reset_index()
        )

        state_map = {
            "Alabama": "AL",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC"
        }

        state_sales["Code"] = (
            state_sales["State"]
            .map(state_map)
        )

        state_sales = state_sales.dropna(
            subset=["Code"]
        )

        fig_map = px.choropleth(
            state_sales,
            locations="Code",
            locationmode="USA-states",
            color="Sales",
            scope="usa",
            hover_name="State",
            hover_data={
                "Code": False,
                "Sales": ":$,.0f"
            },
            title="Sales by State"
        )

        fig_map.update_layout(
            height=420,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=10,
                r=10,
                t=55,
                b=10
            )
        )

        st.plotly_chart(
            fig_map,
            width="stretch"
        )


# ============================================================
# REGION BAR
# ============================================================

with region_col2:

    if (
        "Region" in filtered_df.columns
        and "Sales" in filtered_df.columns
    ):

        region_sales = (
            filtered_df
            .groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values(
                "Sales",
                ascending=True
            )
        )

        fig_region = px.bar(
            region_sales,
            x="Sales",
            y="Region",
            orientation="h",
            text_auto=".2s",
            title="Regional Sales"
        )

        fig_region.update_layout(
            height=420,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )

        st.plotly_chart(
            fig_region,
            width="stretch"
        )


# ============================================================
# CATEGORY + SEGMENT
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Customer & Product Mix</div>',
    unsafe_allow_html=True
)

mix1, mix2 = st.columns(2)


# ============================================================
# CATEGORY
# ============================================================

with mix1:

    if (
        "Category" in filtered_df.columns
        and "Sales" in filtered_df.columns
    ):

        category_sales = (
            filtered_df
            .groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig_category = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.62,
            title="Sales by Category"
        )

        fig_category.update_layout(
            height=400,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_category,
            width="stretch"
        )


# ============================================================
# SEGMENT
# ============================================================

with mix2:

    if (
        "Segment" in filtered_df.columns
        and "Sales" in filtered_df.columns
    ):

        segment_sales = (
            filtered_df
            .groupby("Segment")["Sales"]
            .sum()
            .reset_index()
        )

        fig_segment = px.pie(
            segment_sales,
            names="Segment",
            values="Sales",
            hole=0.62,
            title="Sales by Customer Segment"
        )

        fig_segment.update_layout(
            height=400,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_segment,
            width="stretch"
        )


# ============================================================
# TOP PRODUCTS + RISK MONITOR
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Products & Risk Intelligence</div>',
    unsafe_allow_html=True
)

product_col, risk_col = st.columns(
    [1.7, 1]
)


# ============================================================
# TOP PRODUCTS
# ============================================================

with product_col:

    if (
        "Product Name" in filtered_df.columns
        and "Sales" in filtered_df.columns
    ):

        top_products = (
            filtered_df
            .groupby("Product Name")["Sales"]
            .sum()
            .reset_index()
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(8)
        )

        top_products = top_products.sort_values(
            "Sales",
            ascending=True
        )

        fig_products = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h",
            text_auto=".2s",
            title="Top Products by Sales"
        )

        fig_products.update_layout(
            height=440,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20
            )
        )

        st.plotly_chart(
            fig_products,
            width="stretch"
        )


# ============================================================
# RISK MONITOR
# ============================================================

with risk_col:

    st.markdown("### ⚠️ Risk Monitor")

    # --------------------------------------------------------
    # Worst category
    # --------------------------------------------------------

    if (
        "Category" in filtered_df.columns
        and "Profit" in filtered_df.columns
    ):

        category_profit = (
            filtered_df
            .groupby("Category")["Profit"]
            .sum()
        )

        worst_category = category_profit.idxmin()
        worst_category_profit = category_profit.min()

        if worst_category_profit < 0:

            st.error(
                f"Loss Category\n\n"
                f"**{worst_category}**\n\n"
                f"{money(worst_category_profit)}"
            )

    # --------------------------------------------------------
    # Worst sub-category
    # --------------------------------------------------------

    if (
        "Sub-Category" in filtered_df.columns
        and "Profit" in filtered_df.columns
    ):

        sub_profit = (
            filtered_df
            .groupby("Sub-Category")["Profit"]
            .sum()
        )

        worst_sub = sub_profit.idxmin()
        worst_sub_profit = sub_profit.min()

        if worst_sub_profit < 0:

            st.warning(
                f"Loss Sub-Category\n\n"
                f"**{worst_sub}**\n\n"
                f"{money(worst_sub_profit)}"
            )

    # --------------------------------------------------------
    # Worst product
    # --------------------------------------------------------

    if (
        "Product Name" in filtered_df.columns
        and "Profit" in filtered_df.columns
    ):

        product_profit = (
            filtered_df
            .groupby("Product Name")["Profit"]
            .sum()
        )

        worst_product = product_profit.idxmin()
        worst_product_profit = product_profit.min()

        if worst_product_profit < 0:

            st.info(
                f"Product Under Watch\n\n"
                f"**{worst_product}**\n\n"
                f"{money(worst_product_profit)}"
            )


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Executive Insights</div>',
    unsafe_allow_html=True
)

insight1, insight2, insight3, insight4 = st.columns(4)


# ============================================================
# INSIGHT 1
# ============================================================

with insight1:

    if "Category" in filtered_df.columns:

        cat_sales = (
            filtered_df
            .groupby("Category")["Sales"]
            .sum()
        )

        if len(cat_sales) > 0:

            best_cat = cat_sales.idxmax()

            share = (
                cat_sales.max()
                / cat_sales.sum()
                * 100
            )

            st.info(
                f"📦 **Category Leader**\n\n"
                f"{best_cat} leads sales with "
                f"{share:.1f}% of total revenue."
            )


# ============================================================
# INSIGHT 2
# ============================================================

with insight2:

    if "Region" in filtered_df.columns:

        reg_sales = (
            filtered_df
            .groupby("Region")["Sales"]
            .sum()
        )

        if len(reg_sales) > 0:

            best_reg = reg_sales.idxmax()

            st.success(
                f"🌎 **Regional Leader**\n\n"
                f"{best_reg} is the strongest "
                f"sales-performing region."
            )


# ============================================================
# INSIGHT 3
# ============================================================

with insight3:

    if "Segment" in filtered_df.columns:

        seg_sales = (
            filtered_df
            .groupby("Segment")["Sales"]
            .sum()
        )

        if len(seg_sales) > 0:

            best_segment = seg_sales.idxmax()

            st.warning(
                f"👥 **Customer Leader**\n\n"
                f"{best_segment} generates the "
                f"highest customer-segment revenue."
            )


# ============================================================
# INSIGHT 4
# ============================================================

with insight4:

    if total_sales > 0:

        st.success(
            f"📈 **Profitability**\n\n"
            f"Current profit margin is "
            f"{profit_margin:.2f}%."
        )


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">🗂️ Data Explorer</div>',
    unsafe_allow_html=True
)

show_data = st.toggle(
    "Show filtered raw data",
    value=False
)


if show_data:

    st.write(
        f"Showing {len(filtered_df):,} filtered records."
    )

    st.dataframe(
        filtered_df,
        width="stretch",
        height=480
    )

    filtered_csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "📥 Download Filtered Data",
        data=filtered_csv,
        file_name="filtered_superstore_data.csv",
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Superstore Executive Intelligence • "
    "ApexPlanet Data Analytics Internship • "
    f"{len(filtered_df):,} records analyzed"
)