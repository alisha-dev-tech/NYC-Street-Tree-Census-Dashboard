import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING - LIGHT BROWN & SAGE GREEN PROFESSIONAL THEME
# ============================================================================
st.markdown("""
<style>
    /* Color Variables */
    :root {
        --light-brown: #D4A574;
        --sage-green: #9CAF88;
        --dark-brown: #8B7355;
        --light-sage: #C2D4C8;
        --bg-color: #FAFAF8;
        --card-bg: #FFFBF7;
    }
    
    /* Main Background */
    .main {
        background-color: #FAFAF8;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #F5F1ED 0%, #E8DCC8 100%);
        padding-top: 20px;
    }
    
    /* Headers - Professional Look */
    h1, h2, h3 {
        color: #6B5344;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    h1 {
        border-bottom: 3px solid #9CAF88;
        padding-bottom: 10px;
    }
    
    /* Metric Cards - KPI Section */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFBF7 0%, #FFF8F3 100%);
        border-left: 5px solid #9CAF88;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(156, 175, 136, 0.15);
    }
    
    /* Buttons - Sage Green Theme */
    .stButton>button {
        background-color: #9CAF88;
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(156, 175, 136, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #7a9370;
        box-shadow: 0 4px 12px rgba(156, 175, 136, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input Fields - Light Brown Border */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stMultiSelect>div>div>select,
    .stDateInput>div>div>input {
        border: 2px solid #D4A574 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #9CAF88 !important;
        box-shadow: 0 0 8px rgba(156, 175, 136, 0.3) !important;
    }
    
    /* Slider Styling */
    .stSlider>div>div>div {
        background-color: #9CAF88;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #E8DCC8;
        color: #6B5344;
        font-weight: 600;
        border-radius: 6px;
    }
    
    /* Divider Line */
    hr {
        border-color: #D4A574 !important;
        margin: 25px 0;
    }
    
    /* Sidebar Title Styling */
    .sidebar-title {
        color: #6B5344;
        font-weight: 700;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid #9CAF88;
        padding-left: 10px;
    }
    
    /* Chart Container */
    .chart-container {
        background-color: #FFFBF7;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(156, 175, 136, 0.1);
        margin-bottom: 20px;
    }
    
    /* Description Text */
    .chart-description {
        color: #6B5344;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 12px;
        padding: 10px;
        background-color: #F0E6D6;
        border-left: 3px solid #D4A574;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load and preprocess the 2015 Street Tree Census dataset"""
    df = pd.read_csv('data/trees.csv')
    df['created_at'] = pd.to_datetime(df['created_at'], format='%m/%d/%Y', errors='coerce')
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False
    df = None

if data_loaded and df is not None:
    # ============================================================================
    # HEADER SECTION
    # ============================================================================
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("# 🌳 NYC Street Tree Census Dashboard")
        st.markdown("### Exploratory Data Analysis - 2015 Street Tree Census Data")
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/128/2998/2998432.png", width=80)

    st.markdown("---")
    
    st.markdown("""
    ### 📊 Dashboard Overview
    This **interactive and professional dashboard** presents a comprehensive analysis of the **2015 NYC Street Tree Census** data.
    
    **Features:**
    - 🔍 **Real-time Filters**: Adjust filters to update all charts simultaneously
    - 📥 **Download Data**: Export filtered data and visualizations
    - 📈 **10+ Chart Types**: Pie, Histogram, Line, Bar, Scatter, Box, Heatmap, Area, Count, and Violin plots
    - 🎨 **Professional Theme**: Light Brown & Sage Green color scheme for optimal readability
    
    Explore tree health, species distribution, geographic patterns, and maintenance records across NYC's five boroughs.
    """)
    st.markdown("---")

    # ============================================================================
    # SIDEBAR FILTERS
    # ============================================================================
    st.sidebar.markdown('<div class="sidebar-title">🔍 FILTER CONTROLS</div>', unsafe_allow_html=True)
    st.sidebar.markdown("**Adjust filters to update all charts in real-time**")
    st.sidebar.markdown("")

    # Get unique values for filters
    boroughs = sorted(df['borough'].dropna().unique())
    health_status = sorted(df['health'].dropna().unique())
    tree_species = sorted(df['spc_common'].dropna().unique())
    user_types = sorted(df['user_type'].dropna().unique())

    # Date Range Filter with Calendar
    st.sidebar.markdown('<div class="sidebar-title">📅 Date Range Filter</div>', unsafe_allow_html=True)
    date_min = df['created_at'].min().date()
    date_max = df['created_at'].max().date()
    
    col_date1, col_date2 = st.sidebar.columns(2)
    with col_date1:
        start_date = st.date_input(
            "From:",
            value=date_min,
            min_value=date_min,
            max_value=date_max,
            key="date_start"
        )
    with col_date2:
        end_date = st.date_input(
            "To:",
            value=date_max,
            min_value=date_min,
            max_value=date_max,
            key="date_end"
        )

    # Borough Filter
    st.sidebar.markdown('<div class="sidebar-title">🏘️ Borough Selection</div>', unsafe_allow_html=True)
    selected_boroughs = st.sidebar.multiselect(
        "Select Boroughs:",
        options=boroughs,
        default=boroughs,
        key="borough_filter"
    )

    # Health Status Filter
    st.sidebar.markdown('<div class="sidebar-title">💚 Tree Health Status</div>', unsafe_allow_html=True)
    selected_health = st.sidebar.multiselect(
        "Select Health Status:",
        options=health_status,
        default=health_status,
        key="health_filter"
    )

    # Top 10 Species Filter
    st.sidebar.markdown('<div class="sidebar-title">🌱 Tree Species (Top 10)</div>', unsafe_allow_html=True)
    top_species = df['spc_common'].value_counts().head(10).index.tolist()
    selected_species = st.sidebar.multiselect(
        "Select Species:",
        options=top_species,
        default=top_species,
        key="species_filter"
    )

    # User Type Filter
    st.sidebar.markdown('<div class="sidebar-title">👤 User Type</div>', unsafe_allow_html=True)
    selected_user_type = st.sidebar.multiselect(
        "Select User Type:",
        options=user_types,
        default=user_types,
        key="user_type_filter"
    )

    # Tree Diameter (DBH) Range Slider
    st.sidebar.markdown('<div class="sidebar-title">📏 Tree Diameter (DBH)</div>', unsafe_allow_html=True)
    dbh_range = st.sidebar.slider(
        "Diameter at Breast Height (inches):",
        min_value=int(df['tree_dbh'].min()),
        max_value=int(df['tree_dbh'].max()),
        value=(int(df['tree_dbh'].min()), int(df['tree_dbh'].quantile(0.95))),
        step=1,
        key="dbh_slider"
    )

    # Address Search Filter
    st.sidebar.markdown('<div class="sidebar-title">🔎 Search Address</div>', unsafe_allow_html=True)
    search_keyword = st.sidebar.text_input(
        "Search by address (optional):",
        placeholder="e.g., 'BROADWAY'",
        key="address_search"
    )

    st.sidebar.markdown("")

    # Reset Filters Button
    col_reset1, col_reset2 = st.sidebar.columns([1, 1])
    with col_reset1:
        if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # ============================================================================
    # APPLY ALL FILTERS
    # ============================================================================
    filtered_df = df.copy()

    # Date range filter
    filtered_df = filtered_df[
        (filtered_df['created_at'].dt.date >= start_date) &
        (filtered_df['created_at'].dt.date <= end_date)
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

    # ============================================================================
    # KPI CARDS (SUMMARY METRICS)
    # ============================================================================
    st.markdown("### 📊 Key Performance Indicators (KPIs)")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:
        total_trees = len(filtered_df)
        st.metric(
            "🌳 Total Trees",
            f"{total_trees:,}",
            delta=f"{total_trees - len(df):,}" if total_trees != len(df) else "No Filter",
            delta_color="inverse"
        )

    with kpi_col2:
        avg_dbh = filtered_df['tree_dbh'].mean()
        st.metric(
            "📏 Avg Diameter",
            f"{avg_dbh:.2f}\"",
            delta=f"{(avg_dbh - df['tree_dbh'].mean()):.2f}\"" if avg_dbh != df['tree_dbh'].mean() else None
        )

    with kpi_col3:
        healthy_pct = (len(filtered_df[filtered_df['health'] == 'Good']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric(
            "💚 Healthy Trees",
            f"{healthy_pct:.1f}%",
            delta=f"{len(filtered_df[filtered_df['health'] == 'Good']):,} trees"
        )

    with kpi_col4:
        alive_pct = (len(filtered_df[filtered_df['status'] == 'Alive']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric(
            "❤️ Alive Trees",
            f"{alive_pct:.1f}%",
            delta=f"{len(filtered_df[filtered_df['status'] == 'Alive']):,} trees"
        )

    with kpi_col5:
        unique_species = filtered_df['spc_common'].nunique()
        st.metric(
            "🌿 Species Count",
            f"{unique_species}",
            delta=f"{unique_species - df['spc_common'].nunique()}" if unique_species != df['spc_common'].nunique() else None,
            delta_color="inverse"
        )

    st.markdown("---")

    # ============================================================================
    # VISUALIZATION FUNCTIONS
    # ============================================================================
    def create_pie_chart(data):
        """Pie Chart - Borough Distribution"""
        borough_counts = data['borough'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=borough_counts.index,
            values=borough_counts.values,
            marker=dict(colors=['#9CAF88', '#D4A574', '#8B7355', '#C2D4C8', '#E8DCC8']),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Trees: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )])
        fig.update_layout(
            title={'text': '<b>Borough Distribution</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500
        )
        return fig

    def create_histogram(data):
        """Histogram - Tree Diameter Distribution"""
        fig = go.Figure(data=[go.Histogram(
            x=data['tree_dbh'],
            nbinsx=50,
            marker=dict(color='#9CAF88', line=dict(color='#6B5344', width=1)),
            hovertemplate='Diameter Range: %{x}<br>Frequency: %{y}<extra></extra>'
        )])
        fig.update_layout(
            title={'text': '<b>Tree Diameter (DBH) Distribution</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Diameter at Breast Height (inches)',
            yaxis_title='Frequency',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            hovermode='x unified'
        )
        return fig

    def create_line_chart(data):
        """Line Chart - Trees Planted Over Time"""
        data_sorted = data.sort_values('created_at')
        cumulative_counts = data_sorted.groupby(data_sorted['created_at'].dt.date).size().cumsum()
        
        fig = go.Figure(data=[go.Scatter(
            x=cumulative_counts.index,
            y=cumulative_counts.values,
            mode='lines+markers',
            line=dict(color='#9CAF88', width=3),
            marker=dict(size=6, color='#D4A574'),
            hovertemplate='Date: %{x}<br>Cumulative Trees: %{y:,}<extra></extra>'
        )])
        fig.update_layout(
            title={'text': '<b>Cumulative Trees Over Time</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Date',
            yaxis_title='Cumulative Count',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            hovermode='x unified'
        )
        return fig

    def create_bar_chart(data):
        """Bar Chart - Top 10 Tree Species"""
        top_species = data['spc_common'].value_counts().head(10)
        fig = go.Figure(data=[go.Bar(
            x=top_species.values,
            y=top_species.index,
            orientation='h',
            marker=dict(color='#D4A574', line=dict(color='#6B5344', width=2)),
            hovertemplate='%{y}<br>Count: %{x:,}<extra></extra>'
        )])
        fig.update_layout(
            title={'text': '<b>Top 10 Tree Species</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Number of Trees',
            yaxis_title='Species',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            yaxis=dict(autorange="reversed")
        )
        return fig

    def create_scatter_plot(data):
        """Scatter Plot - Tree Diameter vs Health Status"""
        fig = go.Figure()
        for health in data['health'].unique():
            health_data = data[data['health'] == health]
            fig.add_trace(go.Scatter(
                x=health_data['tree_dbh'],
                y=health_data['health'],
                mode='markers',
                name=health,
                marker=dict(size=6, opacity=0.6),
                hovertemplate='Diameter: %{x:.2f}\"<br>Health: %{y}<extra></extra>'
            ))
        
        color_map = {'Good': '#9CAF88', 'Fair': '#D4A574', 'Poor': '#8B7355'}
        for i, health in enumerate(data['health'].unique()):
            fig.data[i].marker.color = color_map.get(health, '#9CAF88')
        
        fig.update_layout(
            title={'text': '<b>Tree Diameter vs Health Status</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Diameter at Breast Height (inches)',
            yaxis_title='Health Status',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            hovermode='closest'
        )
        return fig

    def create_box_plot(data):
        """Box Plot - Tree Diameter by Borough"""
        fig = go.Figure()
        for borough in sorted(data['borough'].unique()):
            borough_data = data[data['borough'] == borough]
            fig.add_trace(go.Box(
                y=borough_data['tree_dbh'],
                name=borough,
                marker=dict(color='#9CAF88'),
                hovertemplate='Borough: ' + borough + '<br>Diameter: %{y:.2f}\"<extra></extra>'
            ))
        
        fig.update_layout(
            title={'text': '<b>Tree Diameter Distribution by Borough</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            yaxis_title='Diameter at Breast Height (inches)',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500
        )
        return fig

    def create_heatmap(data):
        """Heatmap - Correlation Matrix"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        corr_matrix = data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdYlGn',
            zmid=0,
            hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title={'text': '<b>Feature Correlation Matrix</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            xaxis={'side': 'bottom'}
        )
        return fig

    def create_area_chart(data):
        """Area Chart - Tree Health Status Over Time"""
        data_sorted = data.sort_values('created_at')
        health_by_date = data_sorted.groupby([data_sorted['created_at'].dt.date, 'health']).size().unstack(fill_value=0)
        
        fig = go.Figure()
        colors = {'Good': '#9CAF88', 'Fair': '#D4A574', 'Poor': '#8B7355'}
        
        for health in health_by_date.columns:
            fig.add_trace(go.Scatter(
                x=health_by_date.index,
                y=health_by_date[health],
                name=health,
                mode='lines',
                stackgroup='one',
                fillcolor=colors.get(health, '#9CAF88'),
                line=dict(width=0.5)
            ))
        
        fig.update_layout(
            title={'text': '<b>Tree Health Status Over Time</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Date',
            yaxis_title='Count',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500,
            hovermode='x unified'
        )
        return fig

    def create_count_plot(data):
        """Count Plot - Tree Health Status Frequency"""
        health_counts = data['health'].value_counts()
        fig = go.Figure(data=[go.Bar(
            x=health_counts.index,
            y=health_counts.values,
            marker=dict(color=['#9CAF88', '#D4A574', '#8B7355'][:len(health_counts)]),
            text=health_counts.values,
            textposition='auto',
            hovertemplate='Health Status: %{x}<br>Count: %{y:,}<extra></extra>'
        )])
        fig.update_layout(
            title={'text': '<b>Tree Health Status Distribution</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            xaxis_title='Health Status',
            yaxis_title='Frequency',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500
        )
        return fig

    def create_violin_plot(data):
        """Violin Plot - Tree Diameter Distribution by Health Status"""
        fig = go.Figure()
        for health in sorted(data['health'].unique()):
            health_data = data[data['health'] == health]
            fig.add_trace(go.Violin(
                y=health_data['tree_dbh'],
                name=health,
                box_visible=True,
                meanline_visible=True,
                points=False,
                marker=dict(color='#9CAF88')
            ))
        
        fig.update_layout(
            title={'text': '<b>Tree Diameter Distribution by Health Status</b>', 'font': {'size': 18, 'color': '#6B5344'}},
            yaxis_title='Diameter at Breast Height (inches)',
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=500
        )
        return fig

    # ============================================================================
    # DISPLAY ALL CHARTS
    # ============================================================================
    st.markdown("### 📈 Data Visualizations")
    st.markdown("**Click on chart legend items to toggle visibility. Hover for detailed information.**")
    st.markdown("")

    # Chart Descriptions
    chart_descriptions = {
        'pie': '**📊 Pie Chart**: Shows the proportional distribution of trees across different boroughs. Helps identify which borough has the most street trees.',
        'histogram': '**📏 Histogram**: Displays the frequency distribution of tree diameter (DBH). Shows how tree sizes are distributed - reveals whether we have mostly small, medium, or large trees.',
        'line': '**📈 Line Chart**: Illustrates cumulative growth of trees over time during the survey period. Shows the overall trend and progression of tree census data collection.',
        'bar': '**🌲 Bar Chart**: Compares tree counts across the top 10 most common tree species. Identifies which species are most prevalent on NYC streets.',
        'scatter': '**🔵 Scatter Plot**: Visualizes the relationship between tree diameter and health status. Reveals patterns - does tree size correlate with health conditions?',
        'box': '**📦 Box Plot**: Shows the distribution of tree diameter by borough. Displays median, quartiles, and outliers - which borough has the largest/smallest trees?',
        'heatmap': '**🔥 Heatmap**: Visualizes correlations between numerical features. Shows which tree characteristics are strongly related to each other.',
        'area': '**📚 Area Chart**: Shows cumulative trends in tree health status over time. Demonstrates how the distribution of healthy/fair/poor trees evolved during the survey.',
        'count': '**📊 Count Plot**: Displays frequency counts of tree health conditions. Shows how many trees fall into each health category (Good, Fair, Poor).',
        'violin': '**🎻 Violin Plot**: Shows the probability density distribution of tree diameter by health status. Reveals detailed size patterns within each health category.'
    }

    # ROW 1: Pie Chart, Histogram, Line Chart
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="chart-description">' + chart_descriptions['pie'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_pie_chart(filtered_df), use_container_width=True, height=500)

    with col2:
        st.markdown('<div class="chart-description">' + chart_descriptions['histogram'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_histogram(filtered_df), use_container_width=True, height=500)

    with col3:
        st.markdown('<div class="chart-description">' + chart_descriptions['line'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_line_chart(filtered_df), use_container_width=True, height=500)

    st.markdown("")

    # ROW 2: Bar Chart, Scatter Plot, Box Plot
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="chart-description">' + chart_descriptions['bar'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_bar_chart(filtered_df), use_container_width=True, height=500)

    with col2:
        st.markdown('<div class="chart-description">' + chart_descriptions['scatter'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_scatter_plot(filtered_df), use_container_width=True, height=500)

    with col3:
        st.markdown('<div class="chart-description">' + chart_descriptions['box'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_box_plot(filtered_df), use_container_width=True, height=500)

    st.markdown("")

    # ROW 3: Heatmap, Area Chart, Count Plot
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="chart-description">' + chart_descriptions['heatmap'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_heatmap(filtered_df), use_container_width=True, height=500)

    with col2:
        st.markdown('<div class="chart-description">' + chart_descriptions['area'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_area_chart(filtered_df), use_container_width=True, height=500)

    with col3:
        st.markdown('<div class="chart-description">' + chart_descriptions['count'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_count_plot(filtered_df), use_container_width=True, height=500)

    st.markdown("")

    # ROW 4: Violin Plot (Centered)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="chart-description">' + chart_descriptions['violin'] + '</div>', unsafe_allow_html=True)
        st.plotly_chart(create_violin_plot(filtered_df), use_container_width=True, height=500)

    st.markdown("---")

    # ============================================================================
    # DATA EXPORT SECTION
    # ============================================================================
    st.markdown("### 📥 Data Export & Download")
    
    export_col1, export_col2, export_col3 = st.columns(3)

    with export_col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name=f"tree_census_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:
        summary_stats = {
            'Total Trees': len(filtered_df),
            'Average Diameter (inches)': round(filtered_df['tree_dbh'].mean(), 2),
            'Median Diameter (inches)': round(filtered_df['tree_dbh'].median(), 2),
            'Healthy % (Good Status)': round((len(filtered_df[filtered_df['health'] == 'Good']) / len(filtered_df) * 100), 2) if len(filtered_df) > 0 else 0,
            'Alive % (Status)': round((len(filtered_df[filtered_df['status'] == 'Alive']) / len(filtered_df) * 100), 2) if len(filtered_df) > 0 else 0,
            'Species Count': filtered_df['spc_common'].nunique(),
        }
        summary_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
        csv_summary = summary_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Summary Statistics",
            data=csv_summary,
            file_name=f"tree_census_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col3:
        # Display summary statistics as a table
        summary_stats_display = {
            'Total Records': f"{len(filtered_df):,}",
            'Avg DBH': f"{filtered_df['tree_dbh'].mean():.2f}\"",
            'Species Variety': f"{filtered_df['spc_common'].nunique()}",
            'Healthy Trees': f"{healthy_pct:.1f}%",
        }
        
        st.info("**📊 Quick Summary:**\n\n" + 
                "\n".join([f"• {k}: {v}" for k, v in summary_stats_display.items()]))

    st.markdown("---")

    # ============================================================================
    # FOOTER INFORMATION
    # ============================================================================
    st.markdown("""
    <div style='background-color: #F0E6D6; padding: 20px; border-radius: 10px; border-left: 5px solid #9CAF88; margin-top: 30px;'>
    <h4 style='color: #6B5344; margin-top: 0;'>📋 Dashboard Information</h4>
    <div style='color: #6B5344; font-size: 14px;'>
    <b>Dataset:</b> 2015 NYC Street Tree Census<br>
    <b>Total Records Available:</b> {:,} trees<br>
    <b>Current Filtered Records:</b> {:,} trees<br>
    <b>Analysis Date:</b> {}<br>
    <b>Chart Types:</b> 10 (Pie, Histogram, Line, Bar, Scatter, Box, Heatmap, Area, Count, Violin)<br>
    <b>Interactive Filters:</b> Date Range, Borough, Health Status, Species, User Type, DBH Range, Address Search<br>
    <b>Theme:</b> Light Brown & Sage Green (Professional Color Scheme)<br>
    </div>
    </div>
    """.format(len(df), len(filtered_df), datetime.now().strftime('%B %d, %Y at %H:%M')), unsafe_allow_html=True)

else:
    st.error("⚠️ Unable to load the dataset. Please ensure the CSV file is in the 'data' folder with the correct filename.")