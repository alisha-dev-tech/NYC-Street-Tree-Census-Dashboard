import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Color scheme: Light Brown & Sage Green
COLORS = {
    'light_brown': '#D4A574',
    'sage_green': '#9CAF88',
    'dark_brown': '#8B7355',
    'light_sage': '#C2D4C8',
    'pale_brown': '#E8D4C0'
}

# Gradient colors for charts
GRADIENT_COLORS = ['#9CAF88', '#B0C299', '#C5D5A8', '#D4A574', '#E8D4C0']

def create_pie_chart(df):
    """Pie Chart: Proportional distribution of trees across boroughs"""
    borough_counts = df['borough'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=borough_counts.index,
        values=borough_counts.values,
        marker=dict(colors=GRADIENT_COLORS),
        hovertemplate='<b>%{label}</b><br>Trees: %{value:,}<br>Percentage: %{percent}<extra></extra>',
        textposition='auto',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Tree Distribution by Borough</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=20, r=20, t=60, b=20),
        height=400
    )
    return fig

def create_histogram(df):
    """Histogram: Frequency distribution of tree diameter (DBH)"""
    fig = go.Figure(data=[go.Histogram(
        x=df['tree_dbh'],
        nbinsx=40,
        marker=dict(
            color=COLORS['sage_green'],
            line=dict(color=COLORS['dark_brown'], width=1)
        ),
        hovertemplate='<b>Diameter Range</b><br>%{x} inches<br>Count: %{y:,}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Tree Diameter Distribution (DBH)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Diameter at Breast Height (inches)',
        yaxis_title='Frequency',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        showlegend=False
    )
    return fig

def create_line_chart(df):
    """Line Chart: Trends in tree planting over time (cumulative)"""
    if df['created_at'].isna().all():
        return go.Figure().add_annotation(text="No date data available")
    
    df_sorted = df.dropna(subset=['created_at']).sort_values('created_at')
    cumulative_counts = df_sorted.groupby('created_at').size().cumsum()
    
    fig = go.Figure(data=[go.Scatter(
        x=cumulative_counts.index,
        y=cumulative_counts.values,
        mode='lines+markers',
        name='Cumulative Trees',
        line=dict(color=COLORS['sage_green'], width=3),
        marker=dict(size=6, color=COLORS['sage_green']),
        fill='tozeroy',
        fillcolor='rgba(156, 175, 136, 0.2)',
        hovertemplate='<b>Date: %{x|%b %d, %Y}</b><br>Cumulative Trees: %{y:,}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Cumulative Tree Planting Trend Over Time</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Date',
        yaxis_title='Cumulative Tree Count',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        hovermode='x unified'
    )
    return fig

def create_bar_chart(df):
    """Bar Chart: Comparison of values across categories (Top 10 species)"""
    top_species = df['spc_common'].value_counts().head(10)
    
    fig = go.Figure(data=[go.Bar(
        y=top_species.index,
        x=top_species.values,
        orientation='h',
        marker=dict(
            color=GRADIENT_COLORS,
            line=dict(color=COLORS['dark_brown'], width=1)
        ),
        text=top_species.values,
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Top 10 Most Common Tree Species</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Tree Count',
        yaxis_title='Species',
        font=dict(size=11, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=200, r=20, t=60, b=60),
        height=400,
        showlegend=False
    )
    return fig

def create_scatter_plot(df):
    """Scatter Plot: Relationship between tree diameter and health status"""
    fig = go.Figure()
    
    health_categories = df['health'].dropna().unique()
    colors_dict = {health: GRADIENT_COLORS[i % len(GRADIENT_COLORS)] 
                   for i, health in enumerate(sorted(health_categories))}
    
    for health in sorted(health_categories):
        health_data = df[df['health'] == health]
        fig.add_trace(go.Scatter(
            x=health_data['tree_dbh'],
            y=health_data['health'],
            mode='markers',
            name=health,
            marker=dict(
                size=8,
                color=colors_dict[health],
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>Health: %{y}</b><br>Diameter: %{x} inches<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>Tree Diameter vs Health Status</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Diameter at Breast Height (inches)',
        yaxis_title='Health Status',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=100, r=20, t=60, b=60),
        height=400,
        hovermode='closest',
        legend=dict(x=1.05, y=1)
    )
    return fig

def create_box_plot(df):
    """Box Plot: Data spread, median, and outliers by borough"""
    fig = go.Figure()
    
    for i, borough in enumerate(sorted(df['borough'].dropna().unique())):
        borough_data = df[df['borough'] == borough]['tree_dbh']
        fig.add_trace(go.Box(
            y=borough_data,
            name=borough,
            marker=dict(color=GRADIENT_COLORS[i % len(GRADIENT_COLORS)]),
            boxmean='sd',
            hovertemplate='<b>%{fullData.name}</b><br>DBH: %{y} inches<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>Tree Diameter Distribution by Borough (Box Plot)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        yaxis_title='Diameter at Breast Height (inches)',
        xaxis_title='Borough',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        showlegend=False
    )
    return fig

def create_heatmap(df):
    """Heatmap: Correlation matrix of numerical features"""
    # Select numerical columns
    numerical_cols = ['tree_dbh', 'latitude', 'longitude']
    corr_matrix = df[numerical_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale=[
            [0, '#C2D4C8'],
            [0.5, '#D4A574'],
            [1, '#8B7355']
        ],
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 12},
        hovertemplate='%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>',
        colorbar=dict(title="Correlation", thickness=20, len=0.7)
    ))
    
    fig.update_layout(
        title={
            'text': '<b>Feature Correlation Matrix</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=100, r=100, t=60, b=100),
        height=400,
        xaxis={'side': 'bottom'}
    )
    return fig

def create_area_chart(df):
    """Area Chart: Cumulative trends of health status over time"""
    if df['created_at'].isna().all():
        return go.Figure().add_annotation(text="No date data available")
    
    df_sorted = df.dropna(subset=['created_at']).sort_values('created_at')
    health_timeline = df_sorted.groupby(['created_at', 'health']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    health_categories = health_timeline.columns
    colors_dict = {health: GRADIENT_COLORS[i % len(GRADIENT_COLORS)] 
                   for i, health in enumerate(sorted(health_categories))}
    
    for health in sorted(health_categories):
        fig.add_trace(go.Scatter(
            x=health_timeline.index,
            y=health_timeline[health],
            mode='lines',
            name=health,
            stackgroup='one',
            line=dict(width=0.5, color=colors_dict[health]),
            fillcolor=colors_dict[health],
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%b %d}<br>Count: %{y:,}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>Health Status Trends Over Time (Stacked Area)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Date',
        yaxis_title='Tree Count',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        hovermode='x unified'
    )
    return fig

def create_count_plot(df):
    """Count Plot: Frequency count of categorical variables (Health Status)"""
    health_counts = df['health'].value_counts().sort_values(ascending=False)
    
    fig = go.Figure(data=[go.Bar(
        x=health_counts.index,
        y=health_counts.values,
        marker=dict(
            color=GRADIENT_COLORS,
            line=dict(color=COLORS['dark_brown'], width=2)
        ),
        text=health_counts.values,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y:,}<br>Percentage: %{customdata:.1f}%<extra></extra>',
        customdata=[v/health_counts.sum()*100 for v in health_counts.values]
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Tree Count by Health Status</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        xaxis_title='Health Status',
        yaxis_title='Number of Trees',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        showlegend=False
    )
    return fig

def create_violin_plot(df):
    """Violin Plot: Distribution and probability density by health status"""
    fig = go.Figure()
    
    for i, health in enumerate(sorted(df['health'].dropna().unique())):
        health_data = df[df['health'] == health]['tree_dbh']
        fig.add_trace(go.Violin(
            y=health_data,
            name=health,
            box_visible=True,
            meanline_visible=True,
            points=False,
            line_color=GRADIENT_COLORS[i % len(GRADIENT_COLORS)],
            fillcolor=GRADIENT_COLORS[i % len(GRADIENT_COLORS)],
            opacity=0.7,
            hovertemplate='<b>%{fullData.name}</b><br>DBH: %{y} inches<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>Tree Diameter Distribution by Health Status (Violin Plot)</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#6B5344'}
        },
        yaxis_title='Diameter at Breast Height (inches)',
        xaxis_title='Health Status',
        font=dict(size=12, color='#6B5344'),
        plot_bgcolor='rgba(250, 250, 248, 0.5)',
        paper_bgcolor='#FFFBF7',
        margin=dict(l=60, r=20, t=60, b=60),
        height=400,
        showlegend=False
    )
    return fig

def create_all_charts(df):
    """Create all 10 required charts"""
    return {
        'pie': create_pie_chart(df),
        'histogram': create_histogram(df),
        'line': create_line_chart(df),
        'bar': create_bar_chart(df),
        'scatter': create_scatter_plot(df),
        'box': create_box_plot(df),
        'heatmap': create_heatmap(df),
        'area': create_area_chart(df),
        'count': create_count_plot(df),
        'violin': create_violin_plot(df)
    }

def create_kpi_cards(df):
    """Generate KPI summary cards"""
    return {
        'total_trees': len(df),
        'avg_diameter': df['tree_dbh'].mean(),
        'healthy_percentage': (len(df[df['health'] == 'Good']) / len(df) * 100) if len(df) > 0 else 0,
        'alive_percentage': (len(df[df['status'] == 'Alive']) / len(df) * 100) if len(df) > 0 else 0,
        'total_species': df['spc_common'].nunique()
    }
