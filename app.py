import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import io
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Light Brown & Sage Green Theme + Alignment Fix
st.markdown("""
<style>
:root {
    --light-brown: #D4A574;
    --sage-green: #9CAF88;
    --dark-brown: #8B7355;
    --light-sage: #C2D4C8;
    --bg-color: #FAF8;
}
[data-testid="stSidebar"] {
    background-color: #F5F1ED;
}
.main {
    background-color: #FAF8;
    padding: 0!important;
    margin: 0!important;
}
.block-container {
    padding: 1.5rem 2rem!important;
    max-width: 100%!important;
}
h1, h2, h3 {
    color: #6B5344;
    font-weight: 700;
}
[data-testid="metric-container"] {
    background-color: #FFFBF7;
    border-left: 4px solid #9CAF88;
    padding: 20px;
    border-radius: 8px;
}
.stButton>button {
    background-color: #9CAF88;
    color: white;
    border-radius: 6px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background-color: #7a9370;
    box-shadow: 0 4px 12px rgba(156, 175, 136, 0.3);
}
.stTextInput>div>div>input,
.stSelectbox>div>div>select,
.stMultiSelect>div>div>select {
    border: 2px solid #D4A574;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/2015_Street_Tree_Census_-_Tree_Data.csv')
    df['created_at'] = pd.to_datetime(df['created_at'], format='%m/%d/%Y', errors='coerce')
    return df

df = load_data()

# Dummy functions to replace missing filters.py and charts.py
def apply_filters(df):
    return df

def get_filter_widgets():
    pass

def create_kpi_cards(df):
    pass

def create_all_charts(df):
    pie = px.pie(df, names='borough', title='Trees by Borough', hole=0.4)
    hist = px.histogram(df, x='tree_dbh', nbins=30, title='Tree Diameter Distribution')
    df_sorted = df.sort_values('created_at')
    df_sorted['cumsum'] = range(1, len(df_sorted) + 1)
    line = px.line(df_sorted, x='created_at', y='cumsum', title='Cumulative Trees Over Time')
    top_species = df['spc_common'].value_counts().head(10)
    bar = px.bar(x=top_species.values, y=top_species.index, orientation='h', title='Top 10 Species')
    scatter = px.scatter(df, x='tree_dbh', y='health', title='DBH vs Health', opacity=0.3)
    box = px.box(df, x='borough', y='tree_dbh', title='DBH Distribution by Borough')
    heatmap = px.imshow(df[['tree_dbh']].corr(), title='Correlation Heatmap')
    area_data = df.groupby([df['created_at'].dt.date, 'health']).size().reset_index(name='count')
    area = px.area(area_data, x='created_at', y='count', color='health', title='Health Status Over Time')
    count = px.histogram(df, x='health', title='Tree Health Count')
    violin = px.violin(df, x='health', y='tree_dbh', title='DBH Distribution by Health')
    return {'pie': pie, 'histogram': hist, 'line': line, 'bar': bar, 'scatter': scatter,
            'box': box, 'heatmap': heatmap, 'area': area, 'count': count, 'violin': violin}

def download_chart(chart, filename):
    img_bytes = chart.to_image(format="png", scale=2)
    st.download_button(
        label="📥 Download",
        data=img_bytes,
        file_name=f"{filename}.png",
        mime="image/png",
        key=f"dl_{filename}"
    )

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🌳 NYC Street Tree Census Dashboard")
    st.markdown("**Exploratory Data Analysis - 2015 Street Tree Census Data**")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/128/2998/2998432.png", width=60)

st.markdown("---")
st.markdown("""
### Dashboard Overview
This interactive dashboard presents a comprehensive analysis of the **2015 NYC Street Tree Census** data.
Explore tree health, species distribution, geographic patterns, and maintenance records across NYC's five boroughs.
Each visualization is **filterable in real-time** and **downloadable** for further analysis.
""")
st.markdown("---")

# SIDEBAR FILTERS
st.sidebar.markdown("## 🔍 Filter Controls")
st.sidebar.markdown("**Adjust filters below to update all charts simultaneously**")

boroughs = sorted(df['borough'].dropna().unique())
health_status = sorted(df['health'].dropna().unique())
tree_species = sorted(df['spc_common'].dropna().unique())
user_types = sorted(df['user_type'].dropna().unique())

st.sidebar.markdown("### 📅 Date Range")
date_min = df['created_at'].min().date()
date_max = df['created_at'].max().date()
selected_dates = st.sidebar.date_input("Select date range:", value=(date_min, date_max),
                                       min_value=date_min, max_value=date_max)

st.sidebar.markdown("### 🏘️ Borough Selection")
selected_boroughs = st.sidebar.multiselect("Select Boroughs:", options=boroughs, default=boroughs)

st.sidebar.markdown("### 💚 Tree Health Status")
selected_health = st.sidebar.multiselect("Select Health Status:", options=health_status, default=health_status)

st.sidebar.markdown("### 🌱 Tree Species (Top 10)")
top_species_list = df['spc_common'].value_counts().head(10).index.tolist()
selected_species = st.sidebar.multiselect("Select Species:", options=top_species_list, default=top_species_list)

st.sidebar.markdown("### 👤 User Type")
selected_user_type = st.sidebar.multiselect("Select User Type:", options=user_types, default=user_types)

st.sidebar.markdown("### 📏 Tree Diameter (DBH)")
dbh_range = st.sidebar.slider("Diameter at Breast Height (inches):",
                              min_value=int(df['tree_dbh'].min()),
                              max_value=int(df['tree_dbh'].max()),
                              value=(int(df['tree_dbh'].min()), int(df['tree_dbh'].quantile(0.95))),
                              step=1)

st.sidebar.markdown("### 🔎 Search Address")
search_keyword = st.sidebar.text_input("Search by address (optional):", placeholder="e.g., 'BROADWAY'")

if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Apply filters
filtered_df = df.copy()
if len(selected_dates) == 2:
    filtered_df = filtered_df[(filtered_df['created_at'].dt.date >= selected_dates[0]) &
                              (filtered_df['created_at'].dt.date <= selected_dates[1])]
if selected_boroughs:
    filtered_df = filtered_df[filtered_df['borough'].isin(selected_boroughs)]
if selected_health:
    filtered_df = filtered_df[filtered_df['health'].isin(selected_health)]
if selected_species:
    filtered_df = filtered_df[filtered_df['spc_common'].isin(selected_species)]
if selected_user_type:
    filtered_df = filtered_df[filtered_df['user_type'].isin(selected_user_type)]
filtered_df = filtered_df[(filtered_df['tree_dbh'] >= dbh_range[0]) & (filtered_df['tree_dbh'] <= dbh_range[1])]
if search_keyword:
    filtered_df = filtered_df[filtered_df['address'].str.contains(search_keyword.upper(), na=False)]

st.markdown(f"### 📊 Showing {len(filtered_df):,} trees after filtering")

# KPI Cards
st.markdown("## 📈 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Trees", f"{len(filtered_df):,}")
with col2:
    st.metric("Unique Species", f"{filtered_df['spc_common'].nunique()}")
with col3:
    st.metric("Avg DBH", f"{filtered_df['tree_dbh'].mean():.1f} in")
with col4:
    healthy_pct = (filtered_df['health'] == 'Good').mean() * 100
    st.metric("Healthy Trees", f"{healthy_pct:.1f}%")
with col5:
    st.metric("Boroughs Covered", f"{filtered_df['borough'].nunique()}")

st.markdown("---")

# Generate charts
charts = create_all_charts(filtered_df)

# Chart Grid
st.markdown("## 📊 Interactive Visualizations")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts['pie'], use_container_width=True, key="pie_chart")
    download_chart(charts['pie'], "trees_by_borough")
with col2:
    st.plotly_chart(charts['histogram'], use_container_width=True, key="hist_chart")
    download_chart(charts['histogram'], "dbh_distribution")

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(charts['line'], use_container_width=True, key="line_chart")
    download_chart(charts['line'], "cumulative_trees")
with col4:
    st.plotly_chart(charts['bar'], use_container_width=True, key="bar_chart")
    download_chart(charts['bar'], "top_species")

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(charts['scatter'], use_container_width=True, key="scatter_chart")
    download_chart(charts['scatter'], "dbh_vs_health")
with col6:
    st.plotly_chart(charts['box'], use_container_width=True, key="box_chart")
    download_chart(charts['box'], "dbh_by_borough")

col7, col8 = st.columns(2)
with col7:
    st.plotly_chart(charts['heatmap'], use_container_width=True, key="heatmap_chart")
    download_chart(charts['heatmap'], "correlation")
with col8:
    st.plotly_chart(charts['area'], use_container_width=True, key="area_chart")
    download_chart(charts['area'], "health_over_time")

col9, col10 = st.columns(2)
with col9:
    st.plotly_chart(charts['count'], use_container_width=True, key="count_chart")
    download_chart(charts['count'], "health_count")
with col10:
    st.plotly_chart(charts['violin'], use_container_width=True, key="violin_chart")
    download_chart(charts['violin'], "dbh_by_health")

st.markdown("---")
st.markdown("### 📋 Raw Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data as CSV", csv, "nyc_trees_filtered.csv", "text/csv")

st.markdown("---")
st.markdown("*Dashboard built with Streamlit & Plotly | NYC Open Data*")