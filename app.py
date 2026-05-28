import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="NYC Trees Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌳"
)

# =========================================================
# CINEMATIC SAGA GREEN + LUXURY BROWN THEME
# =========================================================
SAGA_GREEN      = "#2EC4B6"
SAGA_GREEN_DARK = "#1B9AAA"
SAGA_GLOW       = "#52F7D4"

ESPRESSO        = "#1A120B"
DARK_BROWN      = "#2C1810"
CARD_BROWN      = "#3B241A"
SOFT_BROWN      = "#5C4033"

GOLD            = "#FFB703"
GOLD_LIGHT      = "#FFD166"

CREAM           = "#FFF8E7"
TEXT_MAIN       = "#F8F5F0"
TEXT_DIM        = "#D6C2A8"

BG_MAIN         = "#120B08"
BG_CARD         = "#241712"
BG_SIDEBAR      = "#1B110D"

BORDER          = "#5B3A29"

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(f"""
<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */
html, body, [data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(circle at top left, #2b1d16 0%, {BG_MAIN} 45%);
    color: {TEXT_MAIN};
    font-family: 'Inter', sans-serif;
}}

/* Main container */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */
[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {BG_SIDEBAR} 0%,
        #261812 100%
    ) !important;

    border-right: 2px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {SAGA_GREEN} !important;
    font-weight: 700;
}}

[data-testid="stSidebar"] label {{
    color: {TEXT_MAIN} !important;
    font-weight: 600;
}}

[data-testid="stSidebar"] .stMarkdown p {{
    color: {TEXT_DIM} !important;
}}

/* ===================================================== */
/* TITLE */
/* ===================================================== */
h1 {{
    color: {SAGA_GREEN} !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;

    text-shadow:
        0 0 8px rgba(46,196,182,0.35),
        0 0 22px rgba(46,196,182,0.15);
}}

h2, h3 {{
    color: {GOLD_LIGHT} !important;
    font-weight: 700 !important;
}}

/* ===================================================== */
/* INFO / ALERT BOX */
/* ===================================================== */
[data-testid="stAlert"] {{
    background: linear-gradient(
        135deg,
        rgba(46,196,182,0.12),
        rgba(255,183,3,0.08)
    ) !important;

    border: 1px solid rgba(46,196,182,0.4) !important;

    border-radius: 16px;
    backdrop-filter: blur(6px);

    color: {TEXT_MAIN} !important;
}}

/* ===================================================== */
/* METRIC CARDS */
/* ===================================================== */
[data-testid="metric-container"] {{
    background:
        linear-gradient(
            145deg,
            rgba(59,36,26,0.95),
            rgba(36,23,18,0.98)
        );

    border: 1px solid rgba(255,255,255,0.08);

    border-left: 5px solid {SAGA_GREEN};

    border-radius: 18px;

    padding: 1.2rem;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.35),
        0 0 0 1px rgba(46,196,182,0.05);

    transition: 0.3s ease;
}}

[data-testid="metric-container"]:hover {{
    transform: translateY(-3px);
    box-shadow:
        0 12px 28px rgba(0,0,0,0.45),
        0 0 18px rgba(46,196,182,0.18);
}}

[data-testid="metric-container"] label {{
    color: {TEXT_DIM} !important;
    font-size: 0.9rem !important;
}}

[data-testid="stMetricValue"] {{
    color: {CREAM} !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}

/* ===================================================== */
/* BUTTONS */
/* ===================================================== */
.stButton > button {{
    background: linear-gradient(
        135deg,
        {SAGA_GREEN},
        {SAGA_GREEN_DARK}
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    font-weight: 700 !important;

    padding: 0.6rem 1rem !important;

    box-shadow:
        0 4px 14px rgba(46,196,182,0.35);

    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: scale(1.03);
    box-shadow:
        0 6px 18px rgba(46,196,182,0.5);
}}

/* ===================================================== */
/* MULTISELECT */
/* ===================================================== */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background: linear-gradient(
        135deg,
        {SAGA_GREEN_DARK},
        {SAGA_GREEN}
    ) !important;

    color: white !important;

    border-radius: 8px !important;

    border: none !important;

    font-weight: 600;
}}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
    color: white !important;
}}

/* ===================================================== */
/* INPUTS */
/* ===================================================== */
div[data-baseweb="select"] > div {{
    background-color: {BG_CARD} !important;

    border: 1px solid {BORDER} !important;

    border-radius: 10px !important;
}}

/* ===================================================== */
/* SLIDER */
/* ===================================================== */
.stSlider > div > div > div > div {{
    background: linear-gradient(
        90deg,
        {SAGA_GREEN},
        {GOLD}
    ) !important;
}}

/* ===================================================== */
/* DATAFRAME */
/* ===================================================== */
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        0 8px 22px rgba(0,0,0,0.3);
}}

/* ===================================================== */
/* CAPTION */
/* ===================================================== */
.stCaption {{
    color: {TEXT_DIM} !important;
    font-style: italic;
}}

/* ===================================================== */
/* CHART CONTAINERS */
/* ===================================================== */
.element-container:has(canvas) {{
    background: linear-gradient(
        145deg,
        rgba(59,36,26,0.85),
        rgba(36,23,18,0.95)
    );

    padding: 1rem;
    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        0 8px 24px rgba(0,0,0,0.35);

    margin-bottom: 1rem;
}}

/* Divider */
hr {{
    border-color: rgba(255,255,255,0.08);
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# MATPLOTLIB THEME
# =========================================================
plt.rcParams.update({
    'figure.facecolor': BG_CARD,
    'axes.facecolor': BG_CARD,
    'axes.edgecolor': BORDER,
    'axes.labelcolor': TEXT_MAIN,
    'xtick.color': TEXT_DIM,
    'ytick.color': TEXT_DIM,
    'text.color': TEXT_MAIN,
    'grid.color': '#5c4033',
    'grid.alpha': 0.25,
    'axes.titleweight': 'bold',
    'axes.titlecolor': GOLD_LIGHT,
})

# =========================================================
# CHART COLORS
# =========================================================
CHART_PALETTE = [
    "#2EC4B6",
    "#FFB703",
    "#FB8500",
    "#8ECAE6",
    "#90BE6D",
    "#FFD166",
    "#E76F51"
]

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/trees.csv", low_memory=False)

    except FileNotFoundError:
        st.error("❌ trees.csv file not found in data folder")
        st.stop()

    if 'boro_name' in df.columns:
        df = df.rename(columns={'boro_name': 'boroname'})

    elif 'borough' in df.columns:
        df = df.rename(columns={'borough': 'boroname'})

    elif 'boroname' not in df.columns:
        st.error("❌ Borough column missing")
        st.stop()

    df['tree_dbh'] = pd.to_numeric(df['tree_dbh'], errors='coerce')

    df['spc_common'] = df['spc_common'].fillna('Unknown')
    df['boroname'] = df['boroname'].fillna('Unknown')
    df['health'] = df['health'].fillna('Unknown')
    df['status'] = df['status'].fillna('Unknown')

    df = df.dropna(subset=['tree_dbh'])

    return df

df = load_data()

# =========================================================
# HEADER
# =========================================================
st.title("🌳 NYC Street Trees Dashboard")

st.markdown(
    f"""
    <p style='color:{TEXT_DIM}; font-size:1.05rem;'>
    Explore NYC Tree Census data with interactive filters and insights.
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🔍 Filters")

st.sidebar.markdown(
    f"<p style='color:{TEXT_DIM}'>All filters update every chart instantly.</p>",
    unsafe_allow_html=True
)

# Borough filter
st.sidebar.subheader("🏙️ Borough")

boroughs = st.sidebar.multiselect(
    "Select Borough",
    sorted(df['boroname'].unique()),
    default=sorted(df['boroname'].unique())
)

# Health filter
st.sidebar.subheader("🌿 Tree Health")

health = st.sidebar.multiselect(
    "Tree Health",
    sorted(df['health'].unique()),
    default=sorted(df['health'].unique())
)

# Status filter
st.sidebar.subheader("📋 Tree Status")

status = st.sidebar.multiselect(
    "Tree Status",
    sorted(df['status'].unique()),
    default=sorted(df['status'].unique())
)

# Diameter filter
st.sidebar.subheader("📏 Trunk Diameter")

dbh_min = float(df['tree_dbh'].min())
dbh_max = float(df['tree_dbh'].max())

dbh_range = st.sidebar.slider(
    "Diameter Range",
    dbh_min,
    dbh_max,
    (dbh_min, dbh_max)
)

st.sidebar.divider()

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

# =========================================================
# APPLY FILTERS
# =========================================================
df2 = df[
    (df['boroname'].isin(boroughs)) &
    (df['health'].isin(health)) &
    (df['status'].isin(status)) &
    (df['tree_dbh'] >= dbh_range[0]) &
    (df['tree_dbh'] <= dbh_range[1])
].copy()

st.info(f"🌳 Active Filters: {len(df2):,} trees selected")

if df2.empty:
    st.warning("⚠️ No trees match current filters.")
    st.stop()

# =========================================================
# KPI SECTION
# =========================================================
st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Trees", f"{len(df2):,}")

c2.metric(
    "Unique Species",
    f"{df2['spc_common'].nunique():,}"
)

c3.metric(
    "Avg Trunk Diameter",
    f"{df2['tree_dbh'].mean():.1f}\""
)

c4.metric(
    "Boroughs",
    f"{df2['boroname'].nunique()}"
)

st.divider()

# =========================================================
# CHART HELPER
# =========================================================
def styled_fig(w=6, h=4):
    fig, ax = plt.subplots(figsize=(w, h))

    fig.patch.set_facecolor(BG_CARD)
    ax.set_facecolor(BG_CARD)

    return fig, ax

# =========================================================
# CHARTS
# =========================================================

# ---------------------------------------------------------
# 1 + 2
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("1. Trees by Borough")

    borough_counts = df2['boroname'].value_counts()

    fig, ax = styled_fig()

    sns.barplot(
        x=borough_counts.values,
        y=borough_counts.index,
        ax=ax,
        palette=CHART_PALETTE
    )

    ax.set_xlabel("Count")

    st.pyplot(fig)

with col2:

    st.subheader("2. Top 10 Tree Species")

    top_species = df2['spc_common'].value_counts().head(10)

    fig, ax = styled_fig()

    sns.barplot(
        x=top_species.values,
        y=top_species.index,
        ax=ax,
        palette=CHART_PALETTE
    )

    ax.set_xlabel("Count")

    st.pyplot(fig)

# ---------------------------------------------------------
# 3 + 4
# ---------------------------------------------------------
col3, col4 = st.columns(2)

with col3:

    st.subheader("3. Tree Health Distribution")

    health_counts = df2['health'].value_counts()

    fig, ax = styled_fig()

    ax.pie(
        health_counts.values,
        labels=health_counts.index,
        autopct='%1.1f%%',
        colors=CHART_PALETTE,
        textprops={'color': TEXT_MAIN}
    )

    st.pyplot(fig)

with col4:

    st.subheader("4. Trunk Diameter Distribution")

    fig, ax = styled_fig()

    sns.histplot(
        df2['tree_dbh'],
        bins=30,
        kde=True,
        ax=ax,
        color=SAGA_GREEN
    )

    ax.set_xlabel("Diameter (inches)")

    st.pyplot(fig)

# ---------------------------------------------------------
# 5 + 6
# ---------------------------------------------------------
col5, col6 = st.columns(2)

with col5:

    st.subheader("5. Health by Borough")

    health_boro = (
        df2.groupby(['boroname', 'health'])
        .size()
        .unstack(fill_value=0)
    )

    fig, ax = styled_fig()

    health_boro.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=CHART_PALETTE
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

with col6:

    st.subheader("6. Diameter vs Health")

    fig, ax = styled_fig()

    sns.boxplot(
        data=df2,
        x='health',
        y='tree_dbh',
        ax=ax,
        palette=CHART_PALETTE
    )

    st.pyplot(fig)

# ---------------------------------------------------------
# 7 + 8
# ---------------------------------------------------------
col7, col8 = st.columns(2)

with col7:

    st.subheader("7. Status Breakdown")

    status_counts = df2['status'].value_counts()

    fig, ax = styled_fig()

    sns.barplot(
        x=status_counts.values,
        y=status_counts.index,
        ax=ax,
        palette=CHART_PALETTE
    )

    st.pyplot(fig)

with col8:

    st.subheader("8. Species Diversity by Borough")

    diversity = (
        df2.groupby('boroname')['spc_common']
        .nunique()
        .sort_values(ascending=False)
    )

    fig, ax = styled_fig()

    sns.barplot(
        x=diversity.values,
        y=diversity.index,
        ax=ax,
        palette=CHART_PALETTE
    )

    st.pyplot(fig)

# ---------------------------------------------------------
# 9 + 10
# ---------------------------------------------------------
col9, col10 = st.columns(2)

with col9:

    st.subheader("9. Top Species by Avg Diameter")

    avg_dbh = (
        df2.groupby('spc_common')['tree_dbh']
        .mean()
        .nlargest(10)
    )

    fig, ax = styled_fig()

    sns.barplot(
        x=avg_dbh.values,
        y=avg_dbh.index,
        ax=ax,
        palette=CHART_PALETTE
    )

    st.pyplot(fig)

with col10:

    st.subheader("10. Health % by Species")

    top_10 = (
        df2['spc_common']
        .value_counts()
        .head(10)
        .index
    )

    health_pct = (
        df2[df2['spc_common'].isin(top_10)]
        .groupby('spc_common')['health']
        .value_counts(normalize=True)
        .unstack()
        .fillna(0) * 100
    )

    fig, ax = styled_fig()

    health_pct.plot(
        kind='barh',
        stacked=True,
        ax=ax,
        color=CHART_PALETTE
    )

    ax.legend(
        title="Health",
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )

    st.pyplot(fig)

# =========================================================
# DATA TABLE
# =========================================================
st.divider()

st.subheader("📋 Sample of Filtered Data")

display_cols = [
    'spc_common',
    'boroname',
    'tree_dbh',
    'health',
    'status'
]

st.dataframe(
    df2[display_cols]
    .sample(min(100, len(df2)))
    .reset_index(drop=True),

    use_container_width=True,
    height=350
)

# =========================================================
# FOOTER
# =========================================================
st.markdown(f"""
<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */
html, body, [data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(circle at top left, #2b1d16 0%, {BG_MAIN} 45%);
    color: {TEXT_MAIN};
    font-family: 'Inter', sans-serif;
}}

/* Main container */
.block-container {{
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}}

/* ===================================================== */
/* STREAMLIT TOP HEADER */
/* ===================================================== */
header[data-testid="stHeader"] {{
    background: rgba(18, 11, 8, 0.88) !important;
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}

/* Toolbar buttons */
button[kind="header"],
[data-testid="baseButton-headerNoPadding"],
[data-testid="stToolbar"] button {{
    color: white !important;
}}

/* Toolbar icons */
[data-testid="stToolbar"] svg,
button[kind="header"] svg {{
    fill: white !important;
}}

/* Toolbar hover */
[data-testid="stToolbar"] button:hover {{
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 8px;
}}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */
[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {BG_SIDEBAR} 0%,
        #261812 100%
    ) !important;

    border-right: 2px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {SAGA_GREEN} !important;
    font-weight: 700;
}}

[data-testid="stSidebar"] label {{
    color: {TEXT_MAIN} !important;
    font-weight: 600;
}}

[data-testid="stSidebar"] .stMarkdown p {{
    color: {TEXT_DIM} !important;
}}

/* ===================================================== */
/* TITLE */
/* ===================================================== */
h1 {{
    color: {SAGA_GREEN} !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;

    text-shadow:
        0 0 8px rgba(46,196,182,0.35),
        0 0 22px rgba(46,196,182,0.15);
}}

h2, h3 {{
    color: {GOLD_LIGHT} !important;
    font-weight: 700 !important;
}}

/* ===================================================== */
/* INFO / ALERT BOX */
/* ===================================================== */
[data-testid="stAlert"] {{
    background: linear-gradient(
        135deg,
        rgba(46,196,182,0.12),
        rgba(255,183,3,0.08)
    ) !important;

    border: 1px solid rgba(46,196,182,0.4) !important;

    border-radius: 16px;
    backdrop-filter: blur(6px);

    color: {TEXT_MAIN} !important;
}}

/* ===================================================== */
/* METRIC CARDS */
/* ===================================================== */
[data-testid="metric-container"] {{
    background:
        linear-gradient(
            145deg,
            rgba(59,36,26,0.95),
            rgba(36,23,18,0.98)
        );

    border: 1px solid rgba(255,255,255,0.08);

    border-left: 5px solid {SAGA_GREEN};

    border-radius: 18px;

    padding: 1.2rem;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.35),
        0 0 0 1px rgba(46,196,182,0.05);

    transition: 0.3s ease;
}}

[data-testid="metric-container"]:hover {{
    transform: translateY(-3px);

    box-shadow:
        0 12px 28px rgba(0,0,0,0.45),
        0 0 18px rgba(46,196,182,0.18);
}}

[data-testid="metric-container"] label {{
    color: {TEXT_DIM} !important;
    font-size: 0.9rem !important;
}}

[data-testid="stMetricValue"] {{
    color: {CREAM} !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}

/* ===================================================== */
/* BUTTONS */
/* ===================================================== */
.stButton > button {{
    background: linear-gradient(
        135deg,
        {SAGA_GREEN},
        {SAGA_GREEN_DARK}
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    font-weight: 700 !important;

    padding: 0.6rem 1rem !important;

    box-shadow:
        0 4px 14px rgba(46,196,182,0.35);

    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: scale(1.03);

    box-shadow:
        0 6px 18px rgba(46,196,182,0.5);
}}

/* ===================================================== */
/* MULTISELECT TAGS */
/* ===================================================== */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background: linear-gradient(
        135deg,
        {SAGA_GREEN_DARK},
        {SAGA_GREEN}
    ) !important;

    color: white !important;

    border-radius: 8px !important;

    border: none !important;

    font-weight: 600;
}}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
    color: white !important;
}}

/* ===================================================== */
/* INPUTS */
/* ===================================================== */
div[data-baseweb="select"] > div {{
    background-color: {BG_CARD} !important;

    border: 1px solid {BORDER} !important;

    border-radius: 10px !important;
}}

/* ===================================================== */
/* SLIDER */
/* ===================================================== */
.stSlider > div > div > div > div {{
    background: linear-gradient(
        90deg,
        {SAGA_GREEN},
        {GOLD}
    ) !important;
}}

/* ===================================================== */
/* DATAFRAME */
/* ===================================================== */
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        0 8px 22px rgba(0,0,0,0.3);
}}

/* ===================================================== */
/* CAPTION */
/* ===================================================== */
.stCaption {{
    color: {TEXT_DIM} !important;
    font-style: italic;
}}

/* ===================================================== */
/* CHART CONTAINERS */
/* ===================================================== */
.element-container:has(canvas) {{
    background: linear-gradient(
        145deg,
        rgba(59,36,26,0.85),
        rgba(36,23,18,0.95)
    );

    padding: 1rem;

    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        0 8px 24px rgba(0,0,0,0.35);

    margin-bottom: 1rem;
}}

/* ===================================================== */
/* DIVIDER */
/* ===================================================== */
hr {{
    border-color: rgba(255,255,255,0.08);
}}

</style>
""", unsafe_allow_html=True)