import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- 1. SET UP DESKTOP LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Enterprise Analytics - Power BI Canvas",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. GENERATE COMPREHENSIVE ENTERPRISE DATASET ---
@st.cache_data
def get_enterprise_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-06-30", freq="D")
    segments = ["Enterprise", "Mid-Market", "SMB", "Public Sector"]
    regions = ["North America", "EMEA", "APAC", "LATAM"]
    products = ["Cloud Infrastructure", "AI Core Suite", "CyberShield", "Data Mesh Hub"]
    
    rows = []
    for _ in range(2500):
        date = np.random.choice(dates)
        segment = np.random.choice(segments)
        region = np.random.choice(regions)
        product = np.random.choice(products)
        revenue = float(np.random.exponential(scale=5000) + np.random.randint(1000, 20000))
        margin = float(np.random.uniform(0.15, 0.65))
        
        rows.append({
            "Date": date, "Segment": segment, "Region": region, 
            "Product Suite": product, "Gross Revenue": revenue, "Profit Margin": margin
        })
    df = pd.DataFrame(rows)
    df["Net Profit"] = df["Gross Revenue"] * df["Profit Margin"]
    return df

df_raw = get_enterprise_data()

# --- 3. POWER BI FILTER PANE (SIDEBAR) ---
st.sidebar.header("⏳ Global Slicers & Filters")
st.sidebar.markdown("---")

min_date, max_date = df_raw["Date"].min().to_pydatetime(), df_raw["Date"].max().to_pydatetime()

# Date Range Picker Slicer with Safe Empty Handling
selected_dates = st.sidebar.date_input(
    "Date Horizon Window", 
    value=[min_date, max_date], 
    min_value=min_date, 
    max_value=max_date
)

# Multi-select Categorical Slicers
selected_regions = st.sidebar.multiselect("Geographic Regions", options=list(df_raw["Region"].unique()), default=list(df_raw["Region"].unique()))
selected_segments = st.sidebar.multiselect("Market Segments", options=list(df_raw["Segment"].unique()), default=list(df_raw["Segment"].unique()))
selected_products = st.sidebar.multiselect("Product Offerings", options=list(df_raw["Product Suite"].unique()), default=list(df_raw["Product Suite"].unique()))

# FIX: Hardened Slicer Range Check Logic (handles mid-click single date states)
if isinstance(selected_dates, list) or isinstance(selected_dates, tuple):
    if len(selected_dates) == 2:
        start_d, end_d = pd.Timestamp(selected_dates[0]), pd.Timestamp(selected_dates[1])
    elif len(selected_dates) == 1:
        start_d = pd.Timestamp(selected_dates[0])
        end_d = pd.Timestamp(max_date)
    else:
        start_d, end_d = pd.Timestamp(min_date), pd.Timestamp(max_date)
else:
    # Fallback if UI element passes single instance object value
    start_d = pd.Timestamp(selected_dates)
    end_d = pd.Timestamp(max_date)

# Memory Array Boolean Array Filtering Sequence
df_filtered = df_raw[
    (df_raw["Date"] >= start_d) & (df_raw["Date"] <= end_d) &
    (df_raw["Region"].isin(selected_regions)) &
    (df_raw["Segment"].isin(selected_segments)) &
    (df_raw["Product Suite"].isin(selected_products))
]

# --- 4. MAIN CANVAS HEADERS ---
st.title("📊 Power BI Native Functional Emulator")
st.caption("Active Desktop Mode | Instant Matrix Cross-Filtering Array Engine")

# --- 5. HIGH-DENSITY KPI TILES ---
st.markdown("### 🔑 Key Performance Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

deal_count = len(df_filtered)
if deal_count > 0:
    total_rev = df_filtered["Gross Revenue"].sum()
    total_profit = df_filtered["Net Profit"].sum()
    avg_margin = df_filtered["Profit Margin"].mean() * 100
    avg_ticket = total_rev / deal_count
else:
    total_rev, total_profit, avg_margin, avg_ticket = 0.0, 0.0, 0.0, 0.0

with kpi_col1:
    st.metric(label="Gross Revenue Portfolio", value=f"${total_rev:,.2f}", delta=f"{deal_count} Won Contracts")
with kpi_col2:
    st.metric(label="Net Operational Profits", value=f"${total_profit:,.2f}")
with kpi_col3:
    st.metric(label="Avg Combined Profit Margin", value=f"{avg_margin:.2f}%")
with kpi_col4:
    st.metric(label="Average Ticket Velocity Value", value=f"${avg_ticket:,.2f}")

# --- 6. INTERACTIVE DUAL VISUALIZATION ROW ---
chart_col1, chart_col2 = st.columns([2, 1])

with chart_col1:
    st.subheader("📈 Revenue Performance Trajectory Over Time")
    if deal_count > 0:
        # Resample data safely for time series aggregation
        df_trend = df_filtered.resample('W', on='Date')[['Gross Revenue', 'Net Profit']].sum().reset_index()
        
        trend_chart = alt.Chart(df_trend).mark_area(opacity=0.3, color="#1f77b4").encode(
            x=alt.X('Date:T', title='Timeline Window'),
            y=alt.Y('Gross Revenue:Q', title='Gross Revenue ($)'),
            tooltip=['Date:T', alt.Tooltip('Gross Revenue:Q', format='$,.2f')]
        ).properties(height=350).interactive()
        
        line_chart = alt.Chart(df_trend).mark_line(color="#1f77b4", strokeWidth=3).encode(
            x='Date:T',
            y='Gross Revenue:Q'
        )
        st.altair_chart(trend_chart + line_chart, use_container_width=True)
    else:
        st.info("No timeline data matching current filters.")

with chart_col2:
    st.subheader("🍰 Product Revenue Mix")
    if deal_count > 0:
        donut_chart = alt.Chart(df_filtered).mark_arc(innerRadius=60).encode(
            theta=alt.Theta(field="Gross Revenue", type="quantitative", aggregate="sum"),
            color=alt.Color(field="Product Suite", type="nominal", scale=alt.Scale(scheme="tableau10")),
            tooltip=["Product Suite", alt.Tooltip("sum(Gross Revenue):Q", format="$,.2f")]
        ).properties(height=350)
        st.altair_chart(donut_chart, use_container_width=True)
    else:
        st.info("No product mix matches found.")

# --- 7. DRILL-DOWN DATA TABLE MATRIX ---
st.subheader("🔍 Transaction Ledger Audit Trail Grid")
tab_matrix, tab_raw_inspect = st.tabs(["Aggregated Matrix View", "Raw Segment Records Inspector"])

with tab_matrix:
    if deal_count > 0:
        pivot_df = df_filtered.groupby(["Region", "Product Suite"])["Gross Revenue"].sum().unstack().fillna(0)
        st.dataframe(pivot_df.style.format("${:,.2f}").background_gradient(cmap="Blues"), use_container_width=True)
    else:
        st.info("No matrix aggregations available for the selected filters.")

with tab_raw_inspect:
    st.dataframe(
        df_filtered.sort_values(by="Date", ascending=False),
        column_config={
            "Date": st.column_config.DateColumn("Date Horizon"),
            "Gross Revenue": st.column_config.NumberColumn("Total Sales Revenue", format="$%.2f"),
            "Net Profit": st.column_config.NumberColumn("Net Earnings Margin", format="$%.2f"),
            "Profit Margin": st.column_config.ProgressColumn("Margin Density Bar", min_value=0, max_value=1, format="%.2f")
        },
        use_container_width=True,
        hide_index=True
    )
