
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Shopease Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>

/* Main application */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Main title */
h1 {
    font-weight: 800 !important;
    letter-spacing: -1px;
}

/* Section headings */
h2 {
    font-weight: 750 !important;
    margin-top: 1.5rem !important;
}

h3 {
    font-weight: 650 !important;
}

/* KPI metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.055),
        rgba(255,255,255,0.025)
    );
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 20px;
    min-height: 115px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.12);
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    font-size: 0.90rem !important;
    font-weight: 600 !important;
}

/* KPI values */
[data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 750 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar headings */
section[data-testid="stSidebar"] h2 {
    font-size: 1.15rem !important;
}

/* Alerts / information boxes */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Dividers */
hr {
    margin: 1.8rem 0 !important;
    opacity: 0.25;
}

/* Plotly charts */
div[data-testid="stPlotlyChart"] {
    border-radius: 12px;
}

/* Multiselect boxes */
div[data-baseweb="select"] > div {
    border-radius: 9px;
}

/* Footer */
.dashboard-footer {
    text-align: center;
    padding: 25px 0 10px 0;
    margin-top: 30px;
    border-top: 1px solid rgba(255,255,255,0.10);
    color: rgba(255,255,255,0.55);
    font-size: 0.82rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("shopease_clean_9991.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["DeliveryDate"] = pd.to_datetime(df["DeliveryDate"], errors="coerce")

# ============================================================
# HEADER
# ============================================================

st.title("📊 Shopease Analytics Dashboard")

st.markdown(
    """
    **Interactive Business Intelligence Dashboard**
    Sales • Products • Customers • Payments • Operations
    """
)

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

valid_dates = df["OrderDate"].dropna()

if len(valid_dates) > 0:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.sidebar.date_input(
        "📅 Order Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:
    date_range = None


city_options = sorted(df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "🏙️ City",
    city_options,
    default=city_options
)


category_options = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "📦 Category",
    category_options,
    default=category_options
)


gender_options = sorted(df["Gender"].dropna().unique())

selected_genders = st.sidebar.multiselect(
    "👥 Gender",
    gender_options,
    default=gender_options
)


payment_options = sorted(df["PaymentMethod"].dropna().unique())

selected_payments = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_options,
    default=payment_options
)


status_options = sorted(df["OrderStatus"].dropna().unique())

selected_statuses = st.sidebar.multiselect(
    "📌 Order Status",
    status_options,
    default=status_options
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if date_range is not None and len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["OrderDate"].dt.date.between(
            start_date,
            end_date
        )
    ]

filtered_df = filtered_df[
    filtered_df["City"].isin(selected_cities)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_categories)
]

filtered_df = filtered_df[
    filtered_df["Gender"].isin(selected_genders)
]

filtered_df = filtered_df[
    filtered_df["PaymentMethod"].isin(selected_payments)
]

filtered_df = filtered_df[
    filtered_df["OrderStatus"].isin(selected_statuses)
]

# ============================================================
# FILTER STATUS
# ============================================================

st.info(
    f"Showing **{len(filtered_df):,} orders** "
    f"from **{len(df):,} total orders**."
)


# ============================================================
# EXECUTIVE KPI CARDS
# ============================================================

total_sales = filtered_df["TotalAmount"].sum()
total_orders = len(filtered_df)

aov = (
    filtered_df["TotalAmount"].mean()
    if total_orders > 0
    else 0
)

delivered_rate = (
    (filtered_df["OrderStatus"].eq("Delivered").mean() * 100)
    if total_orders > 0
    else 0
)

avg_rating = filtered_df["Rating"].mean()

avg_delivery = filtered_df["DeliveryDays"].mean()

unique_customers = filtered_df["CustomerID"].nunique()

st.subheader("Executive Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.0f}"
    )

with k2:
    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,}"
    )

with k3:
    st.metric(
        "🛒 Average Order Value",
        f"₹{aov:,.0f}"
    )

with k4:
    st.metric(
        "🚚 Delivered Rate",
        f"{delivered_rate:.1f}%"
    )

k5, k6, k7 = st.columns(3)

with k5:
    st.metric(
        "⭐ Average Rating",
        f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A"
    )

with k6:
    st.metric(
        "⏱️ Avg Delivery",
        f"{avg_delivery:.2f} days"
        if pd.notna(avg_delivery)
        else "N/A"
    )

with k7:
    st.metric(
        "👥 Unique Customers",
        f"{unique_customers:,}"
    )

st.divider()


# ============================================================
# SALES PERFORMANCE
# ============================================================

st.subheader("📈 Sales Performance")

# Monthly sales
monthly_sales = (
    filtered_df
    .dropna(subset=["OrderDate"])
    .assign(
        Month=lambda x: x["OrderDate"].dt.to_period("M").astype(str)
    )
    .groupby("Month")
    .agg(
        Sales=("TotalAmount", "sum"),
        Orders=("OrderID", "count")
    )
    .reset_index()
)

# Category sales
category_sales = (
    filtered_df
    .groupby("Category")
    .agg(
        Sales=("TotalAmount", "sum"),
        Orders=("OrderID", "count")
    )
    .reset_index()
    .sort_values("Sales", ascending=True)
)

col1, col2 = st.columns([1.6, 1])

with col1:

    st.markdown("**Monthly Revenue Trend**")

    if not monthly_sales.empty:

        fig_month = px.line(
            monthly_sales,
            x="Month",
            y="Sales",
            markers=True,
            labels={
                "Month": "",
                "Sales": "Revenue"
            }
        )

        fig_month.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )

        fig_month.update_layout(
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            hovermode="x unified",
            yaxis=dict(
                tickformat=",.0f",
                rangemode="tozero"
            ),
            xaxis=dict(
                type="category"
            )
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )

    else:
        st.warning("No dated orders available.")

with col2:

    st.markdown("**Revenue by Category**")

    if not category_sales.empty:

        fig_category = px.bar(
            category_sales,
            x="Sales",
            y="Category",
            orientation="h",
            text="Sales",
            labels={
                "Sales": "Revenue",
                "Category": ""
            }
        )

        fig_category.update_traces(
            texttemplate="₹%{x:,.0f}",
            textposition="outside"
        )

        fig_category.update_layout(
            height=380,
            margin=dict(l=10, r=30, t=20, b=10),
            xaxis=dict(
                tickformat=",.0f",
                rangemode="tozero"
            ),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    else:
        st.warning("No category data available.")


st.divider()




# ============================================================
# PRODUCT INTELLIGENCE
# ============================================================

st.subheader("📦 Product Intelligence")

product_summary = (
    filtered_df
    .groupby("Product")
    .agg(
        Orders=("OrderID", "count"),
        Sales=("TotalAmount", "sum"),
        Quantity=("Quantity", "sum"),
        AOV=("TotalAmount", "mean"),
        Avg_Rating=("Rating", "mean")
    )
    .reset_index()
)

# ------------------------------------------------------------
# Top 10 Products by Revenue
# ------------------------------------------------------------

top_products = (
    product_summary
    .sort_values("Sales", ascending=False)
    .head(10)
    .sort_values("Sales", ascending=True)
)

# ------------------------------------------------------------
# Product Value vs Rating
# ------------------------------------------------------------

product_positioning = product_summary.dropna(
    subset=["Avg_Rating"]
).copy()

col1, col2 = st.columns([1.15, 1])

with col1:

    st.markdown("**Top 10 Products by Revenue**")

    if not top_products.empty:

        fig_products = px.bar(
            top_products,
            x="Sales",
            y="Product",
            orientation="h",
            text="Sales",
            hover_data=[
                "Orders",
                "Quantity",
                "AOV",
                "Avg_Rating"
            ],
            labels={
                "Sales": "Revenue",
                "Product": ""
            }
        )

        fig_products.update_traces(
            texttemplate="₹%{x:,.0f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_products.update_layout(
            height=500,
            margin=dict(l=10, r=110, t=20, b=10),
            xaxis=dict(
                tickformat=",.0f",
                rangemode="tozero"
            ),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    else:
        st.warning("No product data available.")

with col2:

    st.markdown("**Product Value vs Customer Rating**")

    if not product_positioning.empty:

        fig_positioning = px.scatter(
            product_positioning,
            x="AOV",
            y="Avg_Rating",
            size="Sales",
            hover_name="Product",
            hover_data=[
                "Orders",
                "Sales",
                "Quantity"
            ],
            labels={
                "AOV": "Average Order Value",
                "Avg_Rating": "Average Rating"
            }
        )

        fig_positioning.update_layout(
            height=500,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(
                tickformat=",.0f",
                rangemode="tozero"
            ),
            yaxis=dict(
                range=[3.5, 4.3],
                dtick=0.1
            )
        )

        st.plotly_chart(
            fig_positioning,
            use_container_width=True
        )

    else:
        st.warning("No rated products available.")

st.divider()


# ============================================================
# CUSTOMER & PAYMENT ANALYTICS
# ============================================================

st.subheader("👥 Customer & Payment Analytics")

# ------------------------------------------------------------
# Customer Age Distribution
# ------------------------------------------------------------

age_data = filtered_df.dropna(subset=["CustomerAge"]).copy()

# Gender revenue
gender_sales = (
    filtered_df
    .groupby("Gender")
    .agg(
        Sales=("TotalAmount", "sum"),
        Orders=("OrderID", "count"),
        AOV=("TotalAmount", "mean")
    )
    .reset_index()
)

# Payment performance
payment_sales = (
    filtered_df
    .groupby("PaymentMethod", dropna=False)
    .agg(
        Sales=("TotalAmount", "sum"),
        Orders=("OrderID", "count"),
        AOV=("TotalAmount", "mean")
    )
    .reset_index()
)

payment_sales["PaymentMethod"] = payment_sales["PaymentMethod"].fillna(
    "Missing"
)

col1, col2 = st.columns([1.15, 1])

with col1:

    st.markdown("**Customer Age Distribution**")

    if not age_data.empty:

        fig_age = px.histogram(
            age_data,
            x="CustomerAge",
            nbins=20,
            labels={
                "CustomerAge": "Customer Age",
                "count": "Orders"
            }
        )

        fig_age.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(
                dtick=5
            ),
            yaxis=dict(
                rangemode="tozero"
            )
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

    else:
        st.warning("No customer age data available.")

with col2:

    st.markdown("**Revenue by Gender**")

    if not gender_sales.empty:

        fig_gender = px.bar(
            gender_sales,
            x="Gender",
            y="Sales",
            text="Sales",
            hover_data=[
                "Orders",
                "AOV"
            ],
            labels={
                "Gender": "",
                "Sales": "Revenue"
            }
        )

        fig_gender.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_gender.update_layout(
            height=400,
            margin=dict(l=10, r=30, t=20, b=10),
            yaxis=dict(
                tickformat=",.0f",
                rangemode="tozero"
            )
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )

    else:
        st.warning("No gender data available.")

# ------------------------------------------------------------
# Payment Method Performance
# ------------------------------------------------------------

st.markdown("**Payment Method Performance**")

if not payment_sales.empty:

    fig_payment = px.bar(
        payment_sales.sort_values("Sales"),
        x="Sales",
        y="PaymentMethod",
        orientation="h",
        text="Sales",
        hover_data=[
            "Orders",
            "AOV"
        ],
        labels={
            "Sales": "Revenue",
            "PaymentMethod": ""
        }
    )

    fig_payment.update_traces(
        texttemplate="₹%{x:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig_payment.update_layout(
        height=350,
        margin=dict(l=10, r=110, t=20, b=10),
        xaxis=dict(
            tickformat=",.0f",
            rangemode="tozero"
        ),
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

else:
    st.warning("No payment data available.")

st.divider()


# ============================================================
# OPERATIONS & DELIVERY ANALYTICS
# ============================================================

st.subheader("🚚 Operations & Delivery Analytics")

# ------------------------------------------------------------
# Order Status
# ------------------------------------------------------------

status_summary = (
    filtered_df
    .groupby("OrderStatus")
    .agg(
        Orders=("OrderID", "count"),
        Sales=("TotalAmount", "sum")
    )
    .reset_index()
)

# ------------------------------------------------------------
# Delivery by City
# ------------------------------------------------------------

delivery_city = (
    filtered_df
    .dropna(subset=["DeliveryDays"])
    .groupby("City")
    .agg(
        Delivered_Orders=("OrderID", "count"),
        Avg_Delivery_Days=("DeliveryDays", "mean"),
        Median_Delivery_Days=("DeliveryDays", "median")
    )
    .reset_index()
    .sort_values("Avg_Delivery_Days", ascending=True)
)

# ------------------------------------------------------------
# Delivery by Category
# ------------------------------------------------------------

delivery_category = (
    filtered_df
    .dropna(subset=["DeliveryDays"])
    .groupby("Category")
    .agg(
        Delivered_Orders=("OrderID", "count"),
        Avg_Delivery_Days=("DeliveryDays", "mean")
    )
    .reset_index()
    .sort_values("Avg_Delivery_Days", ascending=True)
)

col1, col2 = st.columns([1, 1.3])

# ------------------------------------------------------------
# Order Status Donut
# ------------------------------------------------------------

with col1:

    st.markdown("**Order Status Distribution**")

    if not status_summary.empty:

        fig_status = px.pie(
            status_summary,
            names="OrderStatus",
            values="Orders",
            hole=0.55,
            hover_data=["Sales"]
        )

        fig_status.update_traces(
            textinfo="percent+label",
            textposition="outside"
        )

        fig_status.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    else:
        st.warning("No order-status data available.")

# ------------------------------------------------------------
# Delivery by City
# ------------------------------------------------------------

with col2:

    st.markdown("**Average Delivery Time by City**")

    if not delivery_city.empty:

        fig_delivery_city = px.bar(
            delivery_city,
            x="Avg_Delivery_Days",
            y="City",
            orientation="h",
            text="Avg_Delivery_Days",
            hover_data=[
                "Delivered_Orders",
                "Median_Delivery_Days"
            ],
            labels={
                "Avg_Delivery_Days": "Average Delivery (Days)",
                "City": ""
            }
        )

        fig_delivery_city.update_traces(
            texttemplate="%{x:.2f} days",
            textposition="outside",
            cliponaxis=False
        )

        fig_delivery_city.update_layout(
            height=400,
            margin=dict(l=10, r=90, t=20, b=10),
            xaxis=dict(
                rangemode="tozero",
                dtick=0.5
            ),
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_delivery_city,
            use_container_width=True
        )

    else:
        st.warning("No delivery-time data available.")

# ------------------------------------------------------------
# Delivery by Category
# ------------------------------------------------------------

st.markdown("**Average Delivery Time by Category**")

if not delivery_category.empty:

    fig_delivery_category = px.bar(
        delivery_category,
        x="Category",
        y="Avg_Delivery_Days",
        text="Avg_Delivery_Days",
        hover_data=["Delivered_Orders"],
        labels={
            "Category": "",
            "Avg_Delivery_Days": "Average Delivery (Days)"
        }
    )

    fig_delivery_category.update_traces(
        texttemplate="%{y:.2f} days",
        textposition="outside",
        cliponaxis=False
    )

    fig_delivery_category.update_layout(
        height=350,
        margin=dict(l=10, r=30, t=20, b=10),
        yaxis=dict(
            rangemode="tozero",
            dtick=0.5
        )
    )

    st.plotly_chart(
        fig_delivery_category,
        use_container_width=True
    )

else:
    st.warning("No delivery-time data available.")

st.divider()


# ============================================================
# ANALYTICAL INSIGHTS
# ============================================================

st.subheader("🧠 Analytical Insights")

st.caption(
    "Key findings derived from the descriptive, inferential and "
    "predictive analyses performed on the Shopease dataset."
)

# ------------------------------------------------------------
# Insight Cards
# ------------------------------------------------------------

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(
        """
        **💰 Revenue Concentration**

        Electronics generated approximately **51.7% of total
        revenue**, substantially exceeding the other product
        categories.
        """
    )

with i2:
    st.markdown(
        """
        **📦 Order Value Drivers**

        Unit Price and Quantity show positive relationships with
        Total Amount, with Spearman correlations of approximately
        **0.75** and **0.61**, respectively.
        """
    )

with i3:
    st.markdown(
        """
        **🚚 Delivery Stability**

        Average delivery time remained close to **3.5 days**
        across cities and categories, indicating relatively
        consistent delivery performance.
        """
    )

st.divider()

# ------------------------------------------------------------
# Statistical Findings
# ------------------------------------------------------------

st.markdown("### 📊 Statistical Findings")

stat1, stat2 = st.columns(2)

with stat1:

    st.markdown(
        """
        **Category Revenue Differences**

        • One-way ANOVA: **F = 378.21, p < 0.001**
        • Revenue differs significantly across categories.
        • Electronics was significantly different from the other
          categories in Tukey pairwise comparisons.
        """
    )

    st.markdown(
        """
        **Gender Revenue Comparison**

        • Independent-samples t-test: **p = 0.677**
        • Mann–Whitney U test: **p = 0.642**
        • No statistically significant difference was detected
          between male and female order values.
        """
    )

with stat2:

    st.markdown(
        """
        **Category & Order Status**

        • Chi-square test: **χ² = 7.93, p = 0.440**
        • No statistically significant association was detected
          between product category and order status.
        """
    )

    st.markdown(
        """
        **Delivery Time by Category**

        • ANOVA: **F = 0.97, p = 0.423**
        • Kruskal–Wallis: **H = 4.68, p = 0.322**
        • Delivery times do not show statistically significant
          differences across categories.
        """
    )

st.divider()

# ------------------------------------------------------------
# Predictive Analysis
# ------------------------------------------------------------

st.markdown("### 🤖 Predictive & Regression Findings")

r1, r2 = st.columns(2)

with r1:

    st.markdown(
        """
        **Multiple Linear Regression**

        Total Amount was modelled using Quantity, Unit Price,
        Discount, Customer Age and Delivery Days.

        **R² ≈ 0.40**

        Quantity and Unit Price were the primary positive
        contributors to order value, while Discount showed a
        negative coefficient.
        """
    )

with r2:

    st.markdown(
        """
        **Polynomial Regression**

        Adding a squared Unit Price term increased the model
        **R² from approximately 0.40 to 0.73**, indicating that
        the relationship between Unit Price and Total Amount
        contains a substantial non-linear component.
        """
    )

# ------------------------------------------------------------
# Data Quality Note
# ------------------------------------------------------------

st.divider()

st.markdown("### 🔎 Data Quality Note")

st.info(
    """
    The analytical dataset contains **9,991 cleaned orders**.
    Rating-based metrics use only valid ratings, while delivery
    metrics use records with valid delivery durations. Missing
    ratings and delivery dates were not artificially imputed when
    their absence was associated with order status.
    """
)


# ============================================================
# DASHBOARD FOOTER
# ============================================================

st.markdown(
    """
    <div class="dashboard-footer">
        <b>Shopease Analytics Dashboard</b><br>
        Foundations of Big Data Analytics with Python |
        Interactive Business Intelligence Project |
        Dataset: 9,991 cleaned orders
    </div>
    """,
    unsafe_allow_html=True
)
