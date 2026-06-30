import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- 1. SET UP DESKTOP LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Enterprise Analytics - High-Density Canvas",
    layout="wide", 
    initial_sidebar_state="collapsed" # Collapsed to maximize canvas area
)

# --- 2. CUSTOM NEON DARK THEME INJECTION (CSS) ---
st.markdown("""
    <style>
        /* Main background color matching the image */
        .stApp {
            background-color: #171b30 !important;
            color: #ffffff !important;
        }
        /* Style standard text and headers to neon white/pink */
        h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        /* Custom styling for Streamlit metric widgets */
        [data-testid="stMetricValue"] {
            color: #f43f5e !important; /* Neon Pink */
            font-size: 2.2rem !important;
            font-weight: 700;
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important; /* Muted Slate */
        }
        /* Clean tabs matching dark theme */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #111424;
            padding: 5px;
            border-radius: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #38bdf8 !important; /* Neon Cyan */
            border-bottom-color: #38bdf8 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ALTAIR NEON DATA GLOBAL VISUAL THEME CONFIG ---
def neon_theme():
    return {
        'config': {
            'background': '#171b30',
            'view': {'stroke': 'transparent'},
            'axis': {
                'domainColor': '#475569',
                'gridColor': '#334155',
                'labelColor': '#94a3b8',
                'titleColor': '#ffffff',
                'tickColor': '#475569'
            },
            'legend': {
                'labelColor': '#94a3b8',
                'titleColor': '#ffffff'
            },
            'range': {
                'category': ['#f43f5e', '#38bdf8', '#a855f7', '#34d399', '#fbbf24'] # Pink, Cyan, Purple, Green, Yellow
            }
        }
    }
alt.themes.register('neon_theme', neon_theme)
alt.themes.enable('neon_theme')

# --- 4. GENERATE COMPREHENSIVE DATASET ---
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

df_filtered = get_enterprise_data()

# --- 5. APP CONTAINER LAYOUT ---
st.title("📊 High-Density Infographic Canvas")
st.markdown("---")

# --- ROW 1: INFOGRAPHIC METRIC RINGS (Radial Progress Gauges) ---
st.markdown("### 🎯 Core Target Capacities")
ring_col1, ring_col2, ring_col3, ring_col4 = st.columns(4)

def make_radial_chart(value, label, color):
    source = pd.DataFrame({"values": [value, 100 - value], "category": ["Completed", "Remaining"]})
    chart = alt.Chart(source).mark_arc(innerRadius=45, outerRadius=60).encode(
        theta=alt.Theta(field="values", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(domain=["Completed", "Remaining"], range=[color, "#1e293b"]), legend=None),
    ).properties(width=140, height=140)
    
    text = alt.Chart(pd.DataFrame({"text": [f"{value}%"]})).mark_text(
        align='center', baseline='middle', fontSize=18, color='#ffffff', fontWeight='bold'
    ).encode(text='text:N')
    
    return chart + text

with ring_col1:
    st.altair_chart(make_radial_chart(80, "Enterprise", "#f43f5e"), use_container_width=False)
    st.caption("🚀 Target Growth Segment")
with ring_col2:
    st.altair_chart(make_radial_chart(75, "Mid-Market", "#38bdf8"), use_container_width=False)
    st.caption("🌐 Regional Operations")
with ring_col3:
    st.altair_chart(make_radial_chart(50, "SMB", "#a855f7"), use_container_width=False)
    st.caption("⚡ Product Portfolio")
with ring_col4:
    st.altair_chart(make_radial_chart(25, "Public", "#34d399"), use_container_width=False)
    st.caption("🔒 Security Compliance")

st.markdown("---")

# --- ROW 2: MULTI-COLUMN DATA MATRIX VISUALS ---
chart_row_col1, chart_row_col2, chart_row_col3 = st.columns([1, 1, 1])

with chart_row_col1:
    st.markdown("#### 🍩 Segment Distribution")
    donut_chart = alt.Chart(df_filtered).mark_arc(innerRadius=40).encode(
        theta=alt.Theta(field="Gross Revenue", type="quantitative", aggregate="sum"),
        color=alt.Color(field="Segment", type="nominal"),
        tooltip=["Segment", "sum(Gross Revenue)"]
    ).properties(height=230)
    st.altair_chart(donut_chart, use_container_width=True)

with chart_row_col2:
    st.markdown("#### 📊 Monthly Generation Trends")
    df_filtered['Month'] = df_filtered['Date'].dt.strftime('%b')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    
    bar_chart = alt.Chart(df_filtered).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X('Month:N', sort=month_order, title=None),
        y=alt.Y('sum(Gross Revenue):Q', title=None),
        color=alt.value('#f43f5e') # Fixed neon pink bars
    ).properties(height=230)
    st.altair_chart(bar_chart, use_container_width=True)

with chart_row_col3:
    st.markdown("#### 📈 Multi-Layer Target Range")
    df_trend = df_filtered.resample('W', on='Date')[['Gross Revenue', 'Net Profit']].sum().reset_index()
    
    area_chart = alt.Chart(df_trend).mark_area(opacity=0.2, color="#a855f7").encode(
        x='Date:T', y='Gross Revenue:Q'
    ).properties(height=230)
    
    line_chart = alt.Chart(df_trend).mark_line(color="#38bdf8", strokeWidth=2.5).encode(
        x='Date:T', y='Net Profit:Q'
    )
    st.altair_chart(area_chart + line_chart, use_container_width=True)

st.markdown("---")

# --- ROW 3: COMPLEX INFOGRAPHIC DRILL-DOWN ---
bottom_col1, bottom_col2 = st.columns([2, 1])

with bottom_col1:
    st.markdown("#### 🧬 Product Distribution Matrix Grid")
    grouped_bars = alt.Chart(df_filtered).mark_bar(size=12).encode(
        x=alt.X('Product Suite:N', axis=alt.Axis(labels=False), title=None),
        y=alt.Y('sum(Gross Revenue):Q', title=None),
        color=alt.Color('Product Suite:N'),
        column=alt.Column('Region:N', title=None, header=alt.Header(labelColor='#94a3b8', labelOrient='bottom'))
    ).properties(height=200, width=110)
    st.altair_chart(grouped_bars, use_container_width=False)

with bottom_col2:
    st.markdown("#### 📐 Target Pyramid Priority")
    # Emulate the custom visual structures at the bottom right corner
    pyramid_data = pd.DataFrame({
        "Level": ["L1 - Core Strategy", "L2 - Execution", "L3 - Operations", "L4 - Deployment"],
        "Value": [10, 30, 60, 100]
    })
    pyramid = alt.Chart(pyramid_data).mark_bar(invalid=None).encode(
        x=alt.X('Value:Q', axis=None),
        y=alt.Y('Level:N', sort='descending', title=None),
        color=alt.Color('Level:N', scale=alt.Scale(scheme='magma'), legend=None)
    ).properties(height=200)
    st.altair_chart(pyramid, use_container_width=True)
