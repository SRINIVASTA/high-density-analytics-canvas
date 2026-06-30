import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

# --- 1. SET UP DESKTOP LAYOUT CONFIGURATION ---
st.set_page_config(
    page_title="Enterprise Analytics - High-Density Canvas",
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

# --- 4. GENERATE GEOGRAPHIC ENTERPRISE DATASET ---
@st.cache_data
def get_geo_enterprise_data():
    np.random.seed(42)
    # Correct numerical ANSI/ISO mapping keys for regions
    us_states = [6, 12, 36, 48, 53]      # California, Florida, New York, Texas, Washington
    eu_countries = [276, 250, 380, 724, 826] # Germany, France, Italy, Spain, United Kingdom
    
    rows = []
    for _ in range(1500):
        state_id = np.random.choice(us_states)
        rev_us = float(np.random.exponential(scale=7000) + 2000)
        rows.append({"type": "US", "id": state_id, "Revenue": rev_us})
        
        country_id = np.random.choice(eu_countries)
        rev_eu = float(np.random.exponential(scale=6500) + 1500)
        rows.append({"type": "EU", "id": country_id, "Revenue": rev_eu})
        
    return pd.DataFrame(rows)

df_geo = get_geo_enterprise_data()

# --- 5. DATA PRE-AGGREGATION ---
df_us_agg = df_geo[df_geo["type"] == "US"].groupby("id")["Revenue"].sum().reset_index()
df_eu_agg = df_geo[df_geo["type"] == "EU"].groupby("id")["Revenue"].sum().reset_index()

# --- 6. APP CONTAINER LAYOUT ---
st.title("📊 High-Density Infographic Canvas")
st.caption("Countrywise Operations Metrics Dashboard Panel Grid")
st.markdown("---")

# --- ROW 1: CORE COUNTRYWISE GRAPHIC LAYOUT ---
map_col1, map_col2 = st.columns(2)

with map_col1:
    st.markdown("#### 🇺🇸 US Regional Performance Territory Map")
    
    # Corrected dataset URL pointer for standard US states
    states_topo = alt.topo_feature(data.us_10m.url, 'states')
    
    us_map = alt.Chart(states_topo).mark_geoshape().encode(
        color=alt.Color('Revenue:Q', 
                        scale=alt.Scale(scheme='magma', domain=[df_us_agg['Revenue'].min(), df_us_agg['Revenue'].max()]),
                        legend=alt.Legend(title="Sales Revenue ($)", orient='bottom')),
        tooltip=[alt.Tooltip('Revenue:Q', format='$,.2f')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_us_agg, 'id', ['Revenue'])
    ).properties(
        width=550,
        height=350
    ).project(
        type='albersUsa'
    )
    st.altair_chart(us_map, use_container_width=True)

with map_col2:
    st.markdown("#### 🇪🇺 European Country Market Share Map")
    
    # FIX: Correct dataset endpoint name is world_110m
    world_topo = alt.topo_feature(data.world_110m.url, 'countries')
    
    eu_map = alt.Chart(world_topo).mark_geoshape(stroke="#171b30", strokeWidth=1).encode(
        color=alt.Color('Revenue:Q', 
                        scale=alt.Scale(scheme='plasma', domain=[df_eu_agg['Revenue'].min(), df_eu_agg['Revenue'].max()]),
                        legend=alt.Legend(title="Market Volume ($)", orient='bottom')),
        tooltip=[alt.Tooltip('Revenue:Q', format='$,.2f')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_eu_agg, 'id', ['Revenue'])
    ).properties(
        width=550,
        height=350
    ).project(
        type='mercator',
        scale=350,              
        center=[10, 52]  # Focus coordinates centered over Western Europe
    )
    st.altair_chart(eu_map, use_container_width=True)

st.markdown("---")
st.info("💡 Hint: Hover cursor directly over active map country borders to drill down into live localized dataset metrics values.")
