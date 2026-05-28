import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from filters import apply_filters, get_filter_widgets
from charts import create_all_charts, create_kpi_cards
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Light Brown & Sage Green Theme
st.markdown("""
<style>
/* Main color scheme */
:root {
    --light-brown: #D4A574;
    --sage-green: #9CAF88;
    --dark-brown: #8B7355;
    --light-sage: #C2D4C8;
    --bg-color: #FAF8;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #F5F1ED;
}

/* Main content background */
.main {
    background-color: #FAF8;
}

/* Headers */
h1, h2, h3 {
    color: #6B5344;
    font-weight: 700;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #FFFBF7;
    border-left: 4px solid #9CAF88;
    padding: 20px;
    border-radius: 8px;
}

/* Button styling */
.stButton>button {
    background-color: #9CAF88;
    color: white;
    border-radius: 6px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
    transition: all 0.3s;
}

.stButton>button:hover {
    background-color: #7a9370;
    box-shadow: 0 4px 12px rgba(156, 175, 136, 0.3);
}

/* Text input and selectors */
.stTextInput>div>div>input,
.stSelectbox>div>div>select,
.stMultiSelect>div>div>select {
    border: 2px solid #D4A574;
    border-radius: 6px;
}

/* Slider styling */
.stSlider>div>div>div {
    background-color: #9CAF88;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #E8DCC8;
    color: #6B5344;
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

# Title and Description
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

# Get all unique values for filters
boroughs = sorted(df['borough'].dropna().unique())
health_status = sorted(df['health'].dropna().unique())
tree_species = sorted(df['spc_common'].dropna().unique())
user_types = sorted(df['user_type'].dropna().unique())

# Date Range Filter
st.sidebar.markdown("### 📅 Date Range")
date_min = df['created_at'].min().date()
date_max = df['created_at'].max().date()
selected_dates = st.sidebar.date_input(
    "Select date range:",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
    key="date_range"
)

# Category Filters
st.sidebar.markdown("### 🏘️ Borough Selection")
selected_boroughs = st.sidebar.multiselect(
    "Select Boroughs:",
    options=boroughs,
    default=boroughs,
    key="borough_filter"
)

st.sidebar.markdown("### 💚 Tree Health Status")
selected_health = st.sidebar.multiselect(
    "Select Health Status:",
    options=health_status,
    default=health_status,
    key="health_filter"
)

st.sidebar.markdown("### 🌱 Tree Species (Top 10)")
top_species = df['spc_common'].value_counts().head(10).index.tolist()
selected_species = st.sidebar.multiselect(
    "Select Species:",
    options=top_species,
    default=top_species,
    key="species_filter"
)

st.sidebar.markdown("### 👤 User Type")
selected_user_type = st.sidebar.multiselect(
    "Select User Type:",
    options=user_types,
    default=user_types,
    key="user_type_filter"
)

# Numerical Range Slider
st.sidebar.markdown("### 📏 Tree Diameter (DBH)")
dbh_range = st.sidebar.slider(
    "Diameter at Breast Height (inches):",
    min_value=int(df['tree_dbh'].min()),
    max_value=int(df['tree_dbh'].max()),
    value=(int(df['tree_dbh'].min()), int(df['tree_dbh'].quantile(0.95))),
    step=1,
    key="dbh_slider"
)

# Search/Text Filter
st.sidebar.markdown("### 🔎 Search Address")
search_keyword = st.sidebar.text_input(
    "Search by address (optional):",
    placeholder="e.g., 'BROADWAY'",
    key="address_search"
)

# Reset Filters Button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# Apply all filters
filtered_df = df.copy()

# Date range filter
if len(selected_dates) == 2:
    filtered_df = filtered_df[
        (filtered_df['created_at'].dt.date >= selected_dates[0]) &
        (filtered_df['created_at'].dt.date <= selected_dates[1])
    ]

# Borough filter
if selected_boroughs:
    filtered_df = filtered_df[filtered_df['borough'].isin(selected_boroughs)]

# Health filter
if selected_health:
    filtered_df = filtered_df[filtered_df['health'].isin(selected_health)]

# Species filter
if selected_species:
    filtered_df = filtered_df[filtered_df['spc_common'].isin(selected_species)]

# User type filter
if selected_user_type:
    filtered_df = filtered_df[filtered_df['user_type'].isin(selected_user_type)]

# DBH range filter
filtered_df = filtered_df[
    (filtered_df['tree_dbh'] >= dbh_range[0]) &
    (filtered_df['tree_dbh'] <= dbh_range[1])
]

# Address search filter
if search_keyword:
    filtered_df = filtered_df[filtered_df['address'].str.contains(search_keyword.upper(), na=False)]

# KPI CARDS
st.markdown("### 📊 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric(
        "Total Trees",
        f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df)}" if len(filtered_df)!= len(df) else None,
        delta_color="inverse"
    )

with kpi_col2:
    avg_dbh = filtered_df['tree_dbh'].mean()
    st.metric(
        "Avg Diameter",
        f"{avg_dbh:.1f}\"" if not np.isnan(avg_dbh) else "N/A",
        delta=f"{(avg_dbh - df['tree_dbh'].mean()):.1f}\"" if not np.isnan(avg_dbh) and not np.isnan(df['tree_dbh'].mean()) else None
    )

with kpi_col3:
    healthy_pct = (len(filtered_df[filtered_df['health'] == 'Good']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        "Healthy Trees",
        f"{healthy_pct:.1f}%",
        delta=f"{len(filtered_df[filtered_df['health'] == 'Good']):,} trees"
    )

with kpi_col4:
    alive_pct = (len(filtered_df[filtered_df['status'] == 'Alive']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        "Alive Trees",
        f"{alive_pct:.1f}%",
        delta=f"{len(filtered_df[filtered_df['status'] == 'Alive']):,} trees"
    )

with kpi_col5:
    unique_species = filtered_df['spc_common'].nunique()
    st.metric(
        "Species Count",
        f"{unique_species}",
        delta=f"{unique_species - df['spc_common'].nunique()}" if unique_species!= df['spc_common'].nunique() else None,
        delta_color="inverse"
    )

st.markdown("---")

# CHARTS SECTION
st.markdown("### 📈 Data Visualizations")

# Create all charts with consistent dimensions
all_charts = create_all_charts(filtered_df)

# Chart descriptions
chart_descriptions = {
    'pie': '**Pie Chart**: Shows the proportional distribution of trees across different boroughs.',
    'histogram': '**Histogram**: Displays the frequency distribution of tree diameter (DBH).',
    'line': '**Line Chart**: Illustrates trends in tree planting over time.',
    'bar': '**Bar Chart**: Compares tree counts across the top 10 tree species.',
    'scatter': '**Scatter Plot**: Visualizes relationship between tree diameter and health status.',
    'box': '**Box Plot**: Shows distribution of tree diameter by borough.',
    'heatmap': '**Heatmap**: Visualizes correlation matrix between numerical features.',
    'area': '**Area Chart**: Shows cumulative trends in tree health status over time.',
    'count': '**Count Plot**: Displays frequency counts of tree health conditions.',
    'violin': '**Violin Plot**: Shows probability density distribution of tree diameter by health status.'
}

# Row 1: Pie, Histogram, Line
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(chart_descriptions['pie'])
    st.plotly_chart(all_charts['pie'], use_container_width=True, height=400)
with col2:
    st.markdown(chart_descriptions['histogram'])
    st.plotly_chart(all_charts['histogram'], use_container_width=True, height=400)
with col3:
    st.markdown(chart_descriptions['line'])
    st.plotly_chart(all_charts['line'], use_container_width=True, height=400)

# Row 2: Bar, Scatter, Box
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(chart_descriptions['bar'])
    st.plotly_chart(all_charts['bar'], use_container_width=True, height=400)
with col2:
    st.markdown(chart_descriptions['scatter'])
    st.plotly_chart(all_charts['scatter'], use_container_width=True, height=400)
with col3:
    st.markdown(chart_descriptions['box'])
    st.plotly_chart(all_charts['box'], use_container_width=True, height=400)

# Row 3: Heatmap, Area, Count
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(chart_descriptions['heatmap'])
    st.plotly_chart(all_charts['heatmap'], use_container_width=True, height=400)
with col2:
    st.markdown(chart_descriptions['area'])
    st.plotly_chart(all_charts['area'], use_container_width=True, height=400)
with col3:
    st.markdown(chart_descriptions['count'])
    st.plotly_chart(all_charts['count'], use_container_width=True, height=400)

# Row 4: Violin Plot
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("")
with col2:
    st.markdown(chart_descriptions['violin'])
    st.plotly_chart(all_charts['violin'], use_container_width=True, height=400)
with col3:
    st.markdown("")

st.markdown("---")

# Data Export Section
st.markdown("### 📥 Data Export")
export_col1, export_col2 = st.columns(2)

with export_col1:
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv_data,
        file_name=f"tree_census_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with export_col2:
    summary_stats = {
        'Total Records': len(filtered_df),
        'Average DBH': round(filtered_df['tree_dbh'].mean(), 2) if len(filtered_df) > 0 else 0,
        'Median DBH': round(filtered_df['tree_dbh'].median(), 2) if len(filtered_df) > 0 else 0,
        'Healthy %': round((len(filtered_df[filtered_df['health'] == 'Good']) / len(filtered_df) * 100), 2) if len(filtered_df) > 0 else 0,
        'Alive %': round((len(filtered_df[filtered_df['status'] == 'Alive']) / len(filtered_df) * 100), 2) if len(filtered_df) > 0 else 0,
    }
    summary_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
    csv_summary = summary_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Summary Statistics",
        data=csv_summary,
        file_name=f"tree_census_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("""
**Dashboard Information**
- **Dataset**: 2015 NYC Street Tree Census
- **Total Records**: {:,} trees
- **Filtered Records**: {:,} trees
- **Analysis Date**: {}
- **Chart Types**: 10 (Pie, Histogram, Line, Bar, Scatter, Box, Heatmap, Area, Count, Violin)
- **Interactive Filters**: Date Range, Borough, Health Status, Species, User Type, DBH Range, Address Search
""".format(len(df), len(filtered_df), datetime.now().strftime('%Y-%m-%d %H:%M')))