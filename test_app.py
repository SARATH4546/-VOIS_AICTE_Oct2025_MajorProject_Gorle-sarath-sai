"""
Simple test to verify the application works
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test if all modules can be imported"""
    try:
        from src.data.data_loader import NetflixDataProcessor
        from src.analysis.netflix_analyzer import NetflixAnalyzer
        from src.visualization.netflix_visualizer import NetflixVisualizer
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_processing():
    """Test data processing with sample data"""
    try:
        import pandas as pd
        
        # Create sample data
        sample_data = pd.DataFrame({
            'Show_Id': ['s1', 's2'],
            'Category': ['Movie', 'TV Show'],
            'Title': ['Test Movie', 'Test Show'],
            'Country': ['United States', 'United Kingdom'],
            'Release_Date': ['January 1, 2020', 'February 1, 2021'],
            'Type': ['Drama', 'Comedy'],
            'Duration': ['90 min', '1 Season'],
            'Description': ['Test description 1', 'Test description 2']
        })
        
        from src.analysis.netflix_analyzer import NetflixAnalyzer
        analyzer = NetflixAnalyzer(sample_data)
        
        print("✅ Data processing test passed")
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running application tests...\n")
    
    test1 = test_imports()
    test2 = test_data_processing()
    
    if test1 and test2:
        print("\n🎉 All tests passed! Your application is ready to run.")
    else:
        print("\n❌ Some tests failed. Please check your setup.")