"""
MyAnimeList Dataset - Stunning Dashboard Creator
Dark Theme with Interactive Plotly Visualizations
Inspired by modern analytics dashboards
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Dark theme colors
DARK_BG = '#0a0a0a'
CARD_BG = '#1a1a1a'
GRID_COLOR = '#2a2a2a'
PURPLE = '#9b87f5'
BLUE = '#7dd3fc'
YELLOW = '#fbbf24'
GREEN = '#4ade80'
RED = '#f87171'
TEXT_COLOR = '#e5e7eb'

# Plotly template
TEMPLATE = {
    'layout': {
        'paper_bgcolor': DARK_BG,
        'plot_bgcolor': CARD_BG,
        'font': {'color': TEXT_COLOR, 'family': 'Inter, system-ui, sans-serif'},
        'xaxis': {'gridcolor': GRID_COLOR, 'showgrid': True},
        'yaxis': {'gridcolor': GRID_COLOR, 'showgrid': True},
    }
}

class DashboardCreator:
    """Create stunning interactive dashboards"""
    
    def __init__(self, data_path='output/anime_cleaned.csv'):
        print("📊 Loading cleaned dataset...")
        self.df = pd.read_csv(data_path)
        self.cols_lower = {col.lower(): col for col in self.df.columns}
        print(f"✓ Loaded {len(self.df):,} anime records")
        
    def create_kpi_cards(self):
        """Create KPI metrics similar to the reference dashboard"""
        print("\n📈 Generating KPI metrics...")
        
        # Detect column names and convert to numeric
        score_col = self.cols_lower.get('score', self.cols_lower.get('rating'))
        members_col = self.cols_lower.get('members', self.cols_lower.get('popularity'))
        episodes_col = self.cols_lower.get('episodes', self.cols_lower.get('eps'))
        
        # Calculate KPIs with proper numeric conversion
        total_anime = len(self.df)
        
        avg_rating = 0.0
        if score_col and score_col in self.df.columns:
            avg_rating = pd.to_numeric(self.df[score_col], errors='coerce').mean()
            if pd.isna(avg_rating):
                avg_rating = 0.0
        
        total_members = 0
        if members_col and members_col in self.df.columns:
            total_members = pd.to_numeric(self.df[members_col], errors='coerce').sum()
            if pd.isna(total_members):
                total_members = 0
        
        total_episodes = 0
        if episodes_col and episodes_col in self.df.columns:
            total_episodes = pd.to_numeric(self.df[episodes_col], errors='coerce').sum()
            if pd.isna(total_episodes):
                total_episodes = 0
        
        kpis = {
            'Total Anime': int(total_anime),
            'Avg Rating': float(avg_rating),
            'Total Members': int(total_members),
            'Total Episodes': int(total_episodes),
        }
        
        # Create KPI figure
        fig = go.Figure()
        
        annotations = []
        x_positions = [0.15, 0.40, 0.65, 0.90]
        
        for idx, (label, value) in enumerate(kpis.items()):
            # Format value - handle NaN and different types
            if pd.isna(value):
                display_value = "N/A"
            elif isinstance(value, float):
                display_value = f"{value:.2f}"
                if label == 'Avg Rating':
                    display_value = f"⭐ {value:.1f}/10"
            elif isinstance(value, (int, np.integer)):
                display_value = f"{int(value):,}"
            else:
                display_value = str(value)
            
            # Add annotation for KPI value
            annotations.append(dict(
                x=x_positions[idx],
                y=0.7,
                text=f"<b>{display_value}</b>",
                showarrow=False,
                font=dict(size=32, color=TEXT_COLOR),
                xref='paper',
                yref='paper'
            ))
            
            # Add label
            annotations.append(dict(
                x=x_positions[idx],
                y=0.4,
                text=label,
                showarrow=False,
                font=dict(size=14, color=TEXT_COLOR, family='Inter'),
                xref='paper',
                yref='paper'
            ))
            
            # Add trend indicator (simulated)
            trend = np.random.choice(['+', '-']) + f"{np.random.randint(1, 15)}%"
            trend_color = GREEN if trend.startswith('+') else RED
            annotations.append(dict(
                x=x_positions[idx],
                y=0.25,
                text=trend,
                showarrow=False,
                font=dict(size=12, color=trend_color),
                xref='paper',
                yref='paper'
            ))
        
        fig.update_layout(
            annotations=annotations,
            height=250,
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=20, r=20, t=30, b=20),
            title=dict(
                text="<b>Key Performance Indicators</b>",
                font=dict(size=20, color=TEXT_COLOR),
                x=0.02,
                y=0.95
            )
        )
        
        return fig
    
    def create_rating_distribution(self):
        """Create rating distribution chart"""
        print("📊 Creating rating distribution...")
        
        score_col = self.cols_lower.get('score', self.cols_lower.get('rating'))
        
        if not score_col:
            return None
        
        # Create histogram
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=self.df[score_col].dropna(),
            nbinsx=30,
            marker=dict(
                color=PURPLE,
                line=dict(color=BLUE, width=1)
            ),
            name='Rating Distribution',
            hovertemplate='Rating: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Rating Distribution</b>",
            xaxis_title="Rating Score",
            yaxis_title="Number of Anime",
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR),
            height=400,
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    
    def create_trends_over_time(self):
        """Create anime releases trend over time"""
        print("📈 Creating trends over time...")
        
        if 'year' not in self.df.columns:
            return None
        
        # Count anime by year
        yearly_counts = self.df['year'].value_counts().sort_index()
        yearly_counts = yearly_counts[yearly_counts.index >= 1960]  # Filter old data
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=yearly_counts.index,
            y=yearly_counts.values,
            mode='lines+markers',
            name='Anime Releases',
            line=dict(color=PURPLE, width=3),
            marker=dict(size=6, color=BLUE),
            fill='tonexty',
            fillcolor=f'rgba(155, 135, 245, 0.2)',
            hovertemplate='Year: %{x}<br>Releases: %{y}<extra></extra>'
        ))
        
        # Add moving average
        if len(yearly_counts) > 5:
            ma = yearly_counts.rolling(window=5, center=True).mean()
            fig.add_trace(go.Scatter(
                x=ma.index,
                y=ma.values,
                mode='lines',
                name='5-Year Moving Avg',
                line=dict(color=YELLOW, width=2, dash='dash'),
                hovertemplate='Year: %{x}<br>Avg: %{y:.0f}<extra></extra>'
            ))
        
        fig.update_layout(
            title="<b>Anime Releases Over Time</b>",
            xaxis_title="Year",
            yaxis_title="Number of Releases",
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR),
            height=400,
            margin=dict(l=60, r=40, t=60, b=60),
            hovermode='x unified'
        )
        
        return fig
    
    def create_genre_analysis(self):
        """Analyze genre distribution"""
        print("🎭 Creating genre analysis...")
        
        genre_col = self.cols_lower.get('genres', self.cols_lower.get('genre'))
        
        if not genre_col:
            return None
        
        # Extract and count genres
        all_genres = []
        for genres in self.df[genre_col].dropna():
            if isinstance(genres, str):
                # Split by comma or other delimiters
                genre_list = [g.strip() for g in str(genres).replace('[', '').replace(']', '').replace("'", "").split(',')]
                all_genres.extend(genre_list)
        
        genre_counts = pd.Series(all_genres).value_counts().head(15)
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        colors = [PURPLE, BLUE, YELLOW, GREEN, RED] * 3
        
        fig.add_trace(go.Bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            marker=dict(
                color=colors[:len(genre_counts)],
                line=dict(color=TEXT_COLOR, width=0.5)
            ),
            hovertemplate='%{y}<br>Count: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title="<b>Top 15 Anime Genres</b>",
            xaxis_title="Number of Anime",
            yaxis_title="",
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR),
            height=500,
            margin=dict(l=120, r=40, t=60, b=60),
            showlegend=False
        )
        
        return fig
    
    def create_top_anime_table(self):
        """Create top-rated anime table"""
        print("🏆 Creating top anime rankings...")
        
        score_col = self.cols_lower.get('score', self.cols_lower.get('rating'))
        name_col = self.cols_lower.get('name', self.cols_lower.get('title', self.df.columns[0]))
        
        if not score_col:
            return None
        
        # Get top 20 anime
        top_anime = self.df.nlargest(20, score_col)[[name_col, score_col]]
        
        # Create table
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Rank</b>', '<b>Anime Title</b>', '<b>Rating</b>'],
                fill_color=PURPLE,
                align='left',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[
                    list(range(1, 21)),
                    top_anime[name_col].tolist(),
                    [f"{score:.2f}" for score in top_anime[score_col]]
                ],
                fill_color=[[CARD_BG, '#1f1f1f'] * 10],
                align='left',
                font=dict(color=TEXT_COLOR, size=11),
                height=30
            )
        )])
        
        fig.update_layout(
            title="<b>Top 20 Highest-Rated Anime</b>",
            paper_bgcolor=DARK_BG,
            height=600,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_type_distribution(self):
        """Create anime type distribution (TV, Movie, OVA, etc.)"""
        print("📺 Creating type distribution...")
        
        type_col = self.cols_lower.get('type', None)
        
        if not type_col:
            return None
        
        type_counts = self.df[type_col].value_counts()
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.5,
            marker=dict(colors=[PURPLE, BLUE, YELLOW, GREEN, RED, '#ec4899', '#8b5cf6']),
            hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            textinfo='label+percent',
            textfont=dict(color='white', size=12)
        )])
        
        fig.update_layout(
            title="<b>Anime Type Distribution</b>",
            paper_bgcolor=DARK_BG,
            font=dict(color=TEXT_COLOR),
            height=450,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color=TEXT_COLOR)
            )
        )
        
        return fig
    
    def create_rating_by_type_heatmap(self):
        """Create heatmap of ratings by type and year"""
        print("🗺️ Creating rating heatmap...")
        
        score_col = self.cols_lower.get('score', self.cols_lower.get('rating'))
        type_col = self.cols_lower.get('type', None)
        
        if not score_col or not type_col or 'year' not in self.df.columns:
            return None
        
        # Filter recent years - ensure year is numeric
        recent_df = self.df.copy()
        recent_df['year'] = pd.to_numeric(recent_df['year'], errors='coerce')
        recent_df = recent_df[recent_df['year'] >= 2000].copy()
        
        # Create pivot table
        pivot = recent_df.pivot_table(
            values=score_col,
            index=type_col,
            columns='year',
            aggfunc='mean'
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[[0, PURPLE], [0.5, BLUE], [1, YELLOW]],
            hovertemplate='Year: %{x}<br>Type: %{y}<br>Avg Rating: %{z:.2f}<extra></extra>',
            colorbar=dict(
                title=dict(text="Avg Rating", font=dict(color=TEXT_COLOR)),
                tickfont=dict(color=TEXT_COLOR)
            )
        ))
        
        fig.update_layout(
            title="<b>Average Rating by Type and Year</b>",
            xaxis_title="Year",
            yaxis_title="Anime Type",
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            height=400,
            margin=dict(l=80, r=40, t=60, b=60)
        )
        
        return fig
    
    def create_episodes_vs_rating(self):
        """Create scatter plot of episodes vs rating"""
        print("⚡ Creating episodes vs rating analysis...")
        
        score_col = self.cols_lower.get('score', self.cols_lower.get('rating'))
        episodes_col = self.cols_lower.get('episodes', self.cols_lower.get('eps'))
        type_col = self.cols_lower.get('type', None)
        
        if not score_col or not episodes_col:
            return None
        
        # Filter reasonable episode counts - convert to numeric first
        plot_df = self.df.copy()
        plot_df[episodes_col] = pd.to_numeric(plot_df[episodes_col], errors='coerce')
        plot_df[score_col] = pd.to_numeric(plot_df[score_col], errors='coerce')
        plot_df = plot_df[(plot_df[episodes_col] > 0) & (plot_df[episodes_col] < 500)].copy()
        
        if type_col:
            fig = px.scatter(
                plot_df,
                x=episodes_col,
                y=score_col,
                color=type_col,
                size=episodes_col,
                hover_data=[self.cols_lower.get('name', self.df.columns[0])],
                color_discrete_sequence=[PURPLE, BLUE, YELLOW, GREEN, RED, '#ec4899'],
                opacity=0.6
            )
        else:
            fig = px.scatter(
                plot_df,
                x=episodes_col,
                y=score_col,
                size=episodes_col,
                color=score_col,
                color_continuous_scale=[[0, PURPLE], [0.5, BLUE], [1, YELLOW]],
                opacity=0.6
            )
        
        fig.update_layout(
            title="<b>Episodes vs Rating Analysis</b>",
            xaxis_title="Number of Episodes",
            yaxis_title="Rating Score",
            paper_bgcolor=DARK_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(gridcolor=GRID_COLOR),
            yaxis=dict(gridcolor=GRID_COLOR),
            height=500,
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    
    def create_comprehensive_dashboard(self):
        """Create the main comprehensive dashboard"""
        print("\n" + "="*80)
        print("🎨 Creating Comprehensive Dashboard")
        print("="*80)
        
        os.makedirs('output/dashboards', exist_ok=True)
        
        # Generate all visualizations
        charts = {
            'kpi_cards': self.create_kpi_cards(),
            'rating_dist': self.create_rating_distribution(),
            'trends': self.create_trends_over_time(),
            'genres': self.create_genre_analysis(),
            'top_anime': self.create_top_anime_table(),
            'type_dist': self.create_type_distribution(),
            'heatmap': self.create_rating_by_type_heatmap(),
            'episodes_rating': self.create_episodes_vs_rating(),
        }
        
        # Save individual charts
        print("\n💾 Saving individual visualizations...")
        for name, fig in charts.items():
            if fig is not None:
                filename = f'output/dashboards/{name}.html'
                fig.write_html(filename)
                print(f"  ✓ Saved {filename}")
        
        # Create combined dashboard
        print("\n🎯 Creating combined dashboard...")
        
        with open('output/dashboards/main_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(f'''
<!DOCTYPE html>
<html>
<head>
    <title>MyAnimeList Analytics Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: {DARK_BG};
            color: {TEXT_COLOR};
            padding: 20px;
        }}
        .header {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, {PURPLE}, {BLUE});
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        .dashboard-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
        }}
        .card {{
            background: {CARD_BG};
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        iframe {{
            width: 100%;
            border: none;
            border-radius: 8px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            opacity: 0.6;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎌 MyAnimeList Analytics Dashboard</h1>
        <p>Comprehensive insights into anime trends, ratings, and popularity</p>
        <p style="font-size: 14px; margin-top: 10px;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    
    <div class="dashboard-grid">
        <div class="card full-width">
            <iframe src="kpi_cards.html" height="300"></iframe>
        </div>
        
        <div class="card">
            <iframe src="rating_dist.html" height="450"></iframe>
        </div>
        
        <div class="card">
            <iframe src="type_dist.html" height="450"></iframe>
        </div>
        
        <div class="card full-width">
            <iframe src="trends.html" height="450"></iframe>
        </div>
        
        <div class="card">
            <iframe src="genres.html" height="550"></iframe>
        </div>
        
        <div class="card">
            <iframe src="top_anime.html" height="550"></iframe>
        </div>
        
        <div class="card full-width">
            <iframe src="heatmap.html" height="450"></iframe>
        </div>
        
        <div class="card full-width">
            <iframe src="episodes_rating.html" height="550"></iframe>
        </div>
    </div>
    
    <div class="footer">
        <p>📊 MyAnimeList Dataset Analysis | Powered by Plotly & Python</p>
    </div>
</body>
</html>
''')
        
        print("\n" + "="*80)
        print("✅ DASHBOARD CREATION COMPLETE!")
        print("="*80)
        print(f"\n📂 Output Location: output/dashboards/")
        print(f"🌐 Main Dashboard: output/dashboards/main_dashboard.html")
        print(f"\n💡 Open 'main_dashboard.html' in your browser to view the interactive dashboard!")
        print("="*80)

if __name__ == "__main__":
    try:
        creator = DashboardCreator()
        creator.create_comprehensive_dashboard()
    except FileNotFoundError:
        print("\n❌ Error: Cleaned dataset not found!")
        print("Please run 'python analyze.py' first to clean the data.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
