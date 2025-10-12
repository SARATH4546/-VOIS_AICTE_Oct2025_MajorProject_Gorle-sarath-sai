"""
Utility Functions for Netflix Analysis Project
Helper functions and common utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
import os
import json
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class DataValidation:
    """Data validation utilities for Netflix dataset"""
    
    @staticmethod
    def validate_netflix_schema(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate Netflix dataset schema and return validation report"""
        required_columns = [
            'Show_Id', 'Category', 'Title', 'Director', 'Cast',
            'Country', 'Release_Date', 'Rating', 'Duration', 'Type', 'Description'
        ]
        
        validation_report = {
            'schema_valid': True,
            'missing_columns': [],
            'extra_columns': [],
            'data_quality': {},
            'recommendations': []
        }
        
        # Check required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        extra_cols = [col for col in df.columns if col not in required_columns]
        
        validation_report['missing_columns'] = missing_cols
        validation_report['extra_columns'] = extra_cols
        validation_report['schema_valid'] = len(missing_cols) == 0
        
        # Data quality checks
        if not missing_cols:
            validation_report['data_quality'] = {
                'total_rows': len(df),
                'duplicate_rows': df.duplicated().sum(),
                'missing_values_per_column': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.to_dict(),
                'unique_categories': df['Category'].unique().tolist() if 'Category' in df.columns else [],
                'date_range': {
                    'earliest': df['Release_Date'].min() if 'Release_Date' in df.columns else None,
                    'latest': df['Release_Date'].max() if 'Release_Date' in df.columns else None
                }
            }
        
        # Generate recommendations
        if missing_cols:
            validation_report['recommendations'].append(f"Missing required columns: {missing_cols}")
        if df.duplicated().sum() > 0:
            validation_report['recommendations'].append("Remove duplicate rows")
        if df.isnull().sum().sum() > len(df) * 0.1:
            validation_report['recommendations'].append("High missing data detected - consider data cleaning")
        
        return validation_report
    
    @staticmethod
    def check_data_consistency(df: pd.DataFrame) -> Dict[str, Any]:
        """Check for data consistency issues"""
        consistency_issues = {
            'date_issues': [],
            'category_issues': [],
            'duration_issues': [],
            'country_issues': []
        }
        
        # Check date consistency
        try:
            dates = pd.to_datetime(df['Release_Date'], errors='coerce')
            invalid_dates = dates.isnull().sum()
            if invalid_dates > 0:
                consistency_issues['date_issues'].append(f"{invalid_dates} invalid dates found")
        except:
            consistency_issues['date_issues'].append("Cannot parse Release_Date column")
        
        # Check category values
        valid_categories = ['Movie', 'TV Show']
        if 'Category' in df.columns:
            invalid_categories = df[~df['Category'].isin(valid_categories)]['Category'].unique()
            if len(invalid_categories) > 0:
                consistency_issues['category_issues'].append(f"Invalid categories found: {invalid_categories}")
        
        return consistency_issues

class FileManager:
    """File management utilities"""
    
    @staticmethod
    def ensure_directories(directories: List[str]) -> None:
        """Ensure all required directories exist"""
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Directory ensured: {directory}")
    
    @staticmethod
    def save_analysis_results(results: Dict[str, Any], output_path: str) -> None:
        """Save analysis results to JSON file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Analysis results saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving analysis results: {str(e)}")
    
    @staticmethod
    def load_analysis_results(input_path: str) -> Optional[Dict[str, Any]]:
        """Load analysis results from JSON file"""
        try:
            with open(input_path, 'r') as f:
                results = json.load(f)
            logger.info(f"Analysis results loaded from {input_path}")
            return results
        except Exception as e:
            logger.error(f"Error loading analysis results: {str(e)}")
            return None
    
    @staticmethod
    def get_file_hash(filepath: str) -> Optional[str]:
        """Get MD5 hash of a file for integrity checking"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return None

class DataExporter:
    """Data export utilities"""
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, output_path: str, sheet_name: str = 'Netflix_Data') -> None:
        """Export DataFrame to Excel with formatting"""
        try:
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                
                # Add header formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#E50914',
                    'font_color': 'white',
                    'border': 1
                })
                
                # Apply header formatting
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Auto-adjust column widths
                for i, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(str(col))
                    )
                    worksheet.set_column(i, i, min(max_length + 2, 50))
                
            logger.info(f"Data exported to Excel: {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {str(e)}")
    
    @staticmethod
    def export_summary_report(analysis_results: Dict[str, Any], output_path: str) -> None:
        """Export analysis summary to formatted text file"""
        try:
            with open(output_path, 'w') as f:
                f.write("NETFLIX DATASET ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Executive Summary
                if 'executive_summary' in analysis_results:
                    f.write("EXECUTIVE SUMMARY\n")
                    f.write("-" * 20 + "\n")
                    summary = analysis_results['executive_summary']
                    for key, value in summary.items():
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                    f.write("\n")
                
                # Key Insights
                f.write("KEY INSIGHTS\n")
                f.write("-" * 15 + "\n")
                
                if 'temporal_analysis' in analysis_results:
                    temporal = analysis_results['temporal_analysis']
                    f.write(f"Peak Year: {temporal.get('peak_year', {}).get('year', 'N/A')} ")
                    f.write(f"({temporal.get('peak_year', {}).get('count', 'N/A')} titles)\n")
                    f.write(f"Average Growth Rate: {temporal.get('average_growth_rate', 0):.2%}\n")
                
                if 'geographic_analysis' in analysis_results:
                    geo = analysis_results['geographic_analysis']
                    f.write(f"International Content: {geo.get('international_percentage', 0):.1f}%\n")
                    f.write(f"Countries Represented: {geo.get('total_unique_countries', 0)}\n")
                
                f.write("\n")
                
                # Recommendations
                if 'recommendations' in analysis_results:
                    f.write("RECOMMENDATIONS\n")
                    f.write("-" * 15 + "\n")
                    for i, rec in enumerate(analysis_results['recommendations'], 1):
                        f.write(f"{i}. {rec}\n")
                
            logger.info(f"Summary report exported to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting summary report: {str(e)}")

class ConfigurationManager:
    """Configuration management utilities"""
    
    DEFAULT_CONFIG = {
        'data_processing': {
            'missing_value_threshold': 0.1,
            'duplicate_handling': 'remove',
            'date_format': '%Y-%m-%d'
        },
        'visualization': {
            'chart_height': 500,
            'color_scheme': 'netflix',
            'export_format': 'html'
        },
        'analysis': {
            'min_genre_count': 5,
            'temporal_grouping': 'yearly',
            'geographic_grouping': 'country'
        }
    }
    
    @classmethod
    def load_config(cls, config_path: str) -> Dict[str, Any]:
        """Load configuration from file or return default"""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return {**cls.DEFAULT_CONFIG, **config}
            except Exception as e:
                logger.error(f"Error loading config: {str(e)}")
        
        return cls.DEFAULT_CONFIG
    
    @classmethod
    def save_config(cls, config: Dict[str, Any], config_path: str) -> None:
        """Save configuration to file"""
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")

class PerformanceProfiler:
    """Performance profiling utilities"""
    
    def __init__(self):
        self.start_time = None
        self.checkpoints = {}
    
    def start(self):
        """Start performance profiling"""
        self.start_time = datetime.now()
        logger.info("Performance profiling started")
    
    def checkpoint(self, name: str):
        """Add a performance checkpoint"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.checkpoints[name] = elapsed
            logger.info(f"Checkpoint '{name}': {elapsed:.2f}s")
    
    def get_report(self) -> Dict[str, float]:
        """Get performance report"""
        return self.checkpoints.copy()

# Utility functions
def format_large_number(number: int) -> str:
    """Format large numbers with appropriate suffixes"""
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return float('inf') if new_value > 0 else 0
    return ((new_value - old_value) / old_value) * 100

def get_memory_usage(df: pd.DataFrame) -> Dict[str, Any]:
    """Get memory usage information for DataFrame"""
    memory_usage = df.memory_usage(deep=True)
    return {
        'total_mb': memory_usage.sum() / (1024 * 1024),
        'by_column': (memory_usage / (1024 * 1024)).to_dict()
    }

def clean_text_column(series: pd.Series) -> pd.Series:
    """Clean text column by removing extra spaces and standardizing format"""
    return series.str.strip().str.replace(r'\s+', ' ', regex=True).str.title()

# Example usage and tests
if __name__ == "__main__":
    print("Netflix Analysis Utilities Loaded Successfully!")
    
    # Test file manager
    FileManager.ensure_directories(['test_dir', 'test_dir/sub'])
    
    # Test data validation (would need actual DataFrame)
    print("Available utilities:")
    print("- DataValidation: validate_netflix_schema(), check_data_consistency()")
    print("- FileManager: ensure_directories(), save_analysis_results(), load_analysis_results()")
    print("- DataExporter: export_to_excel(), export_summary_report()")
    print("- ConfigurationManager: load_config(), save_config()")
    print("- PerformanceProfiler: for timing analysis operations")
    print("- Utility functions: format_large_number(), calculate_percentage_change(), etc.")