import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ---------------- SAGA GREEN THEME ----------------
st.set_page_config(
    page_title="NYC Trees Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌳"
)

SAGA_GREEN = "#2a9d8f"
SAGA_LIGHT = "#34c759"
BG_DARK = "#1a1a1a"
BG_LIGHT = "#2a2a2a"

st.markdown(f"""
<style>
body {{background-color: {BG_DARK}; color: #ffffff;}}
.block-container {{padding: 1rem;}}
.stMarkdown {{color: #ffffff;}}
[data-testid="stSidebar"] {{background-color: {BG_LIGHT};}}
.stButton>button {{background-color: {SAGA_GREEN}; color: white; border: none;}}
.stButton>button:hover {{background-color: {SAGA_LIGHT};}}
h1, h2, h3 {{color: {SAGA_GREEN};}}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/trees.csv", low_memory=False)
    except FileNotFoundError:
        st.error("❌ CSV file not found! Make sure 'data/trees.csv' is uploaded to your GitHub repo.")
        st.stop()
    
    # Show actual columns for debugging
    st.sidebar.write("**CSV Columns:**", list(df.columns)[:10])
    
    # اب borough, boro_name, boroname تینوں handle ہوں گے
    if 'boro_name' in df.columns:
        df = df.rename(columns={'boro_name': 'boroname'})
    elif 'borough' in df.columns:
        df = df.rename(columns={'borough': 'boroname'})
    elif 'boroname' not in df.columns:
        st.error(f"❌ No borough column found! Available columns: {list(df.columns)}")
        st.stop()
    
    df['tree_dbh'] = pd.to_numeric(df['tree_dbh'], errors='coerce')
    df['spc_common'] = df['spc_common'].fillna('Unknown')
    df['boroname'] = df['boroname'].fillna('Unknown')
    df['health'] = df['health'].fillna('Unknown')
    df['status'] = df['status'].fillna('Unknown')
    df = df.dropna(subset=['tree_dbh', 'spc_common', 'boroname'])
    return df
df = load_data()

st.title("🌳 NYC Street Trees Dashboard")
st.markdown("**Explore the NYC Tree Census dataset.** Use sidebar filters to narrow down data.")

# باقی کا سارا کوڈ ویسا ہی رہے گا جیسا میں نے پچھلی بار دیا تھا...
# ... آپ کا پورا 10 charts والا کوڈ یہاں paste کر دیں ...

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")
boroughs = st.sidebar.multiselect("Select Borough", sorted(df['boroname'].unique()), default=sorted(df['boroname'].unique()))
health = st.sidebar.multiselect("Tree Health", sorted(df['health'].unique()), default=sorted(df['health'].unique()))
status = st.sidebar.multiselect("Tree Status", sorted(df['status'].unique()), default=sorted(df['status'].unique()))

dbh_min, dbh_max = float(df['tree_dbh'].min()), float(df['tree_dbh'].max())
dbh_range = st.sidebar.slider("Trunk Diameter (inches)", dbh_min, dbh_max, (dbh_min, dbh_max))

df2 = df[
    (df['boroname'].isin(boroughs)) &
    (df['health'].isin(health)) &
    (df['status'].isin(status)) &
    (df['tree_dbh'] >= dbh_range[0]) &
    (df['tree_dbh'] <= dbh_range[1])
].copy()

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

st.info(f"**Active Filters:** {len(df2):,} trees selected")

if df2.empty:
    st.warning("No trees match current filters. Adjust sidebar.")
    st.stop()

# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trees", f"{len(df2):,}")
col2.metric("Unique Species", f"{df2['spc_common'].nunique():,}")
col3.metric("Avg Trunk Diameter", f"{df2['tree_dbh'].mean():.1f}\"")
col4.metric("Boroughs", f"{df2['boroname'].nunique()}")

st.divider()

# ---------------- 10 CHARTS WITH DESCRIPTIONS ----------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Trees by Borough")
    borough_counts = df2['boroname'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=borough_counts.values, y=borough_counts.index, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*Queens and Brooklyn have the most street trees. Manhattan has fewer due to dense buildings.*")

with col2:
    st.subheader("2. Top 10 Tree Species")
    top_species = df2['spc_common'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=top_species.values, y=top_species.index, ax=ax, color=SAGA_LIGHT)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*London Plane and Honey Locust are the most common NYC street trees.*")

col3, col4 = st.columns(2)
with col3:
    st.subheader("3. Tree Health Distribution")
    health_counts = df2['health'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(health_counts.values, labels=health_counts.index, autopct='%1.1f%%', colors=[SAGA_GREEN, SAGA_LIGHT, "#e9c46a"])
    st.pyplot(fig); plt.close()
    st.caption("*Most trees are rated Good health. Dead trees are a small fraction.*")

with col4:
    st.subheader("4. Trunk Diameter Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df2['tree_dbh'], bins=30, kde=True, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Most trees have 10-20 inch trunk diameter. Older trees have >30 inch trunks.*")

col5, col6 = st.columns(2)
with col5:
    st.subheader("5. Health by Borough")
    health_boro = df2.groupby(['boroname', 'health']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 4))
    health_boro.plot(kind='bar', stacked=True, ax=ax, color=[SAGA_GREEN, SAGA_LIGHT, "#e9c46a"])
    ax.set_ylabel("Count"); ax.legend(title="Health")
    plt.xticks(rotation=45)
    st.pyplot(fig); plt.close()
    st.caption("*Health distribution varies by borough. Staten Island has highest % of Good trees.*")

with col6:
    st.subheader("6. Diameter vs Health")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df2, x='health', y='tree_dbh', ax=ax, palette=[SAGA_GREEN, SAGA_LIGHT, "#e9c46a"])
    ax.set_xlabel("Health"); ax.set_ylabel("Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Good health trees tend to have larger diameters. Poor health trees are often smaller/younger.*")

col7, col8 = st.columns(2)
with col7:
    st.subheader("7. Status Breakdown")
    status_counts = df2['status'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=status_counts.values, y=status_counts.index, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Count")
    st.pyplot(fig); plt.close()
    st.caption("*Alive = planted and surviving. Stump = removed tree. Dead = standing dead tree.*")

with col8:
    st.subheader("8. Species Diversity by Borough")
    diversity = df2.groupby('boroname')['spc_common'].nunique().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=diversity.values, y=diversity.index, ax=ax, color=SAGA_LIGHT)
    ax.set_xlabel("Number of Species")
    st.pyplot(fig); plt.close()
    st.caption("*Manhattan has highest species diversity despite fewer total trees.*")

col9, col10 = st.columns(2)
with col9:
    st.subheader("9. Top 10 Species by Avg Diameter")
    avg_dbh = df2.groupby('spc_common')['tree_dbh'].mean().nlargest(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=avg_dbh.values, y=avg_dbh.index, ax=ax, color=SAGA_GREEN)
    ax.set_xlabel("Avg Diameter (inches)")
    st.pyplot(fig); plt.close()
    st.caption("*Oaks and Ginkgos grow largest. Smaller species like Crabapple have lower avg diameter.*")

with col10:
    st.subheader("10. Health % by Species")
    top_10 = df2['spc_common'].value_counts().head(10).index
    health_pct = df2[df2['spc_common'].isin(top_10)].groupby('spc_common')['health'].value_counts(normalize=True).unstack().fillna(0)*100
    fig, ax = plt.subplots(figsize=(6, 4))
    health_pct.plot(kind='barh', stacked=True, ax=ax, color=[SAGA_GREEN, SAGA_LIGHT, "#e9c46a"])
    ax.set_xlabel("Percentage")
    plt.legend(title="Health", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig); plt.close()
    st.caption("*Some species like Ginkgo have very high Good health %. Others like Elm have more Poor trees.*")

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Sample of Filtered Data")
display_cols = ['spc_common', 'boroname', 'tree_dbh', 'health', 'status']
st.dataframe(df2[display_cols].sample(min(100, len(df2))).reset_index(drop=True), use_container_width=True, height=300)