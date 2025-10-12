"""
Netflix Dataset Data Processing Module
Advanced data cleaning and feature engineering
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetflixDataProcessor:
    """
    Professional Netflix dataset processor with comprehensive data cleaning
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None
        
    def load_data(self) -> pd.DataFrame:
        """Load the Netflix dataset with error handling"""
        try:
            logger.info(f"Loading dataset from {self.data_path}")
            self.raw_data = pd.read_csv(self.data_path)
            logger.info(f"Dataset loaded: {self.raw_data.shape[0]} rows, {self.raw_data.shape[1]} columns")
            return self.raw_data
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """Comprehensive data cleaning and preprocessing"""
        if self.raw_data is None:
            self.load_data()
        
        df = self.raw_data.copy()
        
        # Clean dates
        df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
        df['Release_Year'] = df['Release_Date'].dt.year
        df['Release_Month'] = df['Release_Date'].dt.month
        
        # Fill missing values
        df['Country'] = df['Country'].fillna('Unknown')
        df['Type'] = df['Type'].fillna('Unknown')
        df['Category'] = df['Category'].fillna('Unknown')
        df['Director'] = df['Director'].fillna('Unknown')
        df['Cast'] = df['Cast'].fillna('Unknown')
        df['Description'] = df['Description'].fillna('')
        
        # Process genres
        df['Genre_List'] = df['Type'].apply(
            lambda x: [genre.strip() for genre in str(x).split(',') if str(x) != 'Unknown'] if pd.notna(x) else []
        )
        df['Genre_Count'] = df['Genre_List'].apply(len)
        df['Primary_Genre'] = df['Genre_List'].apply(lambda x: x[0] if x else 'Unknown')
        
        # Process countries
        df['Country_List'] = df['Country'].apply(
            lambda x: [country.strip() for country in str(x).split(',') if str(x) != 'Unknown'] if pd.notna(x) else []
        )
        df['Country_Count'] = df['Country_List'].apply(len)
        df['Primary_Country'] = df['Country_List'].apply(lambda x: x[0] if x else 'Unknown')
        
        # Extract duration features
        df['Duration_Minutes'] = df.apply(
            lambda row: self._extract_duration(row.get('Duration', ''), 'minutes'), axis=1
        )
        df['Season_Count'] = df.apply(
            lambda row: self._extract_duration(row.get('Duration', ''), 'seasons'), axis=1
        )
        
        # Content features
        current_year = 2021  # Dataset typically ends around 2021
        df['Content_Age'] = current_year - df['Release_Year']
        df['Is_US_Content'] = df['Primary_Country'].apply(lambda x: 1 if x == 'United States' else 0)
        
        # Text features
        df['Description_Length'] = df['Description'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
        df['Title_Length'] = df['Title'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
        df['Has_Description'] = df['Description_Length'] > 0
        
        # Cast and director features
        df['Cast_Count'] = df['Cast'].apply(lambda x: len(str(x).split(',')) if str(x) != 'Unknown' else 0)
        df['Director_Count'] = df['Director'].apply(lambda x: len(str(x).split(',')) if str(x) != 'Unknown' else 0)
        
        self.processed_data = df
        logger.info("Data cleaning completed successfully")
        return df
    
    def _extract_duration(self, duration_str: str, duration_type: str) -> Optional[int]:
        """Extract duration in minutes or season count"""
        try:
            if pd.isna(duration_str) or duration_str == '':
                return None
            
            duration_str = str(duration_str).strip()
            
            if duration_type == 'minutes' and 'min' in duration_str:
                # Extract minutes for movies
                return int(duration_str.split(' ')[0])
            elif duration_type == 'seasons' and 'Season' in duration_str:
                # Extract season count for TV shows
                return int(duration_str.split(' ')[0])
            else:
                return None
        except (ValueError, IndexError):
            return None
    
    def get_summary_stats(self) -> Dict:
        """Generate comprehensive summary statistics"""
        if self.processed_data is None:
            self.clean_data()
        
        df = self.processed_data
        
        summary = {
            'total_records': len(df),
            'date_range': f"{df['Release_Year'].min():.0f} - {df['Release_Year'].max():.0f}",
            'movies': len(df[df['Category'] == 'Movie']),
            'tv_shows': len(df[df['Category'] == 'TV Show']),
            'unique_countries': df['Primary_Country'].nunique(),
            'unique_genres': df['Primary_Genre'].nunique(),
            'unique_directors': df['Director'].nunique(),
            'avg_content_age': df['Content_Age'].mean(),
            'missing_data_summary': {
                'total_missing': df.isnull().sum().sum(),
                'missing_by_column': df.isnull().sum().to_dict()
            }
        }
        
        return summary
    
    def save_processed_data(self, output_path: str) -> None:
        """Save processed data to CSV"""
        if self.processed_data is None:
            raise ValueError("No processed data available")
        
        self.processed_data.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")
    
    def get_data_quality_report(self) -> Dict:
        """Generate data quality assessment report"""
        if self.processed_data is None:
            self.clean_data()
        
        df = self.processed_data
        
        quality_report = {
            'completeness': {
                'total_cells': df.size,
                'missing_cells': df.isnull().sum().sum(),
                'completeness_rate': (1 - df.isnull().sum().sum() / df.size) * 100
            },
            'duplicates': {
                'duplicate_rows': df.duplicated().sum(),
                'duplicate_titles': df['Title'].duplicated().sum()
            },
            'data_types': df.dtypes.to_dict(),
            'value_ranges': {
                'release_years': {
                    'min': df['Release_Year'].min(),
                    'max': df['Release_Year'].max(),
                    'range': df['Release_Year'].max() - df['Release_Year'].min()
                },
                'content_age': {
                    'min': df['Content_Age'].min(),
                    'max': df['Content_Age'].max(),
                    'mean': df['Content_Age'].mean()
                }
            }
        }
        
        return quality_report

# Utility functions for data processing
def validate_netflix_dataset(df: pd.DataFrame) -> Dict[str, bool]:
    """Validate Netflix dataset structure and content"""
    required_columns = ['Show_Id', 'Category', 'Title', 'Country', 'Release_Date', 'Type']
    
    validation_results = {
        'has_required_columns': all(col in df.columns for col in required_columns),
        'has_data': len(df) > 0,
        'has_movies_and_shows': len(df['Category'].unique()) >= 2,
        'has_valid_dates': pd.to_datetime(df['Release_Date'], errors='coerce').notna().any(),
        'has_countries': df['Country'].notna().any(),
        'has_genres': df['Type'].notna().any()
    }
    
    return validation_results

# Example usage
if __name__ == "__main__":
    # This would be used with actual data file
    print("Netflix Data Processor Module Loaded Successfully!")
    print("Use: processor = NetflixDataProcessor('path/to/netflix_data.csv')")
    print("Then: processed_data = processor.clean_data()")