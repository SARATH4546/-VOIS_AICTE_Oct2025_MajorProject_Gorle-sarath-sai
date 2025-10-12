"""
Netflix Dataset Advanced Visualization Engine
Professional interactive charts and data visualization suite
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import logging
from typing import Dict, List, Any, Optional
import numpy as np

# Set style configurations
plt.style.use('default')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class NetflixVisualizer:
    """
    Advanced visualization suite for Netflix dataset with interactive charts
    """
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.colors = {
            'netflix_red': '#E50914',
            'netflix_black': '#221F1F',
            'netflix_gray': '#564D4D',
            'netflix_white': '#FFFFFF',
            'success': '#28a745',
            'warning': '#ffc107',
            'info': '#17a2b8'
        }
        
        # Netflix color palette for multiple series
        self.color_palette = [
            '#E50914', '#564D4D', '#B81D24', '#831010', '#F5F5F1',
            '#E5E5E5', '#A6A6A6', '#D22630', '#B5B5B5', '#F40612'
        ]
        
    def create_temporal_chart(self) -> go.Figure:
        """Create comprehensive temporal analysis chart"""
        logger.info("Creating temporal analysis chart")
        
        try:
            yearly_data = self.data.groupby(['Release_Year', 'Category']).size().unstack(fill_value=0)
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Content Growth Over Time', 'Cumulative Content Growth'),
                vertical_spacing=0.12,
                shared_xaxes=True
            )
            
            # Main growth chart
            fig.add_trace(
                go.Scatter(
                    x=yearly_data.index,
                    y=yearly_data.get('Movie', []),
                    mode='lines+markers',
                    name='Movies',
                    line=dict(color=self.colors['netflix_red'], width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>Year:</b> %{x}<br><b>Movies:</b> %{y}<extra></extra>'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=yearly_data.index,
                    y=yearly_data.get('TV Show', []),
                    mode='lines+markers',
                    name='TV Shows',
                    line=dict(color=self.colors['netflix_gray'], width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>Year:</b> %{x}<br><b>TV Shows:</b> %{y}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Cumulative chart
            cumulative_movies = yearly_data.get('Movie', []).cumsum()
            cumulative_tv = yearly_data.get('TV Show', []).cumsum()
            
            fig.add_trace(
                go.Scatter(
                    x=yearly_data.index,
                    y=cumulative_movies,
                    mode='lines',
                    name='Cumulative Movies',
                    line=dict(color=self.colors['netflix_red'], width=2, dash='dot'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=yearly_data.index,
                    y=cumulative_tv,
                    mode='lines',
                    name='Cumulative TV Shows',
                    line=dict(color=self.colors['netflix_gray'], width=2, dash='dot'),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title={
                    'text': 'Netflix Content Growth Analysis',
                    'x': 0.5,
                    'font': {'size': 24, 'family': 'Arial'}
                },
                template='plotly_white',
                height=700,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.update_xaxes(title_text="Year", row=2, col=1)
            fig.update_yaxes(title_text="Annual Additions", row=1, col=1)
            fig.update_yaxes(title_text="Cumulative Total", row=2, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating temporal chart: {str(e)}")
            return self._create_error_chart("Temporal Analysis", str(e))
    
    def create_genre_chart(self) -> go.Figure:
        """Create comprehensive genre distribution chart"""
        logger.info("Creating genre analysis chart")
        
        try:
            # Extract all genres
            all_genres = []
            for genres in self.data['Type'].dropna():
                if isinstance(genres, str) and genres != 'Unknown':
                    genre_list = [genre.strip() for genre in genres.split(',')]
                    all_genres.extend(genre_list)
            
            genre_counts = Counter(all_genres)
            top_genres = dict(genre_counts.most_common(12))
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Top Genres Distribution', 'Genre Popularity'),
                specs=[[{"type": "bar"}, {"type": "pie"}]],
                horizontal_spacing=0.1
            )
            
            # Bar chart
            fig.add_trace(
                go.Bar(
                    x=list(top_genres.values()),
                    y=list(top_genres.keys()),
                    orientation='h',
                    marker_color=self.colors['netflix_red'],
                    text=list(top_genres.values()),
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Pie chart for top 8 genres
            top_8_genres = dict(list(top_genres.items())[:8])
            others_count = sum(list(top_genres.values())[8:])
            if others_count > 0:
                top_8_genres['Others'] = others_count
            
            fig.add_trace(
                go.Pie(
                    labels=list(top_8_genres.keys()),
                    values=list(top_8_genres.values()),
                    marker_colors=self.color_palette[:len(top_8_genres)],
                    textinfo='label+percent',
                    textfont_size=12,
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title={
                    'text': 'Netflix Genre Analysis Dashboard',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                template='plotly_white',
                height=500,
                showlegend=False
            )
            
            fig.update_xaxes(title_text="Number of Titles", row=1, col=1)
            fig.update_yaxes(title_text="Genre", row=1, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating genre chart: {str(e)}")
            return self._create_error_chart("Genre Analysis", str(e))
    
    def create_geographic_chart(self) -> go.Figure:
        """Create comprehensive geographic distribution chart"""
        logger.info("Creating geographic analysis chart")
        
        try:
            # Extract all countries
            all_countries = []
            for countries in self.data['Country'].dropna():
                if isinstance(countries, str) and countries != 'Unknown':
                    country_list = [country.strip() for country in countries.split(',')]
                    all_countries.extend(country_list)
            
            country_counts = Counter(all_countries)
            top_countries = dict(country_counts.most_common(12))
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Top Countries by Content Count', 'Global Distribution Overview'),
                vertical_spacing=0.15
            )
            
            # Horizontal bar chart
            fig.add_trace(
                go.Bar(
                    x=list(top_countries.values()),
                    y=list(top_countries.keys()),
                    orientation='h',
                    marker_color='darkblue',
                    text=list(top_countries.values()),
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Content Count: %{x}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Regional grouping for second chart
            regional_data = self._group_by_regions(country_counts)
            
            fig.add_trace(
                go.Bar(
                    x=list(regional_data.keys()),
                    y=list(regional_data.values()),
                    marker_color=self.color_palette[:len(regional_data)],
                    text=list(regional_data.values()),
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Content Count: %{y}<extra></extra>'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title={
                    'text': 'Netflix Global Content Distribution',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                template='plotly_white',
                height=700,
                showlegend=False
            )
            
            fig.update_xaxes(title_text="Number of Titles", row=1, col=1)
            fig.update_yaxes(title_text="Country", row=1, col=1)
            fig.update_xaxes(title_text="Region", row=2, col=1)
            fig.update_yaxes(title_text="Content Count", row=2, col=1)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating geographic chart: {str(e)}")
            return self._create_error_chart("Geographic Analysis", str(e))
    
    def create_content_mix_chart(self) -> go.Figure:
        """Create enhanced content mix visualization"""
        logger.info("Creating content mix chart")
        
        try:
            category_counts = self.data['Category'].value_counts()
            
            # Create subplot with pie chart and bar chart
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Content Mix Distribution', 'Content Volume Comparison'),
                specs=[[{"type": "pie"}, {"type": "bar"}]],
                horizontal_spacing=0.1
            )
            
            # Pie chart
            fig.add_trace(
                go.Pie(
                    labels=category_counts.index,
                    values=category_counts.values,
                    marker_colors=[self.colors['netflix_red'], self.colors['netflix_gray']],
                    textinfo='label+percent+value',
                    textfont_size=14,
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                    pull=[0.1 if cat == 'Movie' else 0 for cat in category_counts.index]  # Highlight movies
                ),
                row=1, col=1
            )
            
            # Bar chart
            fig.add_trace(
                go.Bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    marker_color=[self.colors['netflix_red'], self.colors['netflix_gray']],
                    text=category_counts.values,
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                title={
                    'text': 'Netflix Content Mix: Movies vs TV Shows',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                template='plotly_white',
                height=400,
                showlegend=False
            )
            
            fig.update_yaxes(title_text="Number of Titles", row=1, col=2)
            fig.update_xaxes(title_text="Content Type", row=1, col=2)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating content mix chart: {str(e)}")
            return self._create_error_chart("Content Mix", str(e))
    
    def create_comprehensive_dashboard(self) -> go.Figure:
        """Create a comprehensive dashboard with multiple metrics"""
        logger.info("Creating comprehensive analytics dashboard")
        
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Content Release Trends',
                    'Top Genres',
                    'Geographic Distribution',
                    'Content Age Distribution'
                ),
                specs=[
                    [{"type": "scatter"}, {"type": "bar"}],
                    [{"type": "bar"}, {"type": "histogram"}]
                ],
                vertical_spacing=0.12,
                horizontal_spacing=0.1
            )
            
            # 1. Release trends
            yearly_total = self.data.groupby('Release_Year').size()
            fig.add_trace(
                go.Scatter(
                    x=yearly_total.index,
                    y=yearly_total.values,
                    mode='lines+markers',
                    name='Annual Releases',
                    line=dict(color=self.colors['netflix_red'], width=3),
                    marker=dict(size=6)
                ),
                row=1, col=1
            )
            
            # 2. Top genres
            all_genres = []
            for genres in self.data['Type'].dropna():
                if isinstance(genres, str):
                    all_genres.extend([g.strip() for g in genres.split(',')])
            
            top_genres = dict(Counter(all_genres).most_common(6))
            fig.add_trace(
                go.Bar(
                    x=list(top_genres.keys()),
                    y=list(top_genres.values()),
                    marker_color=self.colors['netflix_red'],
                    text=list(top_genres.values()),
                    textposition='auto'
                ),
                row=1, col=2
            )
            
            # 3. Top countries
            all_countries = []
            for countries in self.data['Country'].dropna():
                if isinstance(countries, str):
                    all_countries.extend([c.strip() for c in countries.split(',')])
            
            top_countries = dict(Counter(all_countries).most_common(6))
            fig.add_trace(
                go.Bar(
                    x=list(top_countries.values()),
                    y=list(top_countries.keys()),
                    orientation='h',
                    marker_color='darkblue',
                    text=list(top_countries.values()),
                    textposition='auto'
                ),
                row=2, col=1
            )
            
            # 4. Content age distribution
            content_ages = self.data['Content_Age'].dropna()
            fig.add_trace(
                go.Histogram(
                    x=content_ages,
                    nbinsx=20,
                    marker_color=self.colors['netflix_gray'],
                    opacity=0.7
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title={
                    'text': 'Netflix Content Analytics Dashboard',
                    'x': 0.5,
                    'font': {'size': 24}
                },
                template='plotly_white',
                height=800,
                showlegend=False
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Year", row=1, col=1)
            fig.update_yaxes(title_text="Count", row=1, col=1)
            
            fig.update_xaxes(title_text="Genre", row=1, col=2)
            fig.update_yaxes(title_text="Count", row=1, col=2)
            
            fig.update_xaxes(title_text="Count", row=2, col=1)
            fig.update_yaxes(title_text="Country", row=2, col=1)
            
            fig.update_xaxes(title_text="Content Age (Years)", row=2, col=2)
            fig.update_yaxes(title_text="Frequency", row=2, col=2)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating comprehensive dashboard: {str(e)}")
            return self._create_error_chart("Comprehensive Dashboard", str(e))
    
    def _group_by_regions(self, country_counts: Counter) -> Dict[str, int]:
        """Group countries by regions for geographic analysis"""
        regional_mapping = {
            'United States': 'North America',
            'Canada': 'North America',
            'Mexico': 'North America',
            'United Kingdom': 'Europe',
            'France': 'Europe',
            'Germany': 'Europe',
            'Spain': 'Europe',
            'Italy': 'Europe',
            'Netherlands': 'Europe',
            'India': 'Asia',
            'Japan': 'Asia',
            'South Korea': 'Asia',
            'China': 'Asia',
            'Thailand': 'Asia',
            'Australia': 'Oceania',
            'New Zealand': 'Oceania',
            'Brazil': 'South America',
            'Argentina': 'South America',
            'Chile': 'South America',
            'Nigeria': 'Africa',
            'South Africa': 'Africa',
            'Egypt': 'Africa'
        }
        
        regional_counts = Counter()
        for country, count in country_counts.items():
            region = regional_mapping.get(country, 'Other')
            regional_counts[region] += count
        
        return dict(regional_counts.most_common())
    
    def _create_error_chart(self, chart_name: str, error_message: str) -> go.Figure:
        """Create an error chart when visualization fails"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading {chart_name}:<br>{error_message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title=f"Error: {chart_name}",
            template='plotly_white',
            height=400
        )
        return fig
    
    def save_all_charts(self, output_dir: str = "static/images/"):
        """Save all charts as HTML files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Create and save all charts
            temporal_fig = self.create_temporal_chart()
            temporal_fig.write_html(f"{output_dir}temporal_chart.html")
            
            genre_fig = self.create_genre_chart()
            genre_fig.write_html(f"{output_dir}genre_chart.html")
            
            geo_fig = self.create_geographic_chart()
            geo_fig.write_html(f"{output_dir}geographic_chart.html")
            
            mix_fig = self.create_content_mix_chart()
            mix_fig.write_html(f"{output_dir}content_mix_chart.html")
            
            dashboard_fig = self.create_comprehensive_dashboard()
            dashboard_fig.write_html(f"{output_dir}comprehensive_dashboard.html")
            
            logger.info(f"All charts saved to {output_dir}")
            
            return {
                'temporal': f"{output_dir}temporal_chart.html",
                'genre': f"{output_dir}genre_chart.html",
                'geographic': f"{output_dir}geographic_chart.html",
                'content_mix': f"{output_dir}content_mix_chart.html",
                'dashboard': f"{output_dir}comprehensive_dashboard.html"
            }
            
        except Exception as e:
            logger.error(f"Error saving charts: {str(e)}")
            return {}

# Example usage
if __name__ == "__main__":
    print("Netflix Advanced Visualization Engine Loaded Successfully!")
    print("Use: visualizer = NetflixVisualizer(processed_dataframe)")
    print("Then: temporal_chart = visualizer.create_temporal_chart()")