"""
MyAnimeList Dataset - Comprehensive EDA and Dashboard Creator
Dark Theme, Modern Design inspired by Fitonist dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# Set style
plt.style.use('dark_background')
sns.set_palette("husl")

class AnimeAnalyzer:
    """Comprehensive MyAnimeList Dataset Analyzer"""
    
    def __init__(self, data_path='data'):
        self.data_path = data_path
        self.anime_df = None
        self.stats = {}
        
    def load_data(self):
        """Load MyAnimeList dataset"""
        print("📊 Loading MyAnimeList dataset...")
        
        # Try to find CSV files in data folder
        if os.path.exists(self.data_path):
            csv_files = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]
        else:
            # Look in current directory
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            self.data_path = '.'
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found!")
        
        print(f"Found {len(csv_files)} CSV file(s): {csv_files}")
        
        # Load the main anime dataset (usually the largest file or named anime.csv)
        for file in csv_files:
            if 'anime' in file.lower() and 'dataset' in file.lower():
                self.anime_df = pd.read_csv(os.path.join(self.data_path, file))
                print(f"✓ Loaded {file}: {self.anime_df.shape[0]:,} rows, {self.anime_df.shape[1]} columns")
                break
        
        if self.anime_df is None:
            # Try final_animedataset
            for file in csv_files:
                if 'final' in file.lower() or 'anime' in file.lower():
                    self.anime_df = pd.read_csv(os.path.join(self.data_path, file))
                    print(f"✓ Loaded {file}: {self.anime_df.shape[0]:,} rows, {self.anime_df.shape[1]} columns")
                    break
        
        if self.anime_df is None:
            # Load the first CSV file
            self.anime_df = pd.read_csv(os.path.join(self.data_path, csv_files[0]))
            print(f"✓ Loaded {csv_files[0]}: {self.anime_df.shape[0]:,} rows, {self.anime_df.shape[1]} columns")
        
        return self.anime_df
    
    def initial_exploration(self):
        """Perform initial data exploration"""
        print("\n" + "="*80)
        print("📋 INITIAL DATA EXPLORATION")
        print("="*80)
        
        print(f"\n📊 Dataset Shape: {self.anime_df.shape[0]:,} rows × {self.anime_df.shape[1]} columns")
        print(f"\n📝 Column Names:\n{list(self.anime_df.columns)}")
        print(f"\n🔍 Data Types:\n{self.anime_df.dtypes}")
        print(f"\n📈 First 5 rows:")
        print(self.anime_df.head())
        print(f"\n📉 Last 5 rows:")
        print(self.anime_df.tail())
        print(f"\n📊 Summary Statistics:")
        print(self.anime_df.describe())
        print(f"\n❓ Missing Values:")
        missing = self.anime_df.isnull().sum()
        missing_pct = (missing / len(self.anime_df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False))
        
        # Store initial stats
        self.stats['total_anime'] = len(self.anime_df)
        self.stats['total_columns'] = len(self.anime_df.columns)
        self.stats['missing_values'] = self.anime_df.isnull().sum().sum()
        
        return self.anime_df.info()
    
    def clean_data(self):
        """Clean and prepare data"""
        print("\n" + "="*80)
        print("🧹 DATA CLEANING")
        print("="*80)
        
        initial_rows = len(self.anime_df)
        
        # Remove duplicates
        duplicates = self.anime_df.duplicated().sum()
        if duplicates > 0:
            self.anime_df = self.anime_df.drop_duplicates()
            print(f"✓ Removed {duplicates:,} duplicate rows")
        
        # Detect common column names (case-insensitive)
        cols_lower = {col.lower(): col for col in self.anime_df.columns}
        
        # Handle missing values strategically
        for col in self.anime_df.columns:
            missing_count = self.anime_df[col].isnull().sum()
            if missing_count > 0:
                missing_pct = (missing_count / len(self.anime_df) * 100)
                
                if missing_pct > 70:
                    print(f"⚠️  Column '{col}' has {missing_pct:.1f}% missing - keeping but noting")
                elif self.anime_df[col].dtype in ['int64', 'float64']:
                    # Fill numeric with median (using skipna to avoid errors)
                    try:
                        median_val = self.anime_df[col].median(skipna=True)
                        self.anime_df[col].fillna(median_val, inplace=True)
                        print(f"✓ Filled {missing_count:,} missing values in '{col}' with median")
                    except:
                        self.anime_df[col].fillna(0, inplace=True)
                        print(f"✓ Filled {missing_count:,} missing values in '{col}' with 0")
                else:
                    # Fill categorical with 'Unknown'
                    self.anime_df[col].fillna('Unknown', inplace=True)
                    print(f"✓ Filled {missing_count:,} missing values in '{col}' with 'Unknown'")
        
        final_rows = len(self.anime_df)
        print(f"\n✅ Cleaning complete: {initial_rows:,} → {final_rows:,} rows")
        
        return self.anime_df
    
    def create_derived_features(self):
        """Create useful derived features"""
        print("\n" + "="*80)
        print("🔧 CREATING DERIVED FEATURES")
        print("="*80)
        
        cols_lower = {col.lower(): col for col in self.anime_df.columns}
        
        # Try to extract year from aired/premiered columns
        for potential_col in ['aired', 'premiered', 'start_date', 'year']:
            if potential_col in cols_lower:
                col_name = cols_lower[potential_col]
                try:
                    # Extract year using regex or string operations
                    self.anime_df['year'] = pd.to_datetime(
                        self.anime_df[col_name], errors='coerce'
                    ).dt.year
                    print(f"✓ Extracted year from '{col_name}'")
                    break
                except:
                    pass
        
        # Create rating categories if rating column exists
        if 'score' in cols_lower or 'rating' in cols_lower:
            score_col = cols_lower.get('score', cols_lower.get('rating'))
            try:
                # Convert to numeric first to avoid type errors
                self.anime_df[score_col] = pd.to_numeric(self.anime_df[score_col], errors='coerce')
                self.anime_df['rating_category'] = pd.cut(
                    self.anime_df[score_col],
                    bins=[0, 5, 7, 8.5, 10],
                    labels=['Poor', 'Average', 'Good', 'Excellent']
                )
                print(f"✓ Created rating categories from '{score_col}'")
            except Exception as e:
                print(f"⚠️  Could not create rating categories: {e}")
        
        # Create popularity tiers if members/favorites exists
        for col_name in ['members', 'favorites', 'popularity']:
            if col_name in cols_lower:
                actual_col = cols_lower[col_name]
                try:
                    # Convert to numeric first
                    self.anime_df[actual_col] = pd.to_numeric(self.anime_df[actual_col], errors='coerce')
                    self.anime_df['popularity_tier'] = pd.qcut(
                        self.anime_df[actual_col].fillna(0),
                        q=4,
                        labels=['Niche', 'Moderate', 'Popular', 'Very Popular'],
                        duplicates='drop'
                    )
                    print(f"✓ Created popularity tiers from '{actual_col}'")
                    break
                except Exception as e:
                    print(f"⚠️  Could not create popularity tiers: {e}")
        
        print(f"\n✅ Feature engineering complete")
        return self.anime_df
    
    def save_results(self, filename='anime_cleaned.csv'):
        """Save cleaned dataset"""
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        self.anime_df.to_csv(output_path, index=False)
        print(f"\n💾 Cleaned dataset saved to: {output_path}")
        return output_path

if __name__ == "__main__":
    print("="*80)
    print("🎌 MyAnimeList Dataset Analysis - Initialization")
    print("="*80)
    
    # Initialize analyzer
    analyzer = AnimeAnalyzer(data_path='data')
    
    try:
        # Load data
        df = analyzer.load_data()
        
        # Explore
        analyzer.initial_exploration()
        
        # Clean
        analyzer.clean_data()
        
        # Create features
        analyzer.create_derived_features()
        
        # Save
        analyzer.save_results()
        
        print("\n" + "="*80)
        print("✅ INITIALIZATION COMPLETE - Ready for visualization!")
        print("="*80)
        print("\nNext step: Run 'python visualizations.py' to create stunning dashboards")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📥 Please ensure CSV files are in the current directory or './data/' folder")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
