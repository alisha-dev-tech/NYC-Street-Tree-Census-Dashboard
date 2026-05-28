import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light Brown & Sage Green Theme
st.markdown("""
<style>
:root {
    --light-brown: #D4A574;
    --sage-green: #9CAF88;
    --dark-brown: #8B7355;
    --bg-color: #FAF8;
}
[data-testid="stSidebar"] {
    background-color: #F5F1ED;
}
.main {
    background-color: #FAF8;
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
}
.stTextInput>div>div>input,.stSelectbox>div>div>select,.stMultiSelect>div>div>select {
    border: 2px solid #D4A574;
    border-radius: 6px;
}
.stSlider>div>div>div {
    background-color: #9CAF88;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #9CAF88!important;
    color: white!important;
    border-radius: 4px;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {
    fill: white!important;
}
</style>
""", unsafe_allow_html=True)

# Load data - Google Drive se
@st.cache_data
def load_data():
    try:
        url = "https://drive.google.com/uc?export=download&id=1OkstsN_r1glXGIAbPW1LkZ2L7SnB6u6A"
        df = pd.read_csv(url, on_bad_lines='skip', engine='python')
    except Exception as e:
        st.error(f"CSV load nahi ho rahi: {e}")
        st.stop()
    df['created_at'] = pd.to_datetime(df['created_at'], format='%m/%d/%Y', errors='coerce')
    return df

df = load_data()

# Title
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🌳 NYC Street Tree Census Dashboard")
    st.markdown("**Exploratory Data Analysis - 2015 Street Tree Census Data**")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/128/2998/2998432.png", width=60)
st.markdown("---")

# SIDEBAR FILTERS
st.sidebar.markdown("## 🔍 Filter Controls")
boroughs = sorted(df['borough'].dropna().unique())
health_status = sorted(df['health'].dropna().unique())
top_species = df['spc_common'].value_counts().head(10).index.tolist()
user_types = sorted(df['user_type'].dropna().unique())
date_min = df['created_at'].min().date()
date_max = df['created_at'].max().date()

selected_dates = st.sidebar.date_input("Select date range:", value=(date_min, date_max), min_value=date_min, max_value=date_max)
selected_boroughs = st.sidebar.multiselect("Select Boroughs:", options=boroughs, default=boroughs)
selected_health = st.sidebar.multiselect("Select Health Status:", options=health_status, default=health_status)
selected_species = st.sidebar.multiselect("Select Species:", options=top_species, default=top_species)
selected_user_type = st.sidebar.multiselect("Select User Type:", options=user_types, default=user_types)

dbh_range = st.sidebar.slider("Diameter at Breast Height (inches):", min_value=int(df['tree_dbh'].min()), max_value=int(df['tree_dbh'].max()), value=(int(df['tree_dbh'].min()), int(df['tree_dbh'].quantile(0.95))))
search_keyword = st.sidebar.text_input("Search by address:", placeholder="e.g., 'BROADWAY'")

if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.rerun()

# Apply filters
filtered_df = df.copy()
if len(selected_dates) == 2:
    filtered_df = filtered_df[(filtered_df['created_at'].dt.date >= selected_dates[0]) & (filtered_df['created_at'].dt.date <= selected_dates[1])]
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

# KPI CARDS
st.markdown("### 📊 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric("Total Trees", f"{len(filtered_df):,}")
with kpi_col2:
    st.metric("Avg Diameter", f"{filtered_df['tree_dbh'].mean():.1f}\"")
with kpi_col3:
    healthy_pct = (len(filtered_df[filtered_df['health'] == 'Good']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Healthy Trees", f"{healthy_pct:.1f}%")
with kpi_col4:
    alive_pct = (len(filtered_df[filtered_df['status'] == 'Alive']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Alive Trees", f"{alive_pct:.1f}%")
with kpi_col5:
    st.metric("Species Count", f"{filtered_df['spc_common'].nunique()}")

st.markdown("---")
st.markdown("### 📈 Data Visualizations")

def create_all_charts(data):
    charts = {}
    borough_counts = data['borough'].value_counts().head(5)
    charts['pie'] = px.pie(values=borough_counts.values, names=borough_counts.index, title='Trees by Borough', color_discrete_sequence=px.colors.sequential.Greens)
    charts['histogram'] = px.histogram(data, x='tree_dbh', nbins=30, title='Tree Diameter Distribution', color_discrete_sequence=['#D4A574'])
    time_data = data.groupby(data['created_at'].dt.date).size().cumsum().reset_index()
    time_data.columns = ['date', 'count']
    charts['line'] = px.line(time_data, x='date', y='count', title='Cumulative Tree Count Over Time', color_discrete_sequence=['#9CAF88'])
    species_counts = data['spc_common'].value_counts().head(10)
    charts['bar'] = px.bar(x=species_counts.values, y=species_counts.index, orientation='h', title='Top 10 Tree Species', color_discrete_sequence=['#D4A574'])
    charts['scatter'] = px.scatter(data.sample(min(1000, len(data))), x='tree_dbh', color='health', title='DBH vs Health Status')
    charts['box'] = px.box(data, x='borough', y='tree_dbh', title='DBH Distribution by Borough', color_discrete_sequence=px.colors.sequential.Greens)
    num_cols = ['tree_dbh', 'x_sp', 'y_sp']
    corr_data = data[num_cols].corr()
    charts['heatmap'] = px.imshow(corr_data, text_auto=True, title='Correlation Heatmap', color_continuous_scale='Greens')
    health_time = data.groupby([data['created_at'].dt.date, 'health']).size().unstack(fill_value=0).cumsum()
    charts['area'] = px.area(health_time, title='Cumulative Health Status Over Time')
    health_counts = data['health'].value_counts()
    charts['count'] = px.bar(x=health_counts.index, y=health_counts.values, title='Tree Health Count', color_discrete_sequence=['#9CAF88'])
    charts['violin'] = px.violin(data, x='health', y='tree_dbh', title='DBH Distribution by Health')
    return charts

all_charts = create_all_charts(filtered_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(all_charts['pie'], use_container_width=True)
with col2:
    st.plotly_chart(all_charts['histogram'], use_container_width=True)
with col3:
    st.plotly_chart(all_charts['line'], use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(all_charts['bar'], use_container_width=True)
with col2:
    st.plotly_chart(all_charts['scatter'], use_container_width=True)
with col3:
    st.plotly_chart(all_charts['box'], use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(all_charts['heatmap'], use_container_width=True)
with col2:
    st.plotly_chart(all_charts['area'], use_container_width=True)
with col3:
    st.plotly_chart(all_charts['count'], use_container_width=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.plotly_chart(all_charts['violin'], use_container_width=True)

st.markdown("---")
st.markdown("### 📥 Data Export")
export_col1, export_col2 = st.columns(2)
with export_col1:
    csv_data = filtered_df.to_csv(index=False)
    st.download_button("📥 Download Filtered Data (CSV)", data=csv_data, file_name=f"tree_census_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")

st.markdown(f"""
**Dashboard Info**
- **Total Records**: {len(df):,} trees
- **Filtered Records**: {len(filtered_df):,} trees
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
""")