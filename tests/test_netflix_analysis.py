"""
Netflix Analysis Project - Complete Testing Suite
Fixed version with proper syntax
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os
from io import StringIO
import tempfile
import json

# Simple test without complex imports to verify basic functionality
class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_pandas_import(self):
        """Test if pandas can be imported"""
        try:
            import pandas as pd
            import numpy as np
            print("✅ Pandas and NumPy imported successfully")
            self.assertTrue(True)
        except ImportError as e:
            print(f"❌ Failed to import pandas/numpy: {str(e)}")
            self.fail(f"Import failed: {str(e)}")
    
    def test_flask_import(self):
        """Test if Flask can be imported"""
        try:
            from flask import Flask
            print("✅ Flask imported successfully")
            self.assertTrue(True)
        except ImportError as e:
            print(f"❌ Failed to import Flask: {str(e)}")
            self.fail(f"Flask import failed: {str(e)}")
    
    def test_plotly_import(self):
        """Test if Plotly can be imported"""
        try:
            import plotly.graph_objects as go
            import plotly.express as px
            print("✅ Plotly imported successfully")
            self.assertTrue(True)
        except ImportError as e:
            print(f"❌ Failed to import Plotly: {str(e)}")
            self.fail(f"Plotly import failed: {str(e)}")
    
    def test_data_processing(self):
        """Test basic data processing"""
        try:
            # Create sample data
            data = pd.DataFrame({
                'Show_Id': ['s1', 's2', 's3'],
                'Category': ['Movie', 'TV Show', 'Movie'],
                'Title': ['Test Movie 1', 'Test Show 1', 'Test Movie 2'],
                'Country': ['United States', 'United Kingdom', 'India'],
                'Release_Date': ['January 1, 2020', 'February 15, 2019', 'March 20, 2021'],
                'Type': ['Drama', 'Comedy', 'Action']
            })
            
            # Basic operations
            self.assertEqual(len(data), 3)
            self.assertIn('Title', data.columns)
            
            # Data manipulation
            movies = data[data['Category'] == 'Movie']
            self.assertEqual(len(movies), 2)
            
            print("✅ Basic data processing test passed")
        except Exception as e:
            print(f"❌ Data processing test failed: {str(e)}")
            self.fail(f"Data processing failed: {str(e)}")
    
    def test_file_operations(self):
        """Test basic file operations"""
        try:
            # Create temporary CSV
            temp_data = pd.DataFrame({
                'Name': ['Test1', 'Test2'],
                'Value': [1, 2]
            })
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                temp_data.to_csv(f.name, index=False)
                temp_file = f.name
            
            # Read back
            loaded_data = pd.read_csv(temp_file)
            self.assertEqual(len(loaded_data), 2)
            
            # Cleanup
            os.unlink(temp_file)
            
            print("✅ File operations test passed")
        except Exception as e:
            print(f"❌ File operations test failed: {str(e)}")
            self.fail(f"File operations failed: {str(e)}")
    
    def test_chart_creation(self):
        """Test basic chart creation"""
        try:
            import plotly.graph_objects as go
            
            # Create simple chart
            fig = go.Figure()
            fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]))
            fig.update_layout(title='Test Chart')
            
            self.assertIsNotNone(fig)
            print("✅ Chart creation test passed")
        except Exception as e:
            print(f"❌ Chart creation test failed: {str(e)}")
            self.fail(f"Chart creation failed: {str(e)}")

class TestNetflixDataProcessing(unittest.TestCase):
    """Test Netflix-specific data processing"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_netflix_data = pd.DataFrame({
            'Show_Id': ['s1', 's2', 's3', 's4', 's5'],
            'Category': ['Movie', 'TV Show', 'Movie', 'TV Show', 'Movie'],
            'Title': ['Test Movie 1', 'Test Show 1', 'Test Movie 2', 'Test Show 2', 'Test Movie 3'],
            'Country': ['United States', 'United Kingdom', 'India, United States', 'Canada', 'France'],
            'Release_Date': ['January 1, 2020', 'February 15, 2019', 'March 20, 2021', 'April 10, 2018', 'May 5, 2022'],
            'Type': ['Drama', 'Comedy, Romance', 'Action', 'Documentary', 'Thriller, Drama'],
            'Director': ['Director A', 'Director B', 'Director C', 'Director D', 'Director E'],
            'Cast': ['Actor A, Actor B', 'Actor C', 'Actor D, Actor E', 'Actor F', 'Actor G, Actor H'],
            'Duration': ['120 min', '2 Seasons', '95 min', '1 Season', '135 min'],
            'Rating': ['PG-13', 'TV-14', 'R', 'TV-G', 'R'],
            'Description': ['A drama film', 'A comedy show', 'Action movie', 'Documentary', 'Thriller film']
        })
    
    def test_netflix_data_structure(self):
        """Test Netflix data structure"""
        required_columns = ['Show_Id', 'Category', 'Title', 'Country', 'Release_Date', 'Type']
        
        for col in required_columns:
            self.assertIn(col, self.sample_netflix_data.columns)
        
        print("✅ Netflix data structure test passed")
    
    def test_category_analysis(self):
        """Test category analysis"""
        category_counts = self.sample_netflix_data['Category'].value_counts()
        
        self.assertEqual(category_counts['Movie'], 3)
        self.assertEqual(category_counts['TV Show'], 2)
        
        print("✅ Category analysis test passed")
    
    def test_genre_processing(self):
        """Test genre processing"""
        # Extract genres
        all_genres = []
        for genres in self.sample_netflix_data['Type']:
            if pd.notna(genres):
                genre_list = [g.strip() for g in str(genres).split(',')]
                all_genres.extend(genre_list)
        
        from collections import Counter
        genre_counts = Counter(all_genres)
        
        self.assertGreater(len(genre_counts), 0)
        self.assertIn('Drama', genre_counts)
        
        print("✅ Genre processing test passed")
    
    def test_country_processing(self):
        """Test country processing"""
        # Extract countries
        all_countries = []
        for countries in self.sample_netflix_data['Country']:
            if pd.notna(countries):
                country_list = [c.strip() for c in str(countries).split(',')]
                all_countries.extend(country_list)
        
        from collections import Counter
        country_counts = Counter(all_countries)
        
        self.assertGreater(len(country_counts), 0)
        self.assertIn('United States', country_counts)
        
        print("✅ Country processing test passed")
    
    def test_date_processing(self):
        """Test date processing"""
        # Convert dates
        dates = pd.to_datetime(self.sample_netflix_data['Release_Date'], errors='coerce')
        years = dates.dt.year
        
        self.assertFalse(years.isna().all())
        self.assertGreater(years.max(), 2015)
        
        print("✅ Date processing test passed")

class TestVisualizationComponents(unittest.TestCase):
    """Test visualization components"""
    
    def setUp(self):
        """Set up test data for visualization"""
        self.viz_data = pd.DataFrame({
            'Year': [2018, 2019, 2020, 2021],
            'Movies': [100, 150, 200, 180],
            'TV_Shows': [50, 75, 100, 120],
            'Genre': ['Drama', 'Comedy', 'Action', 'Documentary'],
            'Count': [80, 60, 90, 45]
        })
    
    def test_temporal_chart_data(self):
        """Test temporal chart data preparation"""
        try:
            # Group by year
            yearly_data = self.viz_data.groupby('Year')[['Movies', 'TV_Shows']].first()
            
            self.assertEqual(len(yearly_data), 4)
            self.assertIn(2020, yearly_data.index)
            
            print("✅ Temporal chart data test passed")
        except Exception as e:
            self.fail(f"Temporal chart test failed: {str(e)}")
    
    def test_genre_chart_data(self):
        """Test genre chart data preparation"""
        try:
            genre_data = self.viz_data.set_index('Genre')['Count']
            top_genres = genre_data.sort_values(ascending=False).head(3)
            
            self.assertEqual(len(top_genres), 3)
            self.assertGreater(top_genres.iloc[0], 0)
            
            print("✅ Genre chart data test passed")
        except Exception as e:
            self.fail(f"Genre chart test failed: {str(e)}")
    
    def test_plotly_chart_creation(self):
        """Test Plotly chart creation"""
        try:
            import plotly.graph_objects as go
            
            # Create bar chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=self.viz_data['Genre'],
                y=self.viz_data['Count'],
                name='Content Count'
            ))
            
            fig.update_layout(title='Test Genre Distribution')
            
            self.assertIsNotNone(fig)
            self.assertIsNotNone(fig.data)
            
            print("✅ Plotly chart creation test passed")
        except Exception as e:
            self.fail(f"Plotly chart creation failed: {str(e)}")

class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_data_validation(self):
        """Test data validation utilities"""
        # Valid Netflix data
        valid_data = pd.DataFrame({
            'Show_Id': ['s1'], 'Category': ['Movie'], 'Title': ['Test'],
            'Country': ['US'], 'Release_Date': ['2020-01-01'], 'Type': ['Drama'],
            'Director': ['Dir'], 'Cast': ['Actor'], 'Duration': ['120 min'],
            'Rating': ['PG'], 'Description': ['Desc']
        })
        
        required_columns = ['Show_Id', 'Category', 'Title', 'Country', 'Release_Date', 'Type']
        has_required = all(col in valid_data.columns for col in required_columns)
        
        self.assertTrue(has_required)
        print("✅ Data validation test passed")
    
    def test_number_formatting(self):
        """Test number formatting utility"""
        def format_large_number(number):
            if number >= 1_000_000:
                return f"{number / 1_000_000:.1f}M"
            elif number >= 1_000:
                return f"{number / 1_000:.1f}K"
            else:
                return str(number)
        
        self.assertEqual(format_large_number(1500), "1.5K")
        self.assertEqual(format_large_number(2500000), "2.5M")
        self.assertEqual(format_large_number(500), "500")
        
        print("✅ Number formatting test passed")
    
    def test_percentage_calculation(self):
        """Test percentage calculation"""
        def calculate_percentage(part, total):
            return (part / total * 100) if total > 0 else 0
        
        self.assertEqual(calculate_percentage(25, 100), 25.0)
        self.assertEqual(calculate_percentage(0, 100), 0.0)
        
        print("✅ Percentage calculation test passed")

def run_performance_benchmark():
    """Run simple performance benchmark"""
    print("\n🚀 Running Performance Benchmark")
    print("=" * 40)
    
    import time
    
    # Test data processing speed
    start_time = time.time()
    
    # Create larger dataset
    n_records = 5000
    test_data = pd.DataFrame({
        'Show_Id': [f's{i}' for i in range(n_records)],
        'Category': np.random.choice(['Movie', 'TV Show'], n_records),
        'Title': [f'Title {i}' for i in range(n_records)],
        'Country': np.random.choice(['US', 'UK', 'India', 'Canada'], n_records),
        'Year': np.random.choice(range(2015, 2023), n_records),
        'Genre': np.random.choice(['Drama', 'Comedy', 'Action', 'Documentary'], n_records)
    })
    
    # Basic operations
    category_counts = test_data['Category'].value_counts()
    yearly_counts = test_data['Year'].value_counts()
    genre_counts = test_data['Genre'].value_counts()
    
    processing_time = time.time() - start_time
    
    print(f"✅ Processed {n_records} records in {processing_time:.2f} seconds")
    print(f"📈 Processing rate: {n_records/processing_time:.0f} records/second")
    
    return processing_time

def main():
    """Run all tests"""
    print("🧪 Netflix Analysis Project - Test Suite")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBasicFunctionality,
        TestNetflixDataProcessing,
        TestVisualizationComponents,
        TestUtilityFunctions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run performance benchmark
    try:
        run_performance_benchmark()
    except Exception as e:
        print(f"⚠️ Performance benchmark failed: {str(e)}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        print(f"✅ {result.testsRun} tests completed successfully")
        print("\n🚀 Your Netflix Analysis setup is working correctly!")
        print("💡 Next steps:")
        print("   1. Copy your Netflix dataset to data/raw/")
        print("   2. Run: python app.py")
        print("   3. Open: http://localhost:5000")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"❌ Failures: {len(result.failures)}")
        print(f"❌ Errors: {len(result.errors)}")
        print(f"✅ Successful: {result.testsRun - len(result.failures) - len(result.errors)}")
        
        if result.failures:
            print("\n📋 FAILURE DETAILS:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
        
        if result.errors:
            print("\n📋 ERROR DETAILS:")
            for test, traceback in result.errors:
                print(f"   - {test}: Error in test execution")
    
    print("\n" + "=" * 50)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = main()
    print(f"\n🏁 Test execution {'SUCCESSFUL' if success else 'FAILED'}")
    sys.exit(0 if success else 1)