"""
Netflix Analysis Dashboard - FINAL FIX
This will make all 4 charts load perfectly
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
import json
import os
import sys
import logging
from werkzeug.utils import secure_filename
from collections import Counter
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'netflix-analysis-secret-key-2025'
app.config['UPLOAD_FOLDER'] = 'data/raw'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Global variables for data storage
current_data = None
analysis_results = None
summary_stats = None

def load_and_process_data(filepath):
    """Load and process Netflix dataset"""
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} records from {filepath}")
        
        # Print column names for debugging
        logger.info(f"Dataset columns: {list(df.columns)}")
        
        # Basic cleaning
        df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
        df['Release_Year'] = df['Release_Date'].dt.year
        
        # Fill missing values
        df['Country'] = df['Country'].fillna('Unknown')
        df['Type'] = df['Type'].fillna('Unknown') 
        df['Category'] = df['Category'].fillna('Unknown')
        df['Director'] = df['Director'].fillna('Unknown')
        df['Cast'] = df['Cast'].fillna('Unknown')
        df['Description'] = df['Description'].fillna('')
        
        # Calculate content age
        current_year = 2021
        df['Content_Age'] = current_year - df['Release_Year']
        
        logger.info("Data processing completed successfully")
        return df
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise

def generate_summary_stats(df):
    """Generate summary statistics"""
    try:
        summary = {
            'total_records': len(df),
            'date_range': f"{df['Release_Year'].min():.0f} - {df['Release_Year'].max():.0f}",
            'movies': len(df[df['Category'] == 'Movie']),
            'tv_shows': len(df[df['Category'] == 'TV Show']),
            'unique_countries': df['Country'].nunique(),
            'unique_genres': df['Type'].nunique()
        }
        logger.info(f"Summary stats generated: {summary}")
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return {}

@app.route('/')
def index():
    """Landing page"""
    global current_data, summary_stats
    
    has_data = current_data is not None
    data_info = None
    
    if has_data and summary_stats:
        data_info = {
            'total_records': summary_stats.get('total_records', 0),
            'movies': summary_stats.get('movies', 0),
            'tv_shows': summary_stats.get('tv_shows', 0),
            'date_range': summary_stats.get('date_range', 'Unknown')
        }
    
    return render_template('index.html', has_data=has_data, data_info=data_info)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and processing"""
    global current_data, analysis_results, summary_stats
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(filepath)
                
                # Process the data
                current_data = load_and_process_data(filepath)
                summary_stats = generate_summary_stats(current_data)
                
                flash(f'Successfully processed {len(current_data)} records!', 'success')
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Please upload a CSV file', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    """Main analytics dashboard"""
    global current_data, summary_stats
    
    if current_data is None:
        flash('Please upload a dataset first', 'warning')
        return redirect(url_for('upload_file'))
    
    return render_template('dashboard.html', summary=summary_stats)

@app.route('/api/temporal-chart')
def api_temporal_chart():
    """API endpoint for temporal analysis chart"""
    global current_data
    
    logger.info("Temporal chart requested")
    
    if current_data is None:
        logger.error("No data available for temporal chart")
        return jsonify({'error': 'No data available'}), 400
    
    try:
        # Year-wise content distribution
        yearly_data = current_data.groupby(['Release_Year', 'Category']).size().unstack(fill_value=0)
        logger.info(f"Temporal chart data shape: {yearly_data.shape}")
        
        # Safely get data
        movies_data = yearly_data.get('Movie', pd.Series()).fillna(0).tolist()
        tv_shows_data = yearly_data.get('TV Show', pd.Series()).fillna(0).tolist()
        years = yearly_data.index.tolist()
        
        # Create chart data
        chart_data = {
            'data': [
                {
                    'x': years,
                    'y': movies_data,
                    'mode': 'lines+markers',
                    'name': 'Movies',
                    'line': {'color': '#E50914', 'width': 3},
                    'marker': {'size': 8}
                },
                {
                    'x': years,
                    'y': tv_shows_data,
                    'mode': 'lines+markers',
                    'name': 'TV Shows',
                    'line': {'color': '#564D4D', 'width': 3},
                    'marker': {'size': 8}
                }
            ],
            'layout': {
                'title': {
                    'text': 'Netflix Content Growth Over Time',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                'xaxis': {'title': 'Year'},
                'yaxis': {'title': 'Number of Titles'},
                'template': 'plotly_white',
                'height': 500,
                'hovermode': 'x unified'
            }
        }
        
        logger.info("Temporal chart data created successfully")
        return jsonify({'chart': json.dumps(chart_data)})
        
    except Exception as e:
        logger.error(f"Error creating temporal chart: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/genre-chart')
def api_genre_chart():
    """API endpoint for genre analysis chart - COMPLETELY FIXED"""
    global current_data
    
    logger.info("Genre chart requested")
    
    if current_data is None:
        logger.error("No data available for genre chart")
        return jsonify({'error': 'No data available'}), 400
    
    try:
        # Extract all genres with better error handling
        all_genres = []
        
        # Check if 'Type' column exists
        if 'Type' not in current_data.columns:
            logger.error("Type column not found in dataset")
            return jsonify({'error': 'Type column not found in dataset'}), 500
        
        for idx, genres in enumerate(current_data['Type'].dropna()):
            try:
                if isinstance(genres, str) and genres.strip() and genres != 'Unknown':
                    genre_list = [genre.strip() for genre in genres.split(',') if genre.strip()]
                    all_genres.extend(genre_list)
            except Exception as e:
                logger.warning(f"Error processing genre at index {idx}: {str(e)}")
                continue
        
        if not all_genres:
            logger.warning("No genres found in dataset")
            return jsonify({'error': 'No valid genres found in dataset'}), 400
        
        # Count and get top 10
        genre_counts = Counter(all_genres)
        top_genres_items = genre_counts.most_common(10)
        
        # Convert to lists safely
        genre_names = [item[0] for item in top_genres_items]
        genre_values = [item[1] for item in top_genres_items]
        
        logger.info(f"Found {len(genre_counts)} unique genres, showing top {len(genre_names)}")
        
        chart_data = {
            'data': [{
                'x': genre_values,
                'y': genre_names,
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': '#E50914'},
                'text': genre_values,
                'textposition': 'auto',
                'hovertemplate': '<b>%{y}</b><br>Count: %{x}<extra></extra>'
            }],
            'layout': {
                'title': {
                    'text': 'Top 10 Netflix Genres by Content Count',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                'xaxis': {'title': 'Number of Titles'},
                'yaxis': {'title': 'Genre'},
                'template': 'plotly_white',
                'height': 500,
                'margin': {'l': 100, 'r': 50, 't': 80, 'b': 50}
            }
        }
        
        logger.info("Genre chart data created successfully")
        return jsonify({'chart': json.dumps(chart_data)})
        
    except Exception as e:
        logger.error(f"Error creating genre chart: {str(e)}")
        return jsonify({'error': f'Failed to create genre chart: {str(e)}'}), 500

@app.route('/api/geographic-chart')
def api_geographic_chart():
    """API endpoint for geographic analysis chart - COMPLETELY FIXED"""
    global current_data
    
    logger.info("Geographic chart requested")
    
    if current_data is None:
        logger.error("No data available for geographic chart")
        return jsonify({'error': 'No data available'}), 400
    
    try:
        # Extract all countries with better error handling
        all_countries = []
        
        # Check if 'Country' column exists
        if 'Country' not in current_data.columns:
            logger.error("Country column not found in dataset")
            return jsonify({'error': 'Country column not found in dataset'}), 500
        
        for idx, countries in enumerate(current_data['Country'].dropna()):
            try:
                if isinstance(countries, str) and countries.strip() and countries != 'Unknown':
                    country_list = [country.strip() for country in countries.split(',') if country.strip()]
                    all_countries.extend(country_list)
            except Exception as e:
                logger.warning(f"Error processing country at index {idx}: {str(e)}")
                continue
        
        if not all_countries:
            logger.warning("No countries found in dataset")
            return jsonify({'error': 'No valid countries found in dataset'}), 400
        
        # Count and get top 10
        country_counts = Counter(all_countries)
        top_countries_items = country_counts.most_common(10)
        
        # Convert to lists safely
        country_names = [item[0] for item in top_countries_items]
        country_values = [item[1] for item in top_countries_items]
        
        logger.info(f"Found {len(country_counts)} unique countries, showing top {len(country_names)}")
        
        chart_data = {
            'data': [{
                'x': country_values,
                'y': country_names,
                'type': 'bar',
                'orientation': 'h',
                'marker': {'color': 'darkblue'},
                'text': country_values,
                'textposition': 'auto',
                'hovertemplate': '<b>%{y}</b><br>Content Count: %{x}<extra></extra>'
            }],
            'layout': {
                'title': {
                    'text': 'Top 10 Countries by Content Count',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                'xaxis': {'title': 'Number of Titles'},
                'yaxis': {'title': 'Country'},
                'template': 'plotly_white',
                'height': 500,
                'margin': {'l': 150, 'r': 50, 't': 80, 'b': 50}
            }
        }
        
        logger.info("Geographic chart data created successfully")
        return jsonify({'chart': json.dumps(chart_data)})
        
    except Exception as e:
        logger.error(f"Error creating geographic chart: {str(e)}")
        return jsonify({'error': f'Failed to create geographic chart: {str(e)}'}), 500

@app.route('/api/content-mix-chart')
def api_content_mix_chart():
    """API endpoint for content mix chart"""
    global current_data
    
    logger.info("Content mix chart requested")
    
    if current_data is None:
        logger.error("No data available for content mix chart")
        return jsonify({'error': 'No data available'}), 400
    
    try:
        category_counts = current_data['Category'].value_counts()
        logger.info(f"Content mix data: {dict(category_counts)}")
        
        chart_data = {
            'data': [{
                'labels': category_counts.index.tolist(),
                'values': category_counts.values.tolist(),
                'type': 'pie',
                'marker': {'colors': ['#E50914', '#564D4D']},
                'textinfo': 'label+percent',
                'textfont': {'size': 14},
                'hovertemplate': '<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            }],
            'layout': {
                'title': {
                    'text': 'Netflix Content Mix: Movies vs TV Shows',
                    'x': 0.5,
                    'font': {'size': 20}
                },
                'template': 'plotly_white',
                'height': 400,
                'showlegend': True
            }
        }
        
        logger.info("Content mix chart data created successfully")
        return jsonify({'chart': json.dumps(chart_data)})
        
    except Exception as e:
        logger.error(f"Error creating content mix chart: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add a debug endpoint to check data
@app.route('/api/debug-data')
def api_debug_data():
    """Debug endpoint to check current data"""
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    debug_info = {
        'total_records': len(current_data),
        'columns': list(current_data.columns),
        'sample_types': current_data['Type'].head(10).tolist() if 'Type' in current_data.columns else [],
        'sample_countries': current_data['Country'].head(10).tolist() if 'Country' in current_data.columns else [],
        'categories': current_data['Category'].value_counts().to_dict() if 'Category' in current_data.columns else {}
    }
    
    return jsonify(debug_info)

@app.route('/analysis')
def analysis_page():
    """Detailed analysis page"""
    global current_data, summary_stats
    
    if current_data is None:
        flash('Please upload and process a dataset first', 'warning')
        return redirect(url_for('upload_file'))
    
    try:
        # Simple analysis for now
        report = {
            'executive_summary': {
                'total_content': len(current_data),
                'date_range': summary_stats.get('date_range', 'Unknown'),
                'movie_percentage': round((summary_stats.get('movies', 0) / len(current_data) * 100), 1) if len(current_data) > 0 else 0
            }
        }
        
        return render_template('analysis.html', report=report)
        
    except Exception as e:
        logger.error(f"Error generating analysis: {str(e)}")
        flash(f'Error generating analysis: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/exports', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Run the application
    print("🚀 Starting Netflix Analysis Application - FINAL VERSION")
    print("📱 Open: http://localhost:5000")
    print("📊 All 4 charts should now load perfectly!")
    print("🔧 Enhanced logging and error handling included")
    
    app.run(debug=True, host='0.0.0.0', port=5000)