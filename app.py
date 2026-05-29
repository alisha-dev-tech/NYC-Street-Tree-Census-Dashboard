import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="NYC Street Tree Census Dashboard",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
      font-family: 'Lato', sans-serif;
      background-color: #FAFAF8;
      color: #3B2A1A;
  }

  /* ── Main background ── */
  .main { background-color: #FAFAF8; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #F2E4C8 0%, #E8D5A8 100%);
      border-right: 3px solid #8B7355;
      padding-top: 10px;
  }

  /* Sidebar all text visible & bold */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div,
  [data-testid="stSidebar"] label {
      color: #3B2A1A !important;
      font-weight: 600 !important;
  }

  /* Sidebar widget labels */
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
      color: #5C3D2E !important;
      font-weight: 700 !important;
      font-size: 0.88rem !important;
  }

  /* Sidebar input boxes */
  [data-testid="stSidebar"] input {
      background: #FFFAF2 !important;
      border: 1.5px solid #D4A574 !important;
      color: #3B2A1A !important;
      font-weight: 600 !important;
      border-radius: 6px !important;
  }

  /* ── Headings ── */
  h1, h2, h3 {
      color: #6B5344;
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      letter-spacing: 0.5px;
  }
  h1 { border-bottom: 3px solid #9CAF88; padding-bottom: 10px; }

  /* ── KPI metric cards — equal size ── */
  [data-testid="metric-container"] {
      background: linear-gradient(135deg, #FFFBF7 0%, #FFF8F3 100%);
      border-left: 5px solid #9CAF88;
      border-radius: 10px;
      padding: 20px;
      min-height: 110px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      box-shadow: 0 2px 8px rgba(156,175,136,0.15);
  }
  [data-testid="metric-container"] label {
      color: #9CAF88 !important;
      font-weight: 700 !important;
      font-size: 0.82rem !important;
      text-transform: uppercase;
      letter-spacing: 0.05em;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
      color: #6B5344 !important;
      font-family: 'Playfair Display', serif;
      font-size: 1.7rem !important;
  }

  /* ── Buttons ── */
  .stButton > button {
      background-color: #9CAF88;
      color: white;
      border-radius: 8px;
      padding: 10px 24px;
      font-weight: 700;
      border: none;
      transition: all 0.3s ease;
      box-shadow: 0 2px 6px rgba(156,175,136,0.25);
  }
  .stButton > button:hover {
      background-color: #6B5344;
      box-shadow: 0 4px 12px rgba(156,175,136,0.4);
      transform: translateY(-2px);
  }

  /* ── Download buttons ── */
  .stDownloadButton > button {
      background-color: #D4A574;
      color: white;
      border-radius: 8px;
      font-weight: 700;
      border: none;
  }
  .stDownloadButton > button:hover { background-color: #8B7355; }

  /* ── Chart description box ── */
  .chart-description {
      color: #6B5344;
      font-size: 13px;
      font-weight: 500;
      margin-top: 6px;
      padding: 10px 14px;
      background-color: #F0E6D6;
      border-left: 3px solid #D4A574;
      border-radius: 4px;
      font-style: italic;
  }

  /* ── Sidebar section title ── */
  .sidebar-title {
      color: #5C3D2E !important;
      font-family: 'Playfair Display', serif;
      font-weight: 700 !important;
      font-size: 0.95rem !important;
      margin: 14px 0 6px 0;
      background: linear-gradient(90deg, #9CAF8822, transparent);
      border-left: 3px solid #9CAF88;
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
  }

  hr { border-color: #D4B896 !important; }
  [data-testid="stDataFrame"] { border: 1px solid #D4B896; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# LOAD DATA
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/trees.csv")
    df['created_at'] = pd.to_datetime(df['created_at'], format='%m/%d/%Y', errors='coerce')
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    data_loaded = False
    df = None

# =============================================================================
# MAIN APPLICATION
# =============================================================================
if data_loaded and df is not None:

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.markdown("# 🌳 NYC Street Tree Census Dashboard")
        st.markdown("### Exploratory Data Analysis — 2015 Street Tree Census Data")
    with col_h2:
        st.image("https://cdn-icons-png.flaticon.com/128/2998/2998432.png", width=80)

    st.markdown("---")

    st.markdown("""
    ### 📊 Dashboard Overview
    This interactive dashboard presents a comprehensive analysis of the **2015 NYC Street Tree Census** dataset.

    **Features:**
    🔍 Real-time sidebar filters &nbsp;|&nbsp;
    📥 CSV export &nbsp;|&nbsp;
    📈 8 interactive chart types &nbsp;|&nbsp;
    🎨 Light Brown & Sage Green theme
    """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # SIDEBAR FILTERS
    # -------------------------------------------------------------------------
    st.sidebar.markdown(
        '<div class="sidebar-title">🔍 FILTER CONTROLS</div>', unsafe_allow_html=True)
    st.sidebar.markdown("**Adjust filters to update all charts in real-time**")

    # -- Date Range --
    st.sidebar.markdown(
        '<div class="sidebar-title">📅 Date Range</div>', unsafe_allow_html=True)

    date_min = df['created_at'].min().date()
    date_max = df['created_at'].max().date()

    col_d1, col_d2 = st.sidebar.columns(2)
    with col_d1:
        start_date = st.date_input(
            "From:", value=date_min,
            min_value=date_min, max_value=date_max,
            key="start_date"           # ← unique key fixes DuplicateElementId
        )
    with col_d2:
        end_date = st.date_input(
            "To:", value=date_max,
            min_value=date_min, max_value=date_max,
            key="end_date"             # ← unique key
        )

    # -- Borough --
    st.sidebar.markdown(
        '<div class="sidebar-title">🏘️ Borough</div>', unsafe_allow_html=True)
    boroughs = sorted(df['borough'].dropna().unique())
    selected_boroughs = st.sidebar.multiselect(
        "Select Boroughs:", boroughs, default=boroughs, key="boroughs")

    # -- Health Status --
    st.sidebar.markdown(
        '<div class="sidebar-title">💚 Tree Health Status</div>', unsafe_allow_html=True)
    health_status = sorted(df['health'].dropna().unique())
    selected_health = st.sidebar.multiselect(
        "Select Health Status:", health_status, default=health_status, key="health")

    # -- Species --
    st.sidebar.markdown(
        '<div class="sidebar-title">🌱 Species (Top 10)</div>', unsafe_allow_html=True)
    top_species = df['spc_common'].value_counts().head(10).index.tolist()
    selected_species = st.sidebar.multiselect(
        "Select Species:", top_species, default=top_species, key="species")

    # -- User Type --
    st.sidebar.markdown(
        '<div class="sidebar-title">👤 User Type</div>', unsafe_allow_html=True)
    user_types = sorted(df['user_type'].dropna().unique())
    selected_user_type = st.sidebar.multiselect(
        "Select User Type:", user_types, default=user_types, key="user_type")

    # -- DBH Slider --
    st.sidebar.markdown(
        '<div class="sidebar-title">📏 Tree Diameter (DBH)</div>', unsafe_allow_html=True)
    dbh_min_val = int(df['tree_dbh'].min())
    dbh_max_val = int(df['tree_dbh'].max())
    dbh_range = st.sidebar.slider(
        "Diameter at Breast Height (inches):",
        min_value=dbh_min_val, max_value=dbh_max_val,
        value=(dbh_min_val, int(df['tree_dbh'].quantile(0.95))),
        key="dbh_range"
    )

    # -- Address Search --
    st.sidebar.markdown(
        '<div class="sidebar-title">🔎 Search Address</div>', unsafe_allow_html=True)
    search_keyword = st.sidebar.text_input(
        "Search by address:", placeholder="e.g. BROADWAY", key="search")

    # -- Reset --
    st.sidebar.markdown("---")
    FILTER_KEYS = ["start_date", "end_date", "boroughs", "health",
                   "species", "user_type", "dbh_range", "search"]
    if st.sidebar.button("🔄 Reset Filters", use_container_width=True, key="reset_btn"):
        for k in FILTER_KEYS:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    # -------------------------------------------------------------------------
    # APPLY FILTERS
    # -------------------------------------------------------------------------
    filtered_df = df.copy()

    filtered_df = filtered_df[
        (filtered_df['created_at'].dt.date >= start_date) &
        (filtered_df['created_at'].dt.date <= end_date)
    ]
    if selected_boroughs:
        filtered_df = filtered_df[filtered_df['borough'].isin(selected_boroughs)]
    if selected_health:
        filtered_df = filtered_df[filtered_df['health'].isin(selected_health)]
    if selected_species:
        filtered_df = filtered_df[filtered_df['spc_common'].isin(selected_species)]
    if selected_user_type:
        filtered_df = filtered_df[filtered_df['user_type'].isin(selected_user_type)]

    filtered_df = filtered_df[
        (filtered_df['tree_dbh'] >= dbh_range[0]) &
        (filtered_df['tree_dbh'] <= dbh_range[1])
    ]
    if search_keyword:
        filtered_df = filtered_df[
            filtered_df['address'].str.contains(search_keyword.upper(), na=False)
        ]

    # -------------------------------------------------------------------------
    # EMPTY DATA CHECK
    # -------------------------------------------------------------------------
    if filtered_df.empty:
        st.warning("⚠️ No data available for selected filters. Please adjust and try again.")
        st.stop()

    # -------------------------------------------------------------------------
    # KPI METRICS — computed once, reused safely below
    # -------------------------------------------------------------------------
    total_trees  = len(filtered_df)
    avg_dbh      = filtered_df['tree_dbh'].mean()
    healthy_pct  = (
        len(filtered_df[filtered_df['health'] == 'Good']) / total_trees * 100
        if total_trees > 0 else 0
    )
    alive_pct    = (
        len(filtered_df[filtered_df['status'] == 'Alive']) / total_trees * 100
        if total_trees > 0 else 0
    )
    species_count = filtered_df['spc_common'].nunique()

    st.markdown("### 📊 Key Performance Indicators")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🌳 Total Trees",    f"{total_trees:,}")
    k2.metric("📏 Avg Diameter",   f"{avg_dbh:.2f}\"")
    k3.metric("💚 Healthy Trees",  f"{healthy_pct:.1f}%")
    k4.metric("❤️ Alive Trees",    f"{alive_pct:.1f}%")
    k5.metric("🌿 Species Count",  species_count)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # CHART LAYOUT HELPER
    # -------------------------------------------------------------------------
    COLORS = {
        'sage':       '#9CAF88',
        'brown':      '#D4A574',
        'dark_brown': '#8B7355',
        'light_sage': '#C2D4C8',
        'palette':    ['#9CAF88', '#D4A574', '#8B7355', '#C2D4C8',
                       '#6B5344', '#B5C9A1', '#E8C99A', '#7A9370'],
    }

    def base_layout(fig, title, height=480):
        fig.update_layout(
            title={'text': f'<b>{title}</b>',
                   'font': {'size': 17, 'color': '#6B5344', 'family': 'serif'}},
            font=dict(size=12, color='#6B5344'),
            plot_bgcolor='#FFFBF7',
            paper_bgcolor='#FFFBF7',
            height=height,
            margin=dict(l=40, r=20, t=60, b=40),
        )
        fig.update_xaxes(gridcolor='#EAD9C4', zerolinecolor='#D4B896')
        fig.update_yaxes(gridcolor='#EAD9C4', zerolinecolor='#D4B896')
        return fig

    def chart_block(fig, description):
        """Render a plotly chart + its description box."""
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            f'<div class="chart-description">{description}</div>',
            unsafe_allow_html=True
        )

    # -------------------------------------------------------------------------
    # CHART DEFINITIONS
    # -------------------------------------------------------------------------

    # 1. Pie — Borough Distribution
    def chart_pie(data):
        counts = data['borough'].value_counts()
        fig = go.Figure(go.Pie(
            labels=counts.index, values=counts.values,
            hole=0.35,
            marker=dict(colors=COLORS['palette'],
                        line=dict(color='#FFFBF7', width=2))
        ))
        return base_layout(fig, "Borough Distribution")

    # 2. Histogram — DBH
    def chart_histogram(data):
        fig = go.Figure(go.Histogram(
            x=data['tree_dbh'], nbinsx=50,
            marker_color=COLORS['sage'],
            marker_line=dict(color='#FFFBF7', width=0.5)
        ))
        fig.update_xaxes(title="Tree Diameter (inches)")
        fig.update_yaxes(title="Frequency")
        return base_layout(fig, "Tree Diameter (DBH) Distribution")

    # 3. Bar — Top 10 Species
    def chart_species_bar(data):
        species = data['spc_common'].value_counts().head(10)
        fig = go.Figure(go.Bar(
            x=species.values, y=species.index,
            orientation='h',
            marker_color=COLORS['brown'],
            marker_line=dict(color='#FFFBF7', width=0.5),
            text=species.values, textposition='outside'
        ))
        fig.update_xaxes(title="Count")
        return base_layout(fig, "Top 10 Tree Species")

    # 4. Box Plot — DBH by Borough
    def chart_box(data):
        fig = go.Figure()
        for i, borough in enumerate(sorted(data['borough'].dropna().unique())):
            subset = data[data['borough'] == borough]
            fig.add_trace(go.Box(
                y=subset['tree_dbh'], name=borough,
                marker_color=COLORS['palette'][i % len(COLORS['palette'])],
                line_color='#6B5344'
            ))
        fig.update_yaxes(title="Tree Diameter (inches)")
        return base_layout(fig, "Tree Diameter by Borough")

    # 5. Bar — Health Distribution
    def chart_health_bar(data):
        counts = data['health'].value_counts()
        health_colors = {'Good': '#9CAF88', 'Fair': '#D4A574', 'Poor': '#8B7355'}
        colors_list = [health_colors.get(h, '#C2D4C8') for h in counts.index]
        fig = go.Figure(go.Bar(
            x=counts.index, y=counts.values,
            marker_color=colors_list,
            marker_line=dict(color='#FFFBF7', width=0.5),
            text=counts.values, textposition='outside'
        ))
        fig.update_yaxes(title="Number of Trees")
        return base_layout(fig, "Tree Health Distribution")

    # 6. Violin — DBH by Health
    def chart_violin(data):
        fig = go.Figure()
        health_colors = {'Good': '#9CAF88', 'Fair': '#D4A574', 'Poor': '#8B7355'}
        for health in sorted(data['health'].dropna().unique()):
            subset = data[data['health'] == health]
            fig.add_trace(go.Violin(
                y=subset['tree_dbh'], name=health,
                box_visible=True, meanline_visible=True,
                fillcolor=health_colors.get(health, '#C2D4C8'),
                line_color='#6B5344', opacity=0.75
            ))
        fig.update_yaxes(title="Tree Diameter (inches)")
        return base_layout(fig, "DBH Distribution by Health Status")

    # 7. Heatmap — Correlation
    def chart_heatmap(data):
        num_cols = data.select_dtypes(include=np.number)
        corr = num_cols.corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale='RdYlGn',
            zmin=-1, zmax=1,
            text=corr.round(2).values,
            texttemplate='%{text}',
            hoverongaps=False
        ))
        return base_layout(fig, "Numeric Feature Correlation Heatmap")

    # 8. Bar — Trees by User Type
    def chart_user_type(data):
        counts = data['user_type'].value_counts()
        fig = go.Figure(go.Bar(
            x=counts.index, y=counts.values,
            marker_color=COLORS['palette'][:len(counts)],
            marker_line=dict(color='#FFFBF7', width=0.5),
            text=counts.values, textposition='outside'
        ))
        fig.update_yaxes(title="Number of Trees")
        return base_layout(fig, "Trees Recorded by User Type")

    # -------------------------------------------------------------------------
    # DISPLAY CHARTS
    # -------------------------------------------------------------------------
    st.markdown("### 📈 Data Visualizations")

    # ROW 1
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        chart_block(
            chart_pie(filtered_df),
            "🏘️ <b>Borough Distribution</b> — Shows how trees are spread across NYC boroughs. "
            "Queens and Brooklyn typically have the highest share due to their larger residential areas."
        )
    with r1c2:
        chart_block(
            chart_histogram(filtered_df),
            "📏 <b>Diameter Distribution</b> — Most street trees have a small DBH (under 10\"), "
            "indicating younger or recently planted trees. Very large trees are rare."
        )
    with r1c3:
        chart_block(
            chart_species_bar(filtered_df),
            "🌲 <b>Top 10 Species</b> — London Plane and Honeylocust dominate NYC streets "
            "as they are hardy, pollution-tolerant species favoured for urban planting."
        )

    # ROW 2
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        chart_block(
            chart_box(filtered_df),
            "📦 <b>DBH by Borough</b> — Box plots reveal the spread and outliers of tree diameter "
            "per borough. Staten Island often has older, larger trees compared to Manhattan."
        )
    with r2c2:
        chart_block(
            chart_health_bar(filtered_df),
            "💚 <b>Health Distribution</b> — Majority of NYC street trees are in 'Good' health. "
            "A small percentage rated 'Poor' may require pruning or removal attention."
        )
    with r2c3:
        chart_block(
            chart_violin(filtered_df),
            "🎻 <b>DBH by Health Status</b> — Violin plots show that healthier trees tend to have "
            "a wider range of diameters, while 'Poor' health trees skew smaller."
        )

    # ROW 3
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        chart_block(
            chart_heatmap(filtered_df),
            "🔥 <b>Correlation Heatmap</b> — Shows relationships between numeric columns. "
            "Strong correlations (close to +1 or -1) may indicate linked tree characteristics."
        )
    with r3c2:
        chart_block(
            chart_user_type(filtered_df),
            "👤 <b>Trees by User Type</b> — Indicates who recorded each tree in the census. "
            "NYC Parks staff account for most entries, with volunteers contributing significantly."
        )

    st.markdown("---")

    # -------------------------------------------------------------------------
    # DATA EXPORT
    # -------------------------------------------------------------------------
    st.markdown("### 📥 Data Export & Download")

    ex1, ex2, ex3 = st.columns(3)

    with ex1:
        csv_full = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_full,
            file_name=f"filtered_trees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_full"
        )

    with ex2:
        summary_df = pd.DataFrame({
            'Metric': ['Total Trees', 'Avg DBH (in)', 'Median DBH (in)',
                       'Healthy %', 'Alive %', 'Species Count'],
            'Value': [
                total_trees,
                round(avg_dbh, 2),
                round(filtered_df['tree_dbh'].median(), 2),
                round(healthy_pct, 2),
                round(alive_pct, 2),
                species_count
            ]
        })
        st.download_button(
            label="📊 Download Summary Stats (CSV)",
            data=summary_df.to_csv(index=False),
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_summary"
        )

    with ex3:
        st.info(f"""
**📊 Quick Summary**

• Total Records: **{total_trees:,}**
• Avg DBH: **{avg_dbh:.2f}"**
• Species Variety: **{species_count}**
• Healthy Trees: **{healthy_pct:.1f}%**
• Alive Trees: **{alive_pct:.1f}%**
        """)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # FOOTER  — inside the if-block, indentation is correct
    # -------------------------------------------------------------------------
    st.markdown(f"""
<div style="
    background-color:#F0E6D6;
    padding:22px 28px;
    border-radius:12px;
    border-left:5px solid #9CAF88;
    margin-top:20px;
">
  <h4 style="color:#6B5344; margin-top:0; font-family:'Playfair Display',serif;">
      📋 Dashboard Information
  </h4>
  <div style="color:#6B5344; font-size:14px; line-height:2;">
      <b>Dataset:</b> 2015 NYC Street Tree Census<br>
      <b>Total Records Available:</b> {len(df):,} trees<br>
      <b>Currently Displayed:</b> {total_trees:,} trees<br>
      <b>Chart Types:</b> Pie · Histogram · Bar · Box · Violin · Heatmap · Health Bar · User Type Bar<br>
      <b>Theme:</b> Light Brown &amp; Sage Green<br>
      <b>Built with:</b> Streamlit &amp; Plotly
  </div>
</div>
""", unsafe_allow_html=True)

# End of if data_loaded block