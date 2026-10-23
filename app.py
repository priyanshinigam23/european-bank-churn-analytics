
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="European Bank Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)


# Premium Dark Banking Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0B1120;
        color: #F1F5F9;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    h1, h2, h3 {
        color: #D4AF37 !important;
    }

    [data-testid="stMetric"] {
        background-color: #172033;
        border: 1px solid #344054;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #CBD5E1;
    }

    [data-testid="stMetricValue"] {
        color: #D4AF37;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        background-color: #D4AF37;
        color: #0B1120;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        background-color: #F1D477;
        color: #0B1120;
        border: none;
    }
    
    /* Section separators */
    hr {
        border-color: #334155 !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Improve general text readability */
    p, li, label {
        color: #CBD5E1;
    }

    /* Rounded data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #344054;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Subtle card-style containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #344054;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("European_Bank_Cleaned.csv")


# Sidebar filters
st.sidebar.header("Filter Customers")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

selected_age_group = st.sidebar.multiselect(
    "Select Age Group",
    options=df["Age_Group"].dropna().unique().tolist(),
    default=df["Age_Group"].dropna().unique().tolist()
)

# Apply filters
filtered_df = df[
    (df["Geography"].isin(selected_country)) &
    (df["Gender"].isin(selected_gender)) &
    (df["Age_Group"].isin(selected_age_group))
]

st.sidebar.write("Filtered Customers:", len(filtered_df))

# Dashboard heading

st.title("🏦 European Banking | Customer Churn Analytics")

st.markdown(
    """
    **Customer Segmentation & Churn Pattern Analytics**

    Explore customer retention, churn behaviour, and risk patterns
    across customer demographics, account activity, and banking products.
    """
)

st.divider()



# Executive Summary
st.subheader("📌 Executive Summary")

st.info(
    "This dashboard analyses 10,000 European banking customer "
    "records from 2025. The overall churn rate is 20.37%."
)

st.markdown("### 🔍 Key Findings")
st.markdown("""
- **Germany:** 32.44% observed churn rate.
- **Age 46–60:** 51.12% observed churn rate.
- **Inactive customers:** 26.85% churn rate.
- **High-balance customers:** 25.23% churn rate.
""")

st.markdown("### 🎯 Business Priorities")
st.markdown("""
1. Investigate churn patterns among German customers.
2. Test re-engagement campaigns for inactive customers.
3. Study retention opportunities for customers aged 46–60.
4. Measure campaign effectiveness.
""")

st.divider()



st.divider()


# Calculate KPIs using filtered data
total_customers = len(filtered_df)
churned_customers = int(filtered_df["Exited"].sum())
retained_customers = total_customers - churned_customers

if total_customers > 0:
    churn_rate = (churned_customers / total_customers) * 100
    retention_rate = (retained_customers / total_customers) * 100
else:
    churn_rate = 0
    retention_rate = 0



# Display KPI cards
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Retention Rate", f"{retention_rate:.2f}%")


# Country-wise churn analysis
st.subheader("🌍 Customer Churn by Country")

country_churn = filtered_df.groupby("Geography").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

country_churn["Churn_Rate_%"] = (
    country_churn["Churned_Customers"]
    / country_churn["Total_Customers"] * 100
).round(2)

# Display chart

# Premium Country-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

country_data = country_churn["Churn_Rate_%"]

bars = ax.bar(
    country_data.index,
    country_data.values,
    color="#2DD4BF",
    width=0.55
)

ax.set_title("Country-wise Churn Rate", color="#D4AF37", fontsize=15, pad=15)
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")
ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Display detailed table
st.dataframe(country_churn, use_container_width=True)


# Age group-wise churn analysis
st.subheader("👥 Customer Churn by Age Group")

age_churn = filtered_df.groupby("Age_Group", observed=False).agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

age_churn["Churn_Rate_%"] = (
    age_churn["Churned_Customers"]
    / age_churn["Total_Customers"] * 100
).round(2)

# Display chart

# Premium Age Group Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

age_data = age_churn["Churn_Rate_%"]

bars = ax.bar(
    age_data.index.astype(str),
    age_data.values,
    color="#2DD4BF",
    width=0.55
)

ax.set_title("Age Group-wise Churn Rate", color="#D4AF37", fontsize=15, pad=15)
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9", rotation=0)
ax.tick_params(axis="y", colors="#F1F5F9")
ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Display detailed table
st.dataframe(age_churn, use_container_width=True)


# Gender-wise churn analysis
st.subheader("👩‍💼 Customer Churn by Gender")

gender_churn = filtered_df.groupby("Gender").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

gender_churn["Churn_Rate_%"] = (
    gender_churn["Churned_Customers"]
    / gender_churn["Total_Customers"] * 100
).round(2)

# Display chart and table

# Premium Gender-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

gender_data = gender_churn["Churn_Rate_%"]

bars = ax.bar(
    gender_data.index.astype(str),
    gender_data.values,
    color=["#D4AF37", "#2DD4BF"],
    width=0.5
)

ax.set_title("Gender-wise Churn Rate", color="#D4AF37", fontsize=15, pad=15)
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")
ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.dataframe(gender_churn, use_container_width=True)


# Active vs Inactive Customer Churn Analysis
st.subheader("📊 Churn by Customer Activity")

activity_churn = filtered_df.groupby("IsActiveMember").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

activity_churn["Churn_Rate_%"] = (
    activity_churn["Churned_Customers"]
    / activity_churn["Total_Customers"] * 100
).round(2)

# Make labels easy to understand
activity_churn.index = activity_churn.index.map({
    0: "Inactive",
    1: "Active"
})


# Premium Activity-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

activity_data = activity_churn["Churn_Rate_%"]

bars = ax.bar(
    activity_data.index.astype(str),
    activity_data.values,
    color=["#D4AF37", "#2DD4BF"],
    width=0.5
)

ax.set_title("Customer Activity vs Churn Rate", color="#D4AF37", fontsize=15, pad=15)
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")
ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.dataframe(activity_churn, use_container_width=True)


# Product-wise churn analysis
st.subheader("🏦 Churn by Number of Products")

product_churn = filtered_df.groupby("NumOfProducts").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

product_churn["Churn_Rate_%"] = (
    product_churn["Churned_Customers"]
    / product_churn["Total_Customers"] * 100
).round(2)


# Premium Product-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

product_data = product_churn["Churn_Rate_%"]

bars = ax.bar(
    product_data.index.astype(str),
    product_data.values,
    color="#2DD4BF",
    width=0.55
)

ax.set_title("Number of Products vs Churn Rate", color="#D4AF37", fontsize=15, pad=15)
ax.set_xlabel("Number of Products", color="#CBD5E1")
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")
ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=9
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.dataframe(product_churn, use_container_width=True)


# Credit score-wise churn analysis
st.subheader("💳 Churn by Credit Score")

credit_churn = filtered_df.groupby("CreditScore_Band").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

credit_churn["Churn_Rate_%"] = (
    credit_churn["Churned_Customers"]
    / credit_churn["Total_Customers"] * 100
).round(2)


# Premium Credit Score-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

credit_data = credit_churn["Churn_Rate_%"]

bars = ax.bar(
    credit_data.index.astype(str),
    credit_data.values,
    color="#2DD4BF",
    width=0.55
)

ax.set_title(
    "Credit Score Band vs Churn Rate",
    color="#D4AF37",
    fontsize=15,
    pad=15
)
ax.set_xlabel("Credit Score Band", color="#CBD5E1")
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")

ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Display table
st.dataframe(credit_churn, use_container_width=True)

st.dataframe(credit_churn, use_container_width=True)


# Tenure-wise churn analysis
st.subheader("📅 Churn by Customer Tenure")

tenure_churn = filtered_df.groupby("Tenure_Group").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

tenure_churn["Churn_Rate_%"] = (
    tenure_churn["Churned_Customers"]
    / tenure_churn["Total_Customers"] * 100
).round(2)


# Premium Tenure-wise Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

tenure_data = tenure_churn["Churn_Rate_%"]

bars = ax.bar(
    tenure_data.index.astype(str),
    tenure_data.values,
    color="#2DD4BF",
    width=0.55
)

ax.set_title(
    "Customer Tenure vs Churn Rate",
    color="#D4AF37",
    fontsize=15,
    pad=15
)
ax.set_xlabel("Tenure Group", color="#CBD5E1")
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9")
ax.tick_params(axis="y", colors="#F1F5F9")

ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Display table
st.dataframe(tenure_churn, use_container_width=True)

st.dataframe(tenure_churn, use_container_width=True)


# Balance segment-wise churn analysis
st.subheader("💰 Churn by Balance Segment")

balance_churn = filtered_df.groupby("Balance_Segment").agg(
    Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", "sum")
)

balance_churn["Churn_Rate_%"] = (
    balance_churn["Churned_Customers"]
    / balance_churn["Total_Customers"] * 100
).round(2)


# Premium Balance Segment Churn Chart
fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

balance_data = balance_churn["Churn_Rate_%"]

bars = ax.bar(
    balance_data.index.astype(str),
    balance_data.values,
    color=["#64748B", "#2DD4BF", "#D4AF37"],
    width=0.55
)

ax.set_title(
    "Balance Segment vs Churn Rate",
    color="#D4AF37",
    fontsize=15,
    pad=15
)
ax.set_xlabel("Balance Segment", color="#CBD5E1")
ax.set_ylabel("Churn Rate (%)", color="#CBD5E1")
ax.tick_params(axis="x", colors="#F1F5F9", rotation=0)
ax.tick_params(axis="y", colors="#F1F5F9")

ax.spines["bottom"].set_color("#475569")
ax.spines["left"].set_color("#475569")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", color="#334155", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.5,
        f"{height:.2f}%",
        ha="center",
        color="#F1F5F9",
        fontsize=10
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Display table
st.dataframe(balance_churn, use_container_width=True)

st.dataframe(balance_churn, use_container_width=True)


# High-value customer analysis
st.subheader("💎 High-Value Customer Analysis")

high_value_customers = filtered_df[
    filtered_df["Balance_Segment"] == "High-balance"
]

total_high_value = len(high_value_customers)
churned_high_value = int(high_value_customers["Exited"].sum())

if total_high_value > 0:
    high_value_churn_rate = (
        churned_high_value / total_high_value
    ) * 100
else:
    high_value_churn_rate = 0

col1, col2, col3 = st.columns(3)

col1.metric("High-Balance Customers", f"{total_high_value:,}")
col2.metric("Churned High-Balance Customers", f"{churned_high_value:,}")
col3.metric("High-Balance Churn Rate", f"{high_value_churn_rate:.2f}%")

st.dataframe(high_value_customers, use_container_width=True)


# Strategic Planning and Marketing Recommendations
st.divider()
st.subheader("🎯 Strategic Planning & Marketing")

st.markdown("""
### 1. Country-Specific Marketing
- **Germany:** Prioritize churn-prevention campaigns because
  the observed churn rate is 32.44%.
- **Spain and France:** Study their lower churn rates to identify
  retention practices that may be useful elsewhere.

### 2. Customer Engagement
- Target inactive customers with personalized re-engagement campaigns.
- Use relevant offers, service reminders, and feedback surveys.

### 3. Age-Based Retention
- Investigate the needs of customers aged 46–60, whose observed
  churn rate is 51.12%.
- Test personalized retention offers for this segment.

### 4. Product Strategy
- Investigate why customers with only one product have a higher
  churn rate than customers with two products.
- Test relevant product recommendations without pressuring customers.

### 5. High-Balance Customer Retention
- Prioritize understanding the needs of high-balance customers.
- Offer suitable service support and personalized communication.

### 6. Measure Campaign Performance
- Track churn rate before and after each campaign.
- Compare customer retention, campaign cost, and conversion rates.
- Use controlled tests where possible to evaluate campaign effectiveness.
""")


# Dataset information
st.divider()
st.subheader("📁 Dataset Overview")

info1, info2, info3 = st.columns(3)

info1.metric("Total Records in Dataset", f"{len(df):,}")
info2.metric("Total Columns", len(df.columns))
info3.metric("Customers After Filters", f"{len(filtered_df):,}")

st.caption(
    "Dataset period: 2025 | Churn target: Exited (1 = Churned, 0 = Retained)"
)


# Customer data preview
st.subheader("📋 Customer Data Preview")

st.write("View the customer records matching your selected filters.")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download filtered customer data
st.subheader("⬇️ Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Customer Data as CSV",
    data=csv_data,
    file_name="European_Bank_Filtered_Customers.csv",
    mime="text/csv"
)
