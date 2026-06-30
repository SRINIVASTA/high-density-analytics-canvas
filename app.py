# ==========================================
# BLOCK 1: INITIALIZATION, CONFIGURATION, AND DATA PIPELINE
# ==========================================
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

# 1. Page Configuration Settings
st.set_page_config(page_title="Executive Infographic Canvas", layout="wide", initial_sidebar_state="expanded")

# 2. Dark Neon Dashboard CSS Theme Injection
st.markdown("""
    <style>
        .stApp { background-color: #121629 !important; color: #ffffff !important; }
        h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown { color: #ffffff !important; font-family: 'Helvetica Neue', Arial, sans-serif; }
        section[data-testid="stSidebar"] { background-color: #0b0d1a !important; border-right: 1px solid #1f243d; }
        section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p { color: #38bdf8 !important; }
        .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Altair Neon Chart Theme Engine Configuration
def neon_theme():
    return {
        'config': {
            'background': '#121629', 'view': {'stroke': 'transparent'},
            'axis': {'domainColor': '#334155', 'gridColor': '#1e293b', 'labelColor': '#94a3b8', 'titleColor': '#ffffff', 'tickColor': '#334155'},
            'legend': {'labelColor': '#94a3b8', 'titleColor': '#ffffff'},
            'range': {'category': ['#ec4899', '#38bdf8', '#a855f7', '#4ade80', '#fbbf24', '#f43f5e']}
        }
    }
alt.themes.register('neon_theme', neon_theme); alt.themes.enable('neon_theme')

# 4. Global Geographic Indices Mapping Keys
US_STATE_MAPPING = {"California": 6, "Texas": 48, "New York": 36, "Florida": 12, "Illinois": 17, "Pennsylvania": 42, "Ohio": 39, "Michigan": 26, "Georgia": 13, "North Carolina": 37}
EU_COUNTRY_MAPPING = {"Germany": 276, "France": 250, "United Kingdom": 826, "Italy": 380, "Spain": 724, "Poland": 616, "Netherlands": 528, "Belgium": 56, "Sweden": 752, "Austria": 40}

# 5. Simulated Analytical Business Dataset Cache Engine
@st.cache_data
def load_dashboard_cache_arrays():
    np.random.seed(101); months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
    timeline_rows = []
    for m in months:
        for cat in ['ONE', 'TWO', 'THREE', 'FOUR']:
            timeline_rows.append({"Month": m, "Category": cat, "Value": int(np.random.randint(2, 6)), "ScatterX": int(np.random.randint(10, 70)), "ScatterY": int(np.random.randint(5, 45))})
    geo_rows = []
    for name, uid in US_STATE_MAPPING.items(): geo_rows.append({"Type": "US", "Name": name, "id": uid, "Value": float(np.random.randint(50, 100))})
    for name, uid in EU_COUNTRY_MAPPING.items(): geo_rows.append({"Type": "EU", "Name": name, "id": uid, "Value": float(np.random.randint(40, 95))})
    return pd.DataFrame(timeline_rows), pd.DataFrame(geo_rows)

df_timeline, df_geo = load_dashboard_cache_arrays()
# ==========================================
# BLOCK 2: CONTROL FILTERS, RUNTIME DATA SELECTION, AND UI GRID CANVAS
# ==========================================
# 1. Global Slicers & Sidebar Filters UI
st.sidebar.subheader("⏳ Global Slicers & Filters")
st.sidebar.markdown("---")
target_segment = st.sidebar.selectbox("🎯 Target Market Segment Focus", ["All Core Operations", "Enterprise Accounts", "Public Sector Network"])
selected_cats = st.sidebar.multiselect("📊 Active Target Categories", options=['ONE', 'TWO', 'THREE', 'FOUR'], default=['ONE', 'TWO', 'THREE', 'FOUR'])
df_time_filtered = df_timeline[df_timeline["Category"].isin(selected_cats)]

# 2. Application Core Layout Matrix Title Canvas
st.title("📊 High-Density Interactive Infographic Canvas")
st.markdown("---")

# --- GRID ROW 1: RADIAL CIRCLE GAUGES & SYMBOL POPULATION MATRICES ---
r1_c1, r1_c2, r1_c3 = st.columns([1.5, 1, 1.5])
with r1_c1:
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    def draw_radial_ring(val, color):
        src = pd.DataFrame({"v": [val, 100-val], "c": ["A", "B"]})
        arc = alt.Chart(src).mark_arc(innerRadius=24, outerRadius=34).encode(theta='v:Q', color=alt.Color('c:N', scale=alt.Scale(domain=["A", "B"], range=[color, "#1e293b"]), legend=None)).properties(width=70, height=70)
        txt = alt.Chart(pd.DataFrame({"t": [f"{val}%"]})).mark_text(align='center', baseline='middle', fontSize=11, color='#ffffff', fontWeight='bold').encode(text='t:N')
        return arc + txt
    with g_col1: st.altair_chart(draw_radial_ring(80, "#ec4899"))
    with g_col2: st.altair_chart(draw_radial_ring(75, "#38bdf8"))
    with g_col3: st.altair_chart(draw_radial_ring(50, "#a855f7"))
    with g_col4: st.altair_chart(draw_radial_ring(25, "#4ade80"))
with r1_c2:
    st.markdown("<p style='text-align:center; font-size:11px; margin:0; color:#94a3b8;'>👥 POPULATION TRACKER</p>", unsafe_allow_html=True)
    pop_df = pd.DataFrame({"x": np.repeat(range(5), 4), "y": np.tile(range(4), 5), "val": np.random.choice([0, 1], 20)})
    pop_grid = alt.Chart(pop_df).mark_square(size=120).encode(x=alt.X('x:O', axis=None), y=alt.Y('y:O', axis=None), color=alt.Color('val:N', scale=alt.Scale(domain=[0, 1], range=["#334155", "#ec4899"]), legend=None)).properties(width=120, height=65)
    st.altair_chart(pop_grid, use_container_width=True)
with r1_c3:
    st.markdown("<p style='text-align:right; font-size:11px; margin:0; color:#94a3b8;'>📐 CAPACITIES RATIO</p>", unsafe_allow_html=True)
    hex_chart = alt.Chart(pd.DataFrame({"theta":, "r": [4, 5, 3, 5, 4, 5, 4]})).mark_line(color="#a855f7", strokeWidth=2).encode(x='theta:Q', y='r:Q').properties(height=65)
    st.altair_chart(hex_chart, use_container_width=True)

st.markdown("---")

# --- GRID ROW 2: CROSS SCATTERS, PROGRESS LOADING STRIPS, AND LINES ---
r2_c1, r2_c2, r2_c3 = st.columns([1.2, 1, 1.2])
with r2_c1:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>🎯 COORDINATE INTERSECTION DISTRIBUTION</p>", unsafe_allow_html=True)
    scat = alt.Chart(df_time_filtered).mark_circle(size=60, color="#ec4899").encode(x=alt.X('ScatterX:Q', title=None), y=alt.Y('ScatterY:Q', title=None)).properties(height=160)
    st.altair_chart(scat, use_container_width=True)
with r2_c2:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📊 PERFORMANCE CAP BARS</p>", unsafe_allow_html=True)
    bars = alt.Chart(pd.DataFrame({"Metric": ["A", "B", "C", "D"], "Val": [45, 30, 20, 48]})).mark_bar(height=14, cornerRadiusEnd=4).encode(x=alt.X('Val:Q', axis=None), y=alt.Y('Metric:N', axis=None), color=alt.Color('Metric:N', scale=alt.Scale(range=["#ec4899", "#38bdf8", "#a855f7", "#4ade80"]), legend=None)).properties(height=160)
    st.altair_chart(bars, use_container_width=True)
with r2_c3:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📈 MULTI-LAYER TRAJECTORY VELOCITY</p>", unsafe_allow_html=True)
    lines = alt.Chart(df_time_filtered).mark_line(strokeWidth=2.5).encode(x=alt.X('Month:N', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'], title=None), y=alt.Y('sum(Value):Q', title=None), color='Category:N').properties(height=160)
    st.altair_chart(lines, use_container_width=True)

st.markdown("---")

# --- GRID ROW 3: TARGET DONUTS, TRACKING BARS, AND COMPLETE GEOSPATIAL MAPS ---
r3_c1, r3_c2, r3_c3, r3_c4 = st.columns([1, 1, 1.2, 1.2])
with r3_c1:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>🎯 TARGET RADAR</p>", unsafe_allow_html=True)
    pie = alt.Chart(df_time_filtered).mark_arc(innerRadius=20, outerRadius=50).encode(theta=alt.Theta(field="Value", type="quantitative", aggregate="sum"), color=alt.Color("Category:N")).properties(height=150)
    st.altair_chart(pie, use_container_width=True)
with r3_c2:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📊 MONTHLY VOLUME</p>", unsafe_allow_html=True)
    v_bars = alt.Chart(df_time_filtered).mark_bar(width=12, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(x=alt.X('Month:N', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'], title=None), y=alt.Y('sum(Value):Q', title=None), color=alt.value('#ec4899')).properties(height=150)
    st.altair_chart(v_bars, use_container_width=True)
with r3_c3:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>🇺🇸 US OPERATIONS METRIC MAP</p>", unsafe_allow_html=True)
    us_geo = alt.Chart(alt.topo_feature(data.us_10m.url, 'states')).mark_geoshape(stroke="#121629", strokeWidth=0.5).encode(color=alt.Color('Value:Q', scale=alt.Scale(scheme='magma'), legend=None)).transform_lookup(lookup='id', from_=alt.LookupData(df_geo[df_geo["Type"]=="US"], 'id', ['Value'])).properties(height=150).project(type='albersUsa')
    st.altair_chart(us_geo, use_container_width=True)
with r3_c4:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>🇪🇺 EUROPE MARKET SHARE MAP</p>", unsafe_allow_html=True)
    eu_geo = alt.Chart(alt.topo_feature(data.world_110m.url, 'countries')).mark_geoshape(stroke="#121629", strokeWidth=0.5).encode(color=alt.Color('Value:Q', scale=alt.Scale(scheme='plasma'), legend=None)).transform_lookup(lookup='id', from_=alt.LookupData(df_geo[df_geo["Type"]=="EU"], 'id', ['Value'])).properties(height=150).project(type='mercator', scale=160, center=[10, 52])
    st.altair_chart(eu_geo, use_container_width=True)

st.markdown("---")

# --- GRID ROW 4: HISTOGRAM DIVIDERS, DENSITY SEGMENTS, AND PYRAMID LAYERS ---
r4_c1, r4_c2, r4_c3 = st.columns([1.5, 1.5, 1])
with r4_c1:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📊 HISTOGRAM TIMELINE GENERATION TRACK</p>", unsafe_allow_html=True)
    hist_grid = alt.Chart(df_time_filtered).mark_bar(size=6).encode(x=alt.X('Category:N', axis=alt.Axis(labels=False), title=None), y=alt.Y('Value:Q', title=None), color=alt.Color('Category:N'), column=alt.Column('Month:N', title=None, header=alt.Header(labelColor='#94a3b8', labelOrient='bottom'))).properties(height=140, width=32)
    st.altair_chart(hist_grid, use_container_width=False)
with r4_c2:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📈 AREA HIGHLIGHT DENSITY</p>", unsafe_allow_html=True)
    area = alt.Chart(df_time_filtered).mark_area(opacity=0.3, color="#a855f7").encode(x=alt.X('Month:N', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'], title=None), y=alt.Y('sum(Value):Q', title=None)).properties(height=140)
    st.altair_chart(area, use_container_width=True)
with r4_c3:
    st.markdown("<p style='font-size:12px; color:#94a3b8; font-weight:bold;'>📐 CAPACITY PRIORITIZATION PYRAMID</p>", unsafe_allow_html=True)
    pyr = alt.Chart(pd.DataFrame({"Layer": ["Tier 1", "Tier 2", "Tier 3", "Tier 4"], "Width": [10, 25, 45, 70]})).mark_bar(align="center").encode(x=alt.X('Width:Q', axis=None), y=alt.Y('Layer:N', sort='descending', axis=None), color=alt.Color('Layer:N', scale=alt.Scale(scheme='cool'), legend=None)).properties(height=140)
    st.altair_chart(pyr, use_container_width=True)
