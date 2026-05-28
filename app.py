import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stSidebar {background-color: #e8f5e9;}
    h1 {color: #2e7d32; font-weight: bold;}
    h2, h3 {color: #388e3c;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; 
               box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .stButton>button {background-color: #4caf50; color: white; border-radius: 5px;}
    .stButton>button:hover {background-color: #45a049;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        url = "https://drive.google.com/uc?export=download&id=1OkstsN_r1glXGIAbPW1LkZ2L7SnB6u6A"
        df = pd.read_csv(url, on_bad_lines='skip', engine='python')
    except Exception as e:
        st.error(f"CSV load nahi ho rahi: {e}")
        st.stop()
    
    # Date column handle karo
    if 'Created_Date' in df.columns:
        df['created_at'] = pd.to_datetime(df['Created_Date'], errors='coerce')
    elif 'created_date' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_date'], errors='coerce')
    elif 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    else:
        st.error(f"Date column nahi mili. Available columns: {list(df.columns)}")
        st.stop()
    
    return df

# Load data
with st.spinner('Data load ho raha hai...'):
    df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
boroughs = st.sidebar.multiselect("Borough Select Karo", options=df['borough'].unique(), default=df['borough'].unique())
health_options = st.sidebar.multiselect("Tree Health", options=df['health'].dropna().unique(), default=df['health'].dropna().unique())
species_list = st.sidebar.multiselect("Species", options=df['spc_common'].dropna().unique()[:20], default=df['spc_common'].dropna().unique()[:10])

# Apply filters
filtered_df = df[
    (df['borough'].isin(boroughs)) & 
    (df['health'].isin(health_options)) & 
    (df['spc_common'].isin(species_list))
]

# Title
st.title("NYC Street Tree Census Dashboard")
st.markdown("New York City ke street trees ka interactive analysis")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Trees", f"{len(filtered_df):,}")
with col2:
    st.metric("Unique Species", filtered_df['spc_common'].nunique())
with col3:
    st.metric("Boroughs", filtered_df['borough'].nunique())
with col4:
    healthy_pct = (filtered_df['health'] == 'Good').mean() * 100
    st.metric("Healthy Trees %", f"{healthy_pct:.1f}%")

# Charts
st.subheader("Species Distribution")
species_count = filtered_df['spc_common'].value_counts().head(10)
fig_species = px.bar(
    species_count,
    x=species_count.values,
    y=species_count.index,
    orientation='h',
    labels={'x': 'Tree Count', 'y': 'Species'},
    color=species_count.values,
    color_continuous_scale='Greens'
)
fig_species.update_layout(height=400)
st.plotly_chart(fig_species, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Health Status")
    health_count = filtered_df['health'].value_counts()
    fig_health = px.pie(
        values=health_count.values,
        names=health_count.index,
        color_discrete_sequence=px.colors.sequential.Greens
    )
    st.plotly_chart(fig_health, use_container_width=True)

with col2:
    st.subheader("Trees by Borough")
    borough_count = filtered_df['borough'].value_counts()
    fig_borough = px.bar(
        x=borough_count.index,
        y=borough_count.values,
        labels={'x': 'Borough', 'y': 'Tree Count'},
        color=borough_count.values,
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig_borough, use_container_width=True)

# Map
st.subheader("Tree Locations Map")
if len(filtered_df) > 0:
    sample_df = filtered_df.sample(min(1000, len(filtered_df)))
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
    
    for idx, row in sample_df.iterrows():
        if pd.notna(row['x_sp']) and pd.notna(row['y_sp']):
            folium.CircleMarker(
                location=[row['y_sp'], row['x_sp']],
                radius=3,
                popup=f"{row['spc_common']} - {row['health']}",
                color='green',
                fill=True
            ).add_to(m)
    
    folium_static(m, width=700, height=500)

# Data table
st.subheader("Sample Data")
st.dataframe(filtered_df[['spc_common', 'borough', 'health', 'created_at']].head(100))

st.markdown("---")
st.markdown("**Data Source:** NYC Open Data - Street Tree Census 2015")