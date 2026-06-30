import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

# --- 1. SET UP DESKTOP LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Enterprise Analytics - Full Canvas Dashboard",
    layout="wide", 
    initial_sidebar_state="collapsed"
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
        [data-testid="stMetricValue"] {
            color: #f43f5e !important;
            font-size: 2.2rem !important;
            font-weight: 700;
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
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
                'category': ['#f43f5e', '#38bdf8', '#a855f7', '#34d399', '#fbbf24']
            }
        }
    }
alt.themes.register('neon_theme', neon_theme)
alt.themes.enable('neon_theme')

# --- 4. GENERATE FULL GEOGRAPHIC DATASETS ---
@st.cache_data
def get_comprehensive_geo_data():
    np.random.seed(42)
    
    # Complete list of numeric ANSI FIPS codes for all 50 US States
    all_us_states = [
        1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 
        44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56
    ]
    
    # Complete numeric ISO-3166-1 keys for all European Union & continental nations
    all_eu_countries = [
        40, 56, 100, 191, 203, 208, 233, 246, 250, 276, 300, 348, 372, 380, 428, 
        440, 442, 470, 528, 616, 620, 642, 703, 705, 724, 752, 756, 826, 404, 578
    ]
    
    rows = []
    
    # Populate every single US state with random revenue
    for state_id in all_us_states:
        revenue = float(np.random.exponential(scale=8000) + np.random.randint(5000, 25000))
        rows.append({"type": "US", "id": state_id, "Revenue": revenue})
        
    # Populate every single European country with random revenue
    for country_id in all_eu_countries:
        revenue = float(np.random.exponential(scale=7500) + np.random.randint(4000, 22000))
        rows.append({"type": "EU", "id": country_id, "Revenue": revenue})
        
    return pd.DataFrame(rows)

df_geo = get_comprehensive_geo_data()

# Split data frames out clean
df_us_agg = df_geo[df_geo["type"] == "US"]
df_eu_agg = df_geo[df_geo["type"] == "EU"]

# --- 5. MAIN CONTAINER HEADERS ---
st.title("📊 High-Density Infographic Canvas")
st.caption("Global Operations Metrics Dashboard | Complete Regional Geospatial Engine")
st.markdown("---")

# --- 6. CORE GEOGRAPHIC DOUBLE MAP ROW ---
map_col1, map_col2 = st.columns(2)

with map_col1:
    st.markdown("#### 🇺🇸 Full United States Territory Performance Map")
    
    # Source official TopoJSON file for accurate US State polygons
    states_topo = alt.topo_feature(data.us_10m.url, 'states')
    
    us_map = alt.Chart(states_topo).mark_geoshape(stroke="#171b30", strokeWidth=0.5).encode(
        color=alt.Color('Revenue:Q', 
                        scale=alt.Scale(scheme='magma'),
                        legend=alt.Legend(title="Sales Performance ($)", orient='bottom', format='$,.0f')),
        tooltip=[
            alt.Tooltip('id:O', title='State Code ID'),
            alt.Tooltip('Revenue:Q', title='Gross Revenue', format='$,.2f')
        ]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_us_agg, 'id', ['Revenue'])
    ).properties(
        height=400
    ).project(
        type='albersUsa'
    )
    st.altair_chart(us_map, use_container_width=True)

with map_col2:
    st.markdown("#### 🇪🇺 Continental European Market Volume Map")
    
    # Source official TopoJSON file for World Countries
    world_topo = alt.topo_feature(data.world_110m.url, 'countries')
    
    eu_map = alt.Chart(world_topo).mark_geoshape(stroke="#171b30", strokeWidth=0.8).encode(
        color=alt.Color('Revenue:Q', 
                        scale=alt.Scale(scheme='plasma'),
                        legend=alt.Legend(title="Market Volume ($)", orient='bottom', format='$,.0f')),
        tooltip=[
            alt.Tooltip('id:O', title='Country Code ID'),
            alt.Tooltip('Revenue:Q', title='Gross Revenue', format='$,.2f')
        ]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_eu_agg, 'id', ['Revenue'])
    ).properties(
        height=400
    ).project(
        type='mercator',
        scale=450,              # Perfect bounding zoom to show all European borders cleanly
        center=[12, 53]         # Centers map view directly above Germany/Central Europe
    )
    st.altair_chart(eu_map, use_container_width=True)

st.markdown("---")
st.info("💡 Interactive Tip: Hover your mouse directly over any populated region on either map to view exact financial reporting metrics.")
