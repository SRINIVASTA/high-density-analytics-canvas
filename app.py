import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="High-Density Neon Infographic",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED STYLESHEET INJECTION ---
st.markdown("""
    <style>
        .stApp { background-color: #16182c !important; color: #ffffff !important; }
        h1, h2, h3, h4, h5, h6, p, span, label { color: #ffffff !important; font-family: monospace, sans-serif; }
        .stMarkdown { margin-bottom: 0px !important; }
        
        /* Pictogram Silhouette Array Emulation Style */
        .icon-grid { display: flex; gap: 8px; font-size: 24px; margin-bottom: 15px; }
        .icon-active { color: #3296ff; }
        .icon-active-pink { color: #f25c8c; }
        .icon-muted { color: #2c2f4d; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ALTAIR COLOR REGISTRATION ---
def apply_neon_theme():
    return {
        'config': {
            'background': '#16182c',
            'view': {'stroke': 'transparent'},
            'axis': {
                'domainColor': '#383b5c', 'gridColor': '#23253f',
                'labelColor': '#9ba1c6', 'titleColor': '#ffffff'
            },
            'range': {'category': ['#f25c8c', '#3296ff', '#bf62fc', '#1ad492', '#ffbc42']}
        }
    }
alt.themes.register('neon_theme', apply_neon_theme)
alt.themes.enable('neon_theme')

# --- 4. TOP ROW: METRIC RINGS & HUMAN ARRAYS ---
st.title("⚡ Ultra High-Density Diagnostic Canvas")
st.markdown("---")

top_col1, top_col2, top_col3 = st.columns([1.5, 1.5, 2])

with top_col1:
    st.markdown("##### 🎯 TARGET THRESHOLDS")
    ring_sub1, ring_sub2 = st.columns(2)
    
    def make_ring(val, color):
        df = pd.DataFrame({"v": [val, 100-val], "c": ["A", "B"]})
        c = alt.Chart(df).mark_arc(innerRadius=32, outerRadius=45).encode(
            theta="v:Q", color=alt.Color("c:N", scale=alt.Scale(domain=["A","B"], range=[color, "#23253f"]), legend=None)
        ).properties(width=100, height=100)
        t = alt.Chart(pd.DataFrame({"t": [f"{val}%"]})).mark_text(align='center', fontSize=14, fontWeight='bold', color='#fff').encode(text='t:N')
        return c + t

    with ring_sub1:
        st.altair_chart(make_ring(80, "#f25c8c"))
        st.altair_chart(make_ring(50, "#bf62fc"))
    with ring_sub2:
        st.altair_chart(make_ring(75, "#3296ff"))
        st.altair_chart(make_ring(25, "#1ad492"))

with top_col2:
    st.markdown("##### 👥 DEMOGRAPHIC DENSITY (SILHOUETTE ARRAYS)")
    # Replicating the human stick figure charts using icon characters & flex grids
    st.caption("Segment Alpha (Male Allocation Index)")
    st.markdown("<div class='icon-grid'>" + "".join(["<span class='icon-active'>🧍</span>"]*7 + ["<span class='icon-muted'>🧍</span>"]*3) + "</div>", unsafe_allow_html=True)
    
    st.caption("Segment Beta (Female Allocation Index)")
    st.markdown("<div class='icon-grid'>" + "".join(["<span class='icon-active-pink'>🧍‍♀️</span>"]*4 + ["<span class='icon-muted'>🧍‍♀️</span>"]*6) + "</div>", unsafe_allow_html=True)

with top_col3:
    st.markdown("##### 💠 POLAR RADAR GRAPH (HEXAGON OVERLAY)")
    # Building a custom structural polygon layer matching the geometric purple web shape
    hex_data = pd.DataFrame({
        'x': [0, 0.86, 0.86, 0, -0.86, -0.86, 0],
        'y': [1, 0.5, -0.5, -1, -0.5, 0.5, 1],
        'order': [1, 2, 3, 4, 5, 6, 7]
    })
    hex_chart = alt.Chart(hex_data).mark_line(color="#bf62fc", strokeWidth=2).encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-1.5, 1.5]), axis=None),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.5, 1.5]), axis=None),
        order='order:O'
    ).properties(width=180, height=180)
    
    fill_chart = alt.Chart(hex_data).mark_area(color="#bf62fc", opacity=0.15).encode(x='x:Q', y='y:Q', order='order:O')
    st.altair_chart(hex_chart + fill_chart, use_container_width=True)

st.markdown("---")

# --- 5. MIDDLE ROW: DISTRIBUTIONS & MATRIX SCATTER PLOTS ---
mid_col1, mid_col2, mid_col3 = st.columns(3)

with mid_col1:
    st.markdown("##### 🍩 PIE CUT VARIANT")
    pie_df = pd.DataFrame({"cat": ["ONE", "TWO", "THREE", "FOUR"], "val": [40, 30, 15, 15]})
    pie = alt.Chart(pie_df).mark_arc(innerRadius=25).encode(
        theta="val:Q", color="cat:N"
    ).properties(height=180)
    st.altair_chart(pie, use_container_width=True)

with mid_col2:
    st.markdown("##### 📊 SCATTER SCALAR VARIANCE")
    # Generates the grid dot chart found in the top-center of the reference image
    np.random.seed(10)
    scatter_df = pd.DataFrame({'X-Coord': np.random.randint(10, 70, 15), 'Y-Coord': np.random.randint(5, 45, 15)})
    scatter = alt.Chart(scatter_df).mark_circle(size=70, color="#f25c8c").encode(
        x=alt.X('X-Coord:Q', scale=alt.Scale(domain=[0, 70])),
        y=alt.Y('Y-Coord:Q', scale=alt.Scale(domain=[0, 50]))
    ).properties(height=180)
    st.altair_chart(scatter, use_container_width=True)

with mid_col3:
    st.markdown("##### 📊 BAR VALUE SCALE")
    bar_df = pd.DataFrame({"M": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "V": [1, 2, 3, 4, 5, 6]})
    bars = alt.Chart(bar_df).mark_bar(size=14, color="#f25c8c").encode(
        x=alt.X("M:N", sort=None, title=None), y=alt.Y("V:Q", title=None)
    ).properties(height=180)
    st.altair_chart(bars, use_container_width=True)

st.markdown("---")

# --- 6. BOTTOM ROW: MULTI-LAYER TRAJECTORY CORNER ---
bot_col1, bot_col2 = st.columns([2, 1])

with bot_col1:
    st.markdown("##### 📈 SPLINE TIMELINE HARMONICS")
    # The multi-layered smooth wave curve at the center bottom
    time_points = np.linspace(0, 10, 30)
    wave_df = pd.DataFrame({
        'Timeline': np.tile(time_points, 2),
        'Amplitude': np.concatenate([np.sin(time_points)*15 + 25, np.cos(time_points)*10 + 20]),
        'Group': np.concatenate([["Metric A"]*30, ["Metric B"]*30])
    })
    wave_chart = alt.Chart(wave_df).mark_area(interpolate='monotone', opacity=0.2).encode(
        x=alt.X('Timeline:Q', axis=None),
        y=alt.Y('Amplitude:Q', axis=None),
        color='Group:N'
    ).properties(height=160)
    st.altair_chart(wave_chart, use_container_width=True)

with bot_col2:
    st.markdown("##### 📐 DISTRIBUTION SEGMENT TRIANGLE")
    # Creates the stylized triangle pyramid layers found on the bottom right
    pyramid_df = pd.DataFrame({"Layer": ["Tier 1", "Tier 2", "Tier 3"], "Size": [10, 20, 30]})
    pyramid = alt.Chart(pyramid_df).mark_bar().encode(
        x=alt.X("Size:Q", axis=None),
        y=alt.Y("Layer:N", sort="descending", title=None),
        color=alt.Color("Layer:N", scale=alt.Scale(scheme="magma"), legend=None)
    ).properties(height=160)
    st.altair_chart(pyramid, use_container_width=True)
