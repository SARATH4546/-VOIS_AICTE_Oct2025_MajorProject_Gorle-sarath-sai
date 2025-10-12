"""
Netflix Dataset Advanced Analytics Engine
Professional statistical analysis and insights generation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import logging
from collections import Counter
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class NetflixAnalyzer:
    """
    Advanced analytics engine for Netflix dataset with comprehensive analysis capabilities
    """
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.insights = {}
        
    def temporal_analysis(self) -> Dict[str, Any]:
        """Analyze content trends over time with advanced metrics"""
        logger.info("Performing comprehensive temporal analysis")
        
        # Year-wise content distribution
        yearly_stats = self.data.groupby(['Release_Year', 'Category']).size().unstack(fill_value=0)
        yearly_total = self.data.groupby('Release_Year').size()
        
        # Growth analysis
        growth_rates = yearly_total.pct_change().fillna(0)
        cumulative_content = yearly_total.cumsum()
        
        # Peak analysis
        peak_year = yearly_total.idxmax()
        peak_count = yearly_total.max()
        
        # Trend analysis
        years = yearly_total.index.values.reshape(-1, 1)
        content_counts = yearly_total.values
        
        # Calculate correlation with time (trend strength)
        correlation = np.corrcoef(years.flatten(), content_counts)[0, 1]
        
        # Seasonal analysis (by month)
        monthly_stats = self.data.groupby('Release_Month').size()
        peak_month = monthly_stats.idxmax()
        
        temporal_insights = {
            'yearly_distribution': yearly_stats.to_dict(),
            'yearly_totals': yearly_total.to_dict(),
            'peak_year': {'year': int(peak_year), 'count': int(peak_count)},
            'average_growth_rate': float(growth_rates.mean()),
            'max_growth_rate': float(growth_rates.max()),
            'total_years': int(self.data['Release_Year'].max() - self.data['Release_Year'].min()),
            'trend_correlation': float(correlation),
            'cumulative_content': cumulative_content.to_dict(),
            'monthly_distribution': monthly_stats.to_dict(),
            'peak_month': int(peak_month),
            'content_acceleration': {
                'early_years': yearly_total.iloc[:len(yearly_total)//2].mean(),
                'recent_years': yearly_total.iloc[len(yearly_total)//2:].mean()
            }
        }
        
        self.insights['temporal'] = temporal_insights
        return temporal_insights
    
    def genre_analysis(self) -> Dict[str, Any]:
        """Comprehensive genre analysis with diversity metrics"""
        logger.info("Performing advanced genre analysis")
        
        # Extract all genres
        all_genres = []
        for genres in self.data['Type'].dropna():
            if isinstance(genres, str) and genres != 'Unknown':
                genre_list = [genre.strip() for genre in genres.split(',')]
                all_genres.extend(genre_list)
        
        genre_counts = Counter(all_genres)
        
        # Category-wise genre analysis
        movie_genres = []
        tv_genres = []
        
        for idx, row in self.data.iterrows():
            if pd.notna(row['Type']) and row['Type'] != 'Unknown':
                genres = [g.strip() for g in str(row['Type']).split(',')]
                if row['Category'] == 'Movie':
                    movie_genres.extend(genres)
                else:
                    tv_genres.extend(genres)
        
        movie_genre_counts = Counter(movie_genres)
        tv_genre_counts = Counter(tv_genres)
        
        # Genre diversity calculations
        total_unique_genres = len(genre_counts)
        genre_entropy = self._calculate_entropy([count for count in genre_counts.values()])
        
        # Genre evolution over time
        genre_trends = {}
        for genre in list(genre_counts.keys())[:5]:  # Top 5 genres
            genre_by_year = self.data[self.data['Type'].str.contains(genre, na=False)].groupby('Release_Year').size()
            genre_trends[genre] = genre_by_year.to_dict()
        
        genre_insights = {
            'total_unique_genres': total_unique_genres,
            'top_genres_overall': dict(genre_counts.most_common(15)),
            'top_movie_genres': dict(movie_genre_counts.most_common(10)),
            'top_tv_genres': dict(tv_genre_counts.most_common(10)),
            'genre_diversity_score': total_unique_genres / len(self.data) * 100,
            'genre_entropy': float(genre_entropy),
            'genre_concentration': {
                'top_5_percentage': sum([genre_counts[genre] for genre in dict(genre_counts.most_common(5))]) / sum(genre_counts.values()) * 100,
                'top_10_percentage': sum([genre_counts[genre] for genre in dict(genre_counts.most_common(10))]) / sum(genre_counts.values()) * 100
            },
            'genre_trends_over_time': genre_trends,
            'rare_genres': dict(Counter({k: v for k, v in genre_counts.items() if v <= 5}))
        }
        
        self.insights['genre'] = genre_insights
        return genre_insights
    
    def geographic_analysis(self) -> Dict[str, Any]:
        """Advanced geographic content distribution analysis"""
        logger.info("Performing comprehensive geographic analysis")
        
        # Extract all countries
        all_countries = []
        for countries in self.data['Country'].dropna():
            if isinstance(countries, str) and countries != 'Unknown':
                country_list = [country.strip() for country in countries.split(',')]
                all_countries.extend(country_list)
        
        country_counts = Counter(all_countries)
        
        # Regional analysis
        regional_mapping = self._get_regional_mapping()
        regional_counts = Counter()
        
        for country, count in country_counts.items():
            region = regional_mapping.get(country, 'Other')
            regional_counts[region] += count
        
        # Content localization analysis
        us_content = country_counts.get('United States', 0)
        total_content = sum(country_counts.values())
        international_ratio = (total_content - us_content) / total_content * 100 if total_content > 0 else 0
        
        # Country diversity metrics
        country_entropy = self._calculate_entropy([count for count in country_counts.values()])
        
        # Multi-country productions
        multi_country_productions = self.data[self.data['Country'].str.contains(',', na=False)]
        
        geographic_insights = {
            'total_unique_countries': len(country_counts),
            'top_countries': dict(country_counts.most_common(15)),
            'regional_distribution': dict(regional_counts.most_common()),
            'us_content_count': us_content,
            'international_percentage': float(international_ratio),
            'content_per_country': total_content / len(country_counts) if len(country_counts) > 0 else 0,
            'country_diversity_entropy': float(country_entropy),
            'multi_country_productions': {
                'count': len(multi_country_productions),
                'percentage': len(multi_country_productions) / len(self.data) * 100
            },
            'geographic_expansion': {
                'countries_with_single_content': sum(1 for count in country_counts.values() if count == 1),
                'countries_with_10plus_content': sum(1 for count in country_counts.values() if count >= 10)
            }
        }
        
        self.insights['geographic'] = geographic_insights
        return geographic_insights
    
    def content_strategy_analysis(self) -> Dict[str, Any]:
        """Analyze Netflix's comprehensive content strategy"""
        logger.info("Performing strategic content analysis")
        
        # Content mix evolution
        category_dist = self.data['Category'].value_counts(normalize=True) * 100
        
        # Duration analysis with statistical measures
        movie_durations = self.data[self.data['Category'] == 'Movie']['Duration_Minutes'].dropna()
        tv_seasons = self.data[self.data['Category'] == 'TV Show']['Season_Count'].dropna()
        
        # Content freshness and portfolio aging
        current_year = 2021
        content_age_dist = self.data['Content_Age'].value_counts().sort_index()
        
        # Rating distribution analysis
        rating_dist = self.data['Rating'].value_counts()
        
        # Content velocity (additions per year)
        content_velocity = self.data.groupby('Release_Year').size()
        avg_velocity = content_velocity.mean()
        
        strategy_insights = {
            'content_mix': {
                'movie_percentage': float(category_dist.get('Movie', 0)),
                'tv_show_percentage': float(category_dist.get('TV Show', 0))
            },
            'duration_strategy': {
                'movie_duration_stats': {
                    'mean': float(movie_durations.mean()) if len(movie_durations) > 0 else 0,
                    'median': float(movie_durations.median()) if len(movie_durations) > 0 else 0,
                    'std': float(movie_durations.std()) if len(movie_durations) > 0 else 0,
                    'range': [float(movie_durations.min()), float(movie_durations.max())] if len(movie_durations) > 0 else [0, 0]
                },
                'tv_season_stats': {
                    'mean': float(tv_seasons.mean()) if len(tv_seasons) > 0 else 0,
                    'median': float(tv_seasons.median()) if len(tv_seasons) > 0 else 0,
                    'most_common': int(tv_seasons.mode().iloc[0]) if len(tv_seasons) > 0 else 0
                }
            },
            'content_freshness': {
                'average_content_age': float(self.data['Content_Age'].mean()),
                'fresh_content_ratio': float((self.data['Content_Age'] <= 3).mean() * 100),
                'vintage_content_ratio': float((self.data['Content_Age'] >= 10).mean() * 100),
                'age_distribution': content_age_dist.head(10).to_dict()
            },
            'rating_strategy': {
                'rating_distribution': rating_dist.to_dict(),
                'family_friendly_percentage': float(rating_dist.get('G', 0) + rating_dist.get('PG', 0) + rating_dist.get('TV-G', 0) + rating_dist.get('TV-PG', 0)) / len(self.data) * 100,
                'mature_content_percentage': float(rating_dist.get('R', 0) + rating_dist.get('TV-MA', 0)) / len(self.data) * 100
            },
            'content_velocity': {
                'average_additions_per_year': float(avg_velocity),
                'peak_addition_year': int(content_velocity.idxmax()),
                'velocity_trend': 'increasing' if content_velocity.iloc[-3:].mean() > content_velocity.iloc[:3].mean() else 'decreasing'
            }
        }
        
        self.insights['strategy'] = strategy_insights
        return strategy_insights
    
    def competitive_analysis(self) -> Dict[str, Any]:
        """Analyze competitive positioning and market dynamics"""
        logger.info("Performing competitive positioning analysis")
        
        # Content uniqueness indicators
        director_diversity = self.data['Director'].nunique() / len(self.data)
        cast_diversity = self.data['Cast'].nunique() / len(self.data)
        
        # Genre innovation (rare genre combinations)
        genre_combinations = []
        for genres in self.data['Type'].dropna():
            if isinstance(genres, str) and ',' in genres:
                genre_combinations.append(tuple(sorted(genres.split(', '))))
        
        combination_counts = Counter(genre_combinations)
        
        competitive_insights = {
            'content_differentiation': {
                'director_diversity_score': float(director_diversity),
                'cast_diversity_score': float(cast_diversity),
                'unique_genre_combinations': len(combination_counts),
                'rare_combinations': dict(Counter({k: v for k, v in combination_counts.items() if v <= 3}).most_common(10))
            },
            'market_positioning': {
                'international_vs_domestic': {
                    'international_content_percentage': self.insights.get('geographic', {}).get('international_percentage', 0),
                    'multi_regional_content': len([c for c in Counter(all_countries).values() if c > 50])
                },
                'content_volume_metrics': {
                    'total_hours_estimate': self._estimate_total_content_hours(),
                    'content_density_score': len(self.data) / self.data['Release_Year'].nunique()
                }
            }
        }
        
        return competitive_insights
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate complete analysis report with all metrics"""
        logger.info("Generating comprehensive strategic analysis report")
        
        # Run all analyses
        temporal = self.temporal_analysis()
        genre = self.genre_analysis()
        geographic = self.geographic_analysis()
        strategy = self.content_strategy_analysis()
        competitive = self.competitive_analysis()
        
        # Generate executive summary with key insights
        executive_summary = {
            'total_content': len(self.data),
            'date_range': f"{self.data['Release_Year'].min():.0f}-{self.data['Release_Year'].max():.0f}",
            'peak_year': temporal['peak_year']['year'],
            'dominant_genre': max(genre['top_genres_overall'], key=genre['top_genres_overall'].get) if genre['top_genres_overall'] else 'Unknown',
            'top_country': max(geographic['top_countries'], key=geographic['top_countries'].get) if geographic['top_countries'] else 'Unknown',
            'international_percentage': geographic['international_percentage'],
            'movie_percentage': strategy['content_mix']['movie_percentage'],
            'content_diversity': {
                'genre_entropy': genre['genre_entropy'],
                'country_entropy': geographic['country_diversity_entropy'],
                'overall_diversity_score': (genre['genre_entropy'] + geographic['country_diversity_entropy']) / 2
            },
            'strategic_focus': {
                'content_velocity': strategy['content_velocity']['average_additions_per_year'],
                'freshness_ratio': strategy['content_freshness']['fresh_content_ratio'],
                'international_expansion': geographic['international_percentage'] > 50
            }
        }
        
        comprehensive_report = {
            'executive_summary': executive_summary,
            'temporal_analysis': temporal,
            'genre_analysis': genre,
            'geographic_analysis': geographic,
            'strategy_analysis': strategy,
            'competitive_analysis': competitive,
            'recommendations': self._generate_recommendations(executive_summary, strategy, geographic, genre)
        }
        
        return comprehensive_report
    
    def _calculate_entropy(self, counts: List[int]) -> float:
        """Calculate Shannon entropy for diversity measurement"""
        if not counts or sum(counts) == 0:
            return 0.0
        
        total = sum(counts)
        probabilities = [count / total for count in counts if count > 0]
        
        entropy = -sum(p * np.log2(p) for p in probabilities)
        return entropy
    
    def _get_regional_mapping(self) -> Dict[str, str]:
        """Get country to region mapping for geographic analysis"""
        return {
            'United States': 'North America',
            'Canada': 'North America',
            'United Kingdom': 'Europe',
            'France': 'Europe',
            'Germany': 'Europe',
            'Spain': 'Europe',
            'Italy': 'Europe',
            'India': 'Asia',
            'Japan': 'Asia',
            'South Korea': 'Asia',
            'China': 'Asia',
            'Australia': 'Oceania',
            'Brazil': 'South America',
            'Mexico': 'North America',
            'Argentina': 'South America',
            'Nigeria': 'Africa',
            'South Africa': 'Africa',
            'Egypt': 'Africa'
        }
    
    def _estimate_total_content_hours(self) -> float:
        """Estimate total hours of content"""
        movie_hours = self.data[self.data['Category'] == 'Movie']['Duration_Minutes'].dropna().sum() / 60
        
        # Estimate TV show hours (assume 45 min per episode, 10 episodes per season average)
        tv_hours = self.data[self.data['Category'] == 'TV Show']['Season_Count'].dropna().sum() * 10 * 45 / 60
        
        return movie_hours + tv_hours
    
    def _generate_recommendations(self, summary: Dict, strategy: Dict, geographic: Dict, genre: Dict) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        # Content mix recommendations
        if strategy['content_mix']['movie_percentage'] > 75:
            recommendations.append("Consider increasing TV show production to balance content portfolio")
        elif strategy['content_mix']['tv_show_percentage'] > 60:
            recommendations.append("Consider increasing movie acquisitions to diversify content mix")
        
        # Geographic expansion recommendations
        if geographic['international_percentage'] < 40:
            recommendations.append("Expand international content acquisition to capture global markets")
        
        # Genre diversity recommendations
        if genre['genre_concentration']['top_5_percentage'] > 70:
            recommendations.append("Diversify genre portfolio to reduce content concentration risk")
        
        # Content freshness recommendations
        if strategy['content_freshness']['fresh_content_ratio'] < 30:
            recommendations.append("Increase focus on recent content to maintain platform relevance")
        
        return recommendations

# Example usage
if __name__ == "__main__":
    print("Netflix Advanced Analytics Engine Loaded Successfully!")
    print("Use: analyzer = NetflixAnalyzer(processed_dataframe)")
    print("Then: report = analyzer.generate_comprehensive_report()")