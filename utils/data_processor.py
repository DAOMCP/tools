import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta

class DataProcessor:
    """
    Process and analyze cryptocurrency data
    """
    
    @staticmethod
    def filter_tokens(df, filter_settings):
        """
        Filter tokens based on user-defined criteria
        """
        if df.empty:
            return df
        
        # Apply market cap filters
        filtered_df = df.copy()
        
        # Handle market cap filtering
        market_cap_min = filter_settings.get("market_cap_min", 0)
        market_cap_max = filter_settings.get("market_cap_max", float('inf'))
        
        filtered_df = filtered_df[
            (filtered_df['market_cap'] >= market_cap_min) & 
            (filtered_df['market_cap'] <= market_cap_max)
        ]
        
        # Filter by market cap category if specified
        category = filter_settings.get("category", "all")
        if category != "all":
            filtered_df = filtered_df[filtered_df['market_cap_category'] == category]
        
        # Filter by AI category if specified
        ai_category = filter_settings.get("ai_category", "all")
        if ai_category != "all" and 'ai_category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['ai_category'] == ai_category]
        
        # Apply sorting
        sort_by = filter_settings.get("sort_by", "market_cap")
        sort_order = filter_settings.get("sort_order", "desc")
        
        if sort_by in filtered_df.columns:
            is_ascending = sort_order == "asc"
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=is_ascending)
        
        return filtered_df
    
    @staticmethod
    def get_top_gainers_losers(df, n=5):
        """
        Get top gainers and losers based on 24h price change
        """
        if df.empty or n <= 0:
            return pd.DataFrame(), pd.DataFrame()
        
        # Make sure we have the price change column
        if 'price_change_24h' not in df.columns:
            return pd.DataFrame(), pd.DataFrame()
        
        # Sort by price change
        df_sorted = df.sort_values(by='price_change_24h')
        
        # Get losers (bottom n)
        losers = df_sorted.head(n).copy()
        
        # Get gainers (top n)
        gainers = df_sorted.tail(n).iloc[::-1].copy()
        
        return gainers, losers
    
    @staticmethod
    def calculate_market_stats(df):
        """
        Calculate overall market statistics
        """
        stats = {}
        
        if df.empty:
            return {
                "total_tokens": 0,
                "total_market_cap": 0,
                "avg_24h_change": 0,
                "token_counts_by_cap": {}
            }
        
        # Total number of tokens
        stats["total_tokens"] = len(df)
        
        # Total market cap
        stats["total_market_cap"] = df['market_cap'].sum()
        
        # Average 24h price change
        stats["avg_24h_change"] = df['price_change_24h'].mean()
        
        # Count tokens by market cap category
        stats["token_counts_by_cap"] = df['market_cap_category'].value_counts().to_dict()
        
        return stats
    
    @staticmethod
    def analyze_token_launch_trends(df):
        """
        Simulate token launch trends based on available data
        Note: This is approximate since CoinGecko doesn't directly provide token launch dates
        """
        if df.empty or 'last_updated' not in df.columns:
            return pd.DataFrame()
            
        # Convert last_updated to datetime
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        # Create a time-based analysis (this is approximate)
        # Group tokens by month of last update as a proxy for activity
        df['month'] = df['last_updated'].dt.strftime('%Y-%m')
        monthly_counts = df.groupby('month').size().reset_index(name='count')
        monthly_counts['month'] = pd.to_datetime(monthly_counts['month'])
        
        # Sort by month
        monthly_counts = monthly_counts.sort_values('month')
        
        return monthly_counts
    
    @staticmethod
    def format_number(num, precision=2):
        """Format large numbers for display"""
        if num is None:
            return "N/A"
            
        if abs(num) >= 1_000_000_000:
            return f"${num / 1_000_000_000:.{precision}f}B"
        elif abs(num) >= 1_000_000:
            return f"${num / 1_000_000:.{precision}f}M"
        elif abs(num) >= 1_000:
            return f"${num / 1_000:.{precision}f}K"
        else:
            return f"${num:.{precision}f}"
