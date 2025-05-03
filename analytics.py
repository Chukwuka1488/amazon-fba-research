"""
Analytics helper functions for Amazon FBA data analysis
"""
import pandas as pd
from utilities import extract_numeric_price

def sort_by_rank(df):
    """Sort DataFrame by rank, handling various rank formats"""
    try:
        # Extract numeric rank from rank column
        df['rank_numeric'] = df['rank'].str.extract(r'#?(\d+)').astype(float)
        # Sort by numeric rank
        df = df.sort_values('rank_numeric')
        # Drop the temporary numeric rank column
        df = df.drop('rank_numeric', axis=1)
    except Exception:
        # If extraction fails, just return the original dataframe
        pass
    return df

def get_recommendation(score):
    """Get FBA recommendation based on score"""
    if score >= 75:
        return "High potential - research further"
    elif score >= 50:
        return "Medium potential - consider with caution"
    else:
        return "Low potential - likely too competitive or insufficient demand"

def create_fba_analysis_sheet(df, writer):
    """Create a sheet with FBA opportunity analysis"""
    try:
        # Create a copy with just the FBA-relevant columns
        cols = ['rank', 'title', 'price', 'rating', 'reviews_count', 
                'fba_opportunity_score', 'asin', 'brand']
        fba_df = df[cols].copy()
        
        # Sort by FBA opportunity score (highest first)
        fba_df = fba_df.sort_values('fba_opportunity_score', ascending=False)
        
        # Add a recommendation column
        fba_df['recommendation'] = fba_df['fba_opportunity_score'].apply(get_recommendation)
        
        # Write to Excel
        fba_df.to_excel(writer, sheet_name='FBA Analysis', index=False)
    except Exception as e:
        print(f"Could not create FBA analysis sheet: {e}")

def create_price_analysis_sheet(df, writer):
    """Create a sheet with price distribution analysis"""
    try:
        # Create the numeric price column
        price_data = []
        for price in df['price']:
            price_value = extract_numeric_price(price)
            price_data.append(price_value if price_value is not None else float('nan'))
        
        df['price_numeric'] = price_data
        
        # Define price ranges and analyze
        price_ranges = [
            (0, 10, 'Under $10'),
            (10, 25, '$10-$25'),
            (25, 50, '$25-$50'),
            (50, 100, '$50-$100'),
            (100, float('inf'), 'Over $100')
        ]
        
        # Analyze each price range
        price_analysis = get_price_range_analysis(df, price_ranges)
        
        # Create and save the DataFrame
        price_df = pd.DataFrame(price_analysis)
        price_df.to_excel(writer, sheet_name='Price Analysis', index=False)
    except Exception as e:
        print(f"Could not create price analysis sheet: {e}")

def get_price_range_analysis(df, price_ranges):
    """Analyze product distribution across price ranges"""
    price_analysis = []
    for low, high, label in price_ranges:
        count = ((df['price_numeric'] >= low) & (df['price_numeric'] < high)).sum()
        if count > 0:
            price_analysis.append({
                'Price Range': label,
                'Count': count,
                'Percentage': f"{(count / len(df) * 100):.1f}%",
                'Avg. FBA Score': df.loc[(df['price_numeric'] >= low) & 
                                        (df['price_numeric'] < high), 
                                        'fba_opportunity_score'].mean()
            })
    return price_analysis

def create_metadata_sheet(df, writer, timestamp):
    """Create a metadata sheet with summary information"""
    try:
        high_count = (df['fba_opportunity_score'] >= 75).sum()
        med_count = ((df['fba_opportunity_score'] >= 50) & 
                     (df['fba_opportunity_score'] < 75)).sum()
        low_count = (df['fba_opportunity_score'] < 50).sum()
        
        metadata = [
            {'Metric': 'Report Generated', 'Value': timestamp},
            {'Metric': 'Total Products Analyzed', 'Value': len(df)},
            {'Metric': 'Category', 'Value': 'Electronics'},
            {'Metric': 'Average FBA Score', 'Value': df['fba_opportunity_score'].mean()},
            {'Metric': 'High Potential Products (≥75)', 'Value': high_count},
            {'Metric': 'Medium Potential Products (50-74)', 'Value': med_count},
            {'Metric': 'Low Potential Products (<50)', 'Value': low_count},
        ]
        
        meta_df = pd.DataFrame(metadata)
        meta_df.to_excel(writer, sheet_name='Summary', index=False)
    except Exception as e:
        print(f"Could not create metadata sheet: {e}")