import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ---------------- SAGA GREEN + BROWN THEME ----------------
st.set_page_config(
    page_title="NYC Trees Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌳"
)

SAGA_GREEN   = "#2a9d8f"
SAGA_GREEN2  = "#21867a"
BROWN_DARK   = "#4a3728"
BROWN_MID    = "#6b4f3a"
BROWN_LIGHT  = "#8b6f5e"
CREAM        = "#f5f0eb"
BG_DARK      = "#1c1410"      # very dark brown-black background
BG_SIDEBAR   = "#2a1f18"      # dark brown sidebar
BG_CARD      = "#3a2a20"      # card background
TEXT_MAIN    = "#f0e6d3"      # warm cream text
TEXT_DIM     = "#c4a882"      # dimmed warm text
ACCENT       = "#e8b86d"      # golden brown accent

st.markdown(f"""
<style>
/* ---- Global ---- */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {BG_DARK};
    color: {TEXT_MAIN};
    font-family: 'Georgia', serif;
}}

/* ---- Main block ---- */
.block-container {{
    padding: 1.5rem 2rem;
    background-color: {BG_DARK};
}}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {{
    background-color: {BG_SIDEBAR} !important;
    border-right: 2px solid {BROWN_MID};
}}
[data-testid="stSidebar"] * {{
    color: {TEXT_MAIN} !important;
}}
[data-testid="stSidebar"] .stMarkdown p {{
    color: {TEXT_DIM} !important;
    font-size: 0.85rem;
}}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {SAGA_GREEN} !important;
}}

/* ---- Sidebar header label ---- */
[data-testid="stSidebar"] label {{
    color: {TEXT_MAIN} !important;
    font-weight: 600;
}}

/* ---- Multiselect tags — fix invisible text ---- */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background-color: {BROWN_MID} !important;
    color: {CREAM} !important;
    border: 1px solid {SAGA_GREEN} !important;
    border-radius: 4px;
}}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {{
    color: {CREAM} !important;
}}
/* X button in tags */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] [role="presentation"] svg {{
    fill: {CREAM} !important;
}}

/* ---- Multiselect dropdown input ---- */
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
    background-color: {BG_CARD} !important;
    border: 1px solid {BROWN_MID} !important;
    color: {TEXT_MAIN} !important;
}}

/* ---- Slider ---- */
[data-testid="stSlider"] label {{
    color: {TEXT_MAIN} !important;
}}
[data-testid="stSlider"] div[data-testid="stTickBar"] {{
    color: {TEXT_DIM} !important;
}}
.stSlider > div > div > div > div {{
    background-color: {SAGA_GREEN} !important;
}}

/* ---- Headings ---- */
h1 {{ color: {SAGA_GREEN} !important; font-size: 2.2rem; }}
h2, h3 {{ color: {ACCENT} !important; }}

/* ---- Metrics ---- */
[data-testid="metric-container"] {{
    background-color: {BG_CARD};
    border: 1px solid {BROWN_MID};
    border-left: 4px solid {SAGA_GREEN};
    border-radius: 8px;
    padding: 0.8rem 1rem;
}}
[data-testid="metric-container"] label {{
    color: {TEXT_DIM} !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {CREAM} !important;
    font-size: 1.8rem;
}}

/* ---- Info / success / warning boxes ---- */
[data-testid="stAlert"] {{
    background-color: {BG_CARD} !important;
    border: 1px solid {BROWN_MID} !important;
    color: {TEXT_MAIN} !important;
    border-radius: 6px;
}}

/* ---- Divider ---- */
hr {{ border-color: {BROWN_MID}; }}

/* ---- Buttons ---- */
.stButton > button {{
    background-color: {SAGA_GREEN} !important;
    color: {CREAM} !important;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: 0.5px;
}}
.stButton > button:hover {{
    background-color: {SAGA_GREEN2} !important;
    color: #ffffff !important;
}}

/* ---- Dataframe ---- */
[data-testid="stDataFrame"] {{
    background-color: {BG_CARD};
    border: 1px solid {BROWN_MID};
    border-radius: 6px;
}}

/* ---- Caption ---- */
.stCaption, [data-testid="stCaptionContainer"] p {{
    color: {TEXT_DIM} !important;
    font-style: italic;
    font-size: 0.82rem;
}}

/* ---- Sidebar subheader spacing ---- */
[data-testid="stSidebar"] h3 {{
    margin-top: 1rem;
    font-size: 0.95rem;
    border-bottom: 1px solid {BROWN_MID};
    padding-bottom: 3px;
}}
</style>
""", unsafe_allow_html=True)

# Set matplotlib to match theme
plt.rcParams.update({
    'figure.facecolor': '#3a2a20',
    'axes.facecolor':   '#3a2a20',
    'axes.edgecolor':   '#6b4f3a',
    'axes.labelcolor':  '#f0e6d3',
    'xtick.color':      '#c4a882',
    'ytick.color':      '#c4a882',
    'text.color':       '#f0e6d3',
    'grid.color':       '#4a3728',
    'grid.alpha':       0.4,
})

# Color palettes for charts
CHART_PALETTE = [SAGA_GREEN, ACCENT, BROWN_LIGHT, "#e07a5f", "#81b29a", "#f2cc8f", "#3d405b"]

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/trees.csv", low_memory=False)
    except FileNotFoundError:
        st.error("❌ CSV file not found! Make sure 'data/trees.csv' is in your GitHub repo.")
        st.stop()

    if 'boro_name' in df.columns:
        df = df.rename(columns={'boro_name': 'boroname'})
    elif 'borough' in df.columns:
        df = df.rename(columns={'borough': 'boroname'})
    elif 'boroname' not in df.columns:
        st.error(f"❌ No borough column found! Available: {list(df.columns)}")
        st.stop()

    df['tree_dbh']   = pd.to_numeric(df['tree_dbh'], errors='coerce')
    df['spc_common'] = df['spc_common'].fillna('Unknown')
    df['boroname']   = df['boroname'].fillna('Unknown')
    df['health']     = df['health'].fillna('Unknown')
    df['status']     = df['status'].fillna('Unknown')
    df = df.dropna(subset=['tree_dbh', 'spc_common', 'boroname'])
    return df

df = load_data()

# ---------------- HEADER ----------------
st.title("🌳 NYC Street Trees Dashboard")
st.markdown(f"<p style='color:{TEXT_DIM}; font-size:1rem;'>Explore the NYC Tree Census dataset. Use sidebar filters to narrow down data.</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")
st.sidebar.markdown(f"<p style='color:{TEXT_DIM}'>All filters apply to all charts simultaneously.</p>", unsafe_allow_html=True)

st.sidebar.subheader("🏙️ Borough")
boroughs = st.sidebar.multiselect(
    "Select Borough",
    sorted(df['boroname'].unique()),
    default=sorted(df['boroname'].unique())
)

st.sidebar.subheader("🌿 Tree Health")
health = st.sidebar.multiselect(
    "Tree Health",
    sorted(df['health'].unique()),
    default=sorted(df['health'].unique())
)

st.sidebar.subheader("📋 Tree Status")
status = st.sidebar.multiselect(
    "Tree Status",
    sorted(df['status'].unique()),
    default=sorted(df['status'].unique())
)

st.sidebar.subheader("📏 Trunk Diameter (inches)")
dbh_min, dbh_max = float(df['tree_dbh'].min()), float(df['tree_dbh'].max())
dbh_range = st.sidebar.slider("Diameter Range", dbh_min, dbh_max, (dbh_min, dbh_max))

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

# ---------------- APPLY FILTERS ----------------
df2 = df[
    (df['boroname'].isin(boroughs)) &
    (df['health'].isin(health)) &
    (df['status'].isin(status)) &
    (df['tree_dbh'] >= dbh_range[0]) &
    (df['tree_dbh'] <= dbh_range[1])
].copy()

st.info(f"**Active Filters:** {len(df2):,} trees selected")

if df2.empty:
    st.warning("⚠️ No trees match current filters. Adjust sidebar.")
    st.stop()

# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trees",        f"{len(df2):,}")
col2.metric("Unique Species",     f"{df2['spc_common'].nunique():,}")
col3.metric("Avg Trunk Diameter", f"{df2['tree_dbh'].mean():.1f}\"")
col4.metric("Boroughs",           f"{df2['boroname'].nunique()}")

st.divider()

# ---------------- CHART HELPER ----------------
def styled_fig(w=6, h=4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor('#3a2a20')
    ax.set_facecolor('#3a2a20')
    return fig, ax

# ---------------- 10 CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Trees by Borough")
    borough_counts = df2['boroname'].value_counts()
    fig, ax = styled_fig()
    sns.barplot(x=borough_counts.values, y=borough_counts.index, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*Queens and Brooklyn have the most street trees. Manhattan has fewer due to dense buildings.*")

with col2:
    st.subheader("2. Top 10 Tree Species")
    top_species = df2['spc_common'].value_counts().head(10)
    fig, ax = styled_fig()
    sns.barplot(x=top_species.values, y=top_species.index, ax=ax, color=ACCENT)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*London Plane and Honey Locust are the most common NYC street trees.*")

col3, col4 = st.columns(2)

with col3:
    st.subheader("3. Tree Health Distribution")
    health_counts = df2['health'].value_counts()
    fig, ax = styled_fig()
    ax.pie(
        health_counts.values,
        labels=health_counts.index,
        autopct='%1.1f%%',
        colors=[SAGA_GREEN, ACCENT, BROWN_LIGHT, "#e07a5f"],
        textprops={'color': TEXT_MAIN}
    )
    st.pyplot(fig); plt.close()
    st.caption("*Most trees are rated Good health. Dead trees are a small fraction.*")

with col4:
    st.subheader("4. Trunk Diameter Distribution")
    fig, ax = styled_fig()
    sns.histplot(df2['tree_dbh'], bins=30, kde=True, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Most trees have 10–20 inch trunk diameter. Older trees have >30 inch trunks.*")

col5, col6 = st.columns(2)

with col5:
    st.subheader("5. Health by Borough")
    health_boro = df2.groupby(['boroname', 'health']).size().unstack(fill_value=0)
    fig, ax = styled_fig()
    health_boro.plot(kind='bar', stacked=True, ax=ax,
                     color=[SAGA_GREEN, ACCENT, BROWN_LIGHT, "#e07a5f"])
    ax.set_ylabel("Count")
    ax.legend(title="Health", facecolor='#3a2a20', labelcolor=TEXT_MAIN)
    plt.xticks(rotation=45)
    st.pyplot(fig); plt.close()
    st.caption("*Health distribution varies by borough. Staten Island has highest % of Good trees.*")

with col6:
    st.subheader("6. Diameter vs Health")
    fig, ax = styled_fig()
    sns.boxplot(data=df2, x='health', y='tree_dbh', ax=ax,
                palette=[SAGA_GREEN, ACCENT, BROWN_LIGHT, "#e07a5f"])
    ax.set_xlabel("Health")
    ax.set_ylabel("Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Good health trees tend to have larger diameters. Poor health trees are often smaller/younger.*")

col7, col8 = st.columns(2)

with col7:
    st.subheader("7. Status Breakdown")
    status_counts = df2['status'].value_counts()
    fig, ax = styled_fig()
    sns.barplot(x=status_counts.values, y=status_counts.index, ax=ax, color=BROWN_LIGHT)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*Alive = planted and surviving. Stump = removed tree. Dead = standing dead tree.*")

with col8:
    st.subheader("8. Species Diversity by Borough")
    diversity = df2.groupby('boroname')['spc_common'].nunique().sort_values(ascending=False)
    fig, ax = styled_fig()
    sns.barplot(x=diversity.values, y=diversity.index, ax=ax, color=ACCENT)
    ax.set_xlabel("Number of Species")
    st.pyplot(fig); plt.close()
    st.caption("*Manhattan has highest species diversity despite fewer total trees.*")

col9, col10 = st.columns(2)

with col9:
    st.subheader("9. Top 10 Species by Avg Diameter")
    avg_dbh = df2.groupby('spc_common')['tree_dbh'].mean().nlargest(10)
    fig, ax = styled_fig()
    sns.barplot(x=avg_dbh.values, y=avg_dbh.index, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Avg Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Oaks and Ginkgos grow largest. Smaller species like Crabapple have lower avg diameter.*")

with col10:
    st.subheader("10. Health % by Species")
    top_10 = df2['spc_common'].value_counts().head(10).index
    health_pct = (
        df2[df2['spc_common'].isin(top_10)]
        .groupby('spc_common')['health']
        .value_counts(normalize=True)
        .unstack()
        .fillna(0) * 100
    )
    fig, ax = styled_fig()
    health_pct.plot(kind='barh', stacked=True, ax=ax,
                    color=[SAGA_GREEN, ACCENT, BROWN_LIGHT, "#e07a5f"])
    ax.set_xlabel("Percentage")
    ax.legend(title="Health", bbox_to_anchor=(1.05, 1), loc='upper left',
              facecolor='#3a2a20', labelcolor=TEXT_MAIN)
    st.pyplot(fig); plt.close()
    st.caption("*Some species like Ginkgo have very high Good health %. Others like Elm have more Poor trees.*")

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Sample of Filtered Data")
display_cols = ['spc_common', 'boroname', 'tree_dbh', 'health', 'status']
st.dataframe(
    df2[display_cols].sample(min(100, len(df2))).reset_index(drop=True),
    use_container_width=True,
    height=300
)