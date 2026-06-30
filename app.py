import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

# --- 1. SET UP DESKTOP LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Enterprise Analytics - Interactive Map Canvas",
    layout="wide", 
    initial_sidebar_state="expanded" # Sidebar opened by default for filtering
)

# --- 2. CUSTOM NEON DARK THEME INJECTION (CSS) ---
st.markdown("""
    <style>
        .stApp {
            background-color: #171b30 !important;
            color: #ffffff !important;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
            color: #ffffff !important;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        /* Style the sidebar cleanly */
        section[data-testid="stSidebar"] {
            background-color: #111424 !important;
            border-right: 1px solid #334155;
        }
        section[data-testid="stSidebar"] .stMarkdown h2 {
            color: #38bdf8 !important; /* Neon Cyan Header */
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ALTAIR GLOBAL NEON CONFIG ---
def neon_theme():
    return {
        'config': {
            'background': '#171b30',
            'view': {'stroke': 'transparent'},
            'axis': {'domainColor': '#475569', 'gridColor': '#334155', 'labelColor': '#94a3b8', 'titleColor': '#ffffff'},
            'legend': {'labelColor': '#94a3b8', 'titleColor': '#ffffff'},
            'range': {'category': ['#f43f5e', '#38bdf8', '#a855f7', '#34d399', '#fbbf24']}
        }
    }
alt.themes.register('neon_theme', neon_theme)
alt.themes.enable('neon_theme')

# --- 4. DICTIONARY MAPS: NAMES TO NUMERIC TOPOLOGY IDs ---
US_STATE_MAPPING = {
    "Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6, "Colorado": 8, 
    "Connecticut": 9, "Delaware": 10, "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, 
    "Illinois": 17, "Indiana": 18, "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22, 
    "Maine": 23, "Maryland": 24, "Massachusetts": 25, "Michigan": 26, "Minnesota": 27, 
    "Mississippi": 28, "Missouri": 29, "Montana": 30, "Nebraska": 31, "Nevada": 32, 
    "New Hampshire": 33, "New Jersey": 34, "New Mexico": 35, "New York": 36, "North Carolina": 37, 
    "North Dakota": 38, "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42, 
    "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46, "Tennessee": 47, "Texas": 48, 
    "Utah": 49, "Vermont": 50, "Virginia": 51, "Washington": 53, "West Virginia": 54, 
    "Wisconsin": 55, "Wyoming": 56
}

EU_COUNTRY_MAPPING = {
    "Austria": 40, "Belgium": 56, "Bulgaria": 100, "Croatia": 191, "Cyprus": 196, 
    "Czechia": 203, "Denmark": 208, "Estonia": 233, "Finland": 246, "France": 250, 
    "Germany": 276, "Greece": 300, "Hungary": 348, "Ireland": 372, "Italy": 380, 
    "Latvia": 428, "Lithuania": 440, "Luxembourg": 442, "Malta": 470, "Netherlands": 528, 
    "Poland": 616, "Portugal": 620, "Romania": 642, "Slovakia": 703, "Slovenia": 705, 
    "Spain": 724, "Sweden": 752, "United Kingdom": 826, "Norway": 578, "Switzerland": 756
}

# --- 5. GENERATE SIMULATED BUSINESS DATA ---
@st.cache_data
def get_clean_geo_dataset():
    np.random.seed(42)
    rows = []
    
    # Generate full data for US states
    for name, uid in US_STATE_MAPPING.items():
        rev = float(np.random.exponential(scale=15000) + 5000)
        prof = rev * float(np.random.uniform(0.2, 0.5))
        rows.append({"Type": "US", "Name": name, "id": uid, "Gross Revenue": rev, "Net Profit": prof})
        
    # Generate full data for European nations
    for name, uid in EU_COUNTRY_MAPPING.items():
        rev = float(np.random.exponential(scale=12000) + 4000)
        prof = rev * float(np.random.uniform(0.15, 0.45))
        rows.append({"Type": "EU", "Name": name, "id": uid, "Gross Revenue": rev, "Net Profit": prof})
        
    return pd.DataFrame(rows)

df_raw = get_clean_geo_dataset()

# --- 6. SIDEBAR: FILTER CONTROL PANEL ---
st.sidebar.header("🎛️ Control Panel Slicers")
st.sidebar.markdown("---")

# Slicer 1: Metric Value Selector Toggle
target_metric = st.sidebar.radio(
    "📊 Select Target Focus Metric",
    options=["Gross Revenue", "Net Profit"],
    index=0
)

# Choose map color palette based on selected metric for better UX
color_scheme = "magma" if target_metric == "Gross Revenue" else "viridis"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Territory Sub-Filters")

# Slicer 2: US States Specific Multi-select Dropdown Filter
selected_us = st.sidebar.multiselect(
    "🇺🇸 Filter US States",
    options=list(US_STATE_MAPPING.keys()),
    default=list(US_STATE_MAPPING.keys())
)

# Slicer 3: European Countries Specific Multi-select Dropdown Filter
selected_eu = st.sidebar.multiselect(
    "🇪🇺 Filter European Nations",
    options=list(EU_COUNTRY_MAPPING.keys()),
    default=list(EU_COUNTRY_MAPPING.keys())
)

# Apply filter masks based on selections
df_us_filtered = df_raw[(df_raw["Type"] == "US") & (df_raw["Name"].isin(selected_us))]
df_eu_filtered = df_raw[(df_raw["Type"] == "EU") & (df_raw["Name"].isin(selected_eu))]

# --- 7. MAIN CANVAS LAYOUT AND HEADERS ---
st.title("📊 High-Density Infographic Canvas")
st.caption(f"Active Live Filter Mode | Currently Analyzing: **{target_metric}**")
st.markdown("---")

# --- ROW 1: CORE DUAL GEOGRAPHIC CANVASES ---
map_col1, map_col2 = st.columns(2)

with map_col1:
    st.markdown(f"#### 🇺🇸 United States Distribution ({target_metric})")
    
    if not df_us_filtered.empty:
        states_topo = alt.topo_feature(data.us_10m.url, 'states')
        
        us_map = alt.Chart(states_topo).mark_geoshape(stroke="#171b30", strokeWidth=0.5).encode(
            color=alt.Color(f'{target_metric}:Q', 
                            scale=alt.Scale(scheme=color_scheme),
                            legend=alt.Legend(title=f"{target_metric} ($)", orient='bottom', format='$,.0f')),
            tooltip=[
                alt.Tooltip('Name:N', title='State Name'),
                alt.Tooltip(f'{target_metric}:Q', title=target_metric, format='$,.2f')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(df_us_filtered, 'id', ['Name', target_metric])
        ).properties(height=400).project(type='albersUsa')
        
        st.altair_chart(us_map, use_container_width=True)
    else:
        st.warning("Please select at least one US state in the sidebar dashboard panel.")

with map_col2:
    st.markdown(f"#### 🇪🇺 Continental Europe Distribution ({target_metric})")
    
    if not df_eu_filtered.empty:
        world_topo = alt.topo_feature(data.world_110m.url, 'countries')
        
        eu_map = alt.Chart(world_topo).mark_geoshape(stroke="#171b30", strokeWidth=0.8).encode(
            color=alt.Color(f'{target_metric}:Q', 
                            scale=alt.Scale(scheme=color_scheme),
                            legend=alt.Legend(title=f"{target_metric} ($)", orient='bottom', format='$,.0f')),
            tooltip=[
                alt.Tooltip('Name:N', title='Country Name'),
                alt.Tooltip(f'{target_metric}:Q', title=target_metric, format='$,.2f')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(df_eu_filtered, 'id', ['Name', target_metric])
        ).properties(height=400).project(
            type='mercator',
            scale=420,
            center=[10, 52]
        )
        st.altair_chart(eu_map, use_container_width=True)
    else:
        st.warning("Please select at least one European country in the sidebar dashboard panel.")

st.markdown("---")

# --- ROW 2: SUMMARY SUMMARY TOTAL METRIC FOOTERS ---
tot_col1, tot_col2, tot_col3, tot_col4 = st.columns(4)
with tot_col1:
    st.metric("Total Selected US Revenue", f"${df_us_filtered['Gross Revenue'].sum():,.2f}")
with tot_col2:
    st.metric("Total Selected US Profit", f"${df_us_filtered['Net Profit'].sum():,.2f}")
with tot_col3:
    st.metric("Total Selected EU Revenue", f"${df_eu_filtered['Gross Revenue'].sum():,.2f}")
with tot_col4:
    st.metric("Total Selected EU Profit", f"${df_eu_filtered['Net Profit'].sum():,.2f}")
