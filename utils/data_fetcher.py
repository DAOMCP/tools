import requests
import pandas as pd
import time
import streamlit as st
import os

class CoinGeckoAPI:
    """
    Wrapper for the CoinGecko API to fetch cryptocurrency data
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.api_key = os.getenv("COINGECKO_API_KEY", None)
        self.headers = {}
        if self.api_key:
            self.headers["x-cg-pro-api-key"] = self.api_key
    
    @st.cache_data(ttl=300)  # Cache results for 5 minutes
    def get_ai_related_tokens(self):
        """
        Get AI-related tokens by searching and filtering categories
        """
        try:
            # Get all tokens with AI in name, description or category
            ai_tokens = self._search_ai_tokens()
            
            # Get additional details for each token
            detailed_tokens = self._get_token_details(ai_tokens)
            
            # Create a DataFrame
            return pd.DataFrame(detailed_tokens)
        
        except Exception as e:
            st.error(f"Error fetching AI tokens: {str(e)}")
            return pd.DataFrame()
    
    def _search_ai_tokens(self):
        """Search for AI-related tokens"""
        ai_tokens = []
        
        # Get all cryptocurrency categories
        categories_url = f"{self.BASE_URL}/coins/categories/list"
        categories_response = self.session.get(categories_url, headers=self.headers)
        categories_response.raise_for_status()
        
        ai_categories = [
            cat["category_id"] for cat in categories_response.json() 
            if "ai" in cat["name"].lower() or "artificial intelligence" in cat["name"].lower()
        ]
        
        # Get coins by AI categories
        for category in ai_categories:
            category_url = f"{self.BASE_URL}/coins/markets"
            params = {
                "vs_currency": "usd",
                "category": category,
                "order": "market_cap_desc",
                "per_page": 250,
                "page": 1
            }
            
            category_response = self.session.get(category_url, params=params, headers=self.headers)
            category_response.raise_for_status()
            
            ai_tokens.extend(category_response.json())
            
            # Rate limiting to avoid API issues
            time.sleep(1)
        
        # Also do a search for AI-related terms
        search_terms = ["ai", "artificial intelligence", "machine learning", "neural", "gpt"]
        
        for term in search_terms:
            search_url = f"{self.BASE_URL}/search"
            search_response = self.session.get(search_url, params={"query": term}, headers=self.headers)
            search_response.raise_for_status()
            
            # Get coin IDs from search results
            coin_ids = [coin["id"] for coin in search_response.json().get("coins", [])]
            
            # Get detailed info for each coin
            if coin_ids:
                markets_url = f"{self.BASE_URL}/coins/markets"
                params = {
                    "vs_currency": "usd",
                    "ids": ",".join(coin_ids[:25]),  # API limitation
                    "order": "market_cap_desc",
                    "per_page": 250,
                    "page": 1
                }
                
                markets_response = self.session.get(markets_url, params=params, headers=self.headers)
                if markets_response.status_code == 200:
                    ai_tokens.extend(markets_response.json())
            
            # Rate limiting
            time.sleep(1)
        
        # Remove duplicates
        seen_ids = set()
        unique_tokens = []
        
        for token in ai_tokens:
            if token["id"] not in seen_ids:
                seen_ids.add(token["id"])
                unique_tokens.append(token)
        
        return unique_tokens
    
    def _get_token_details(self, tokens):
        """Get detailed information for each token"""
        detailed_tokens = []
        
        for token in tokens:
            token_id = token["id"]
            
            # Add a categorization based on market cap
            market_cap = token.get("market_cap", 0)
            if market_cap is None:
                market_cap = 0
                
            if market_cap >= 1_000_000_000:
                market_cap_category = "Large Cap (>$1B)"
            elif market_cap >= 100_000_000:
                market_cap_category = "Mid Cap ($100M-$1B)"
            elif market_cap >= 10_000_000:
                market_cap_category = "Small Cap ($10M-$100M)"
            elif market_cap >= 1_000_000:
                market_cap_category = "Micro Cap ($1M-$10M)"
            elif market_cap >= 500_000:
                market_cap_category = "Nano Cap ($500K-$1M)"
            else:
                market_cap_category = "Ultra Nano Cap (<$500K)"
                
            token_data = {
                "id": token_id,
                "name": token.get("name", "Unknown"),
                "symbol": token.get("symbol", "").upper(),
                "market_cap": market_cap,
                "market_cap_category": market_cap_category,
                "price": token.get("current_price", 0),
                "volume_24h": token.get("total_volume", 0),
                "price_change_24h": token.get("price_change_percentage_24h", 0),
                "price_change_7d": token.get("price_change_percentage_7d_in_currency", 0),
                "image": token.get("image", ""),
                "last_updated": token.get("last_updated", ""),
            }
            
            detailed_tokens.append(token_data)
        
        return detailed_tokens
    
    @st.cache_data(ttl=300)
    def get_token_historical_data(self, token_id, days=7):
        """Get historical market data for a specific token"""
        url = f"{self.BASE_URL}/coins/{token_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily" if days > 30 else "hourly"
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Convert timestamps and create DataFrame
            prices_df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
            prices_df["date"] = pd.to_datetime(prices_df["timestamp"], unit="ms")
            
            market_caps_df = pd.DataFrame(data["market_caps"], columns=["timestamp", "market_cap"])
            volumes_df = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
            
            # Merge all dataframes
            result = prices_df.merge(market_caps_df[["timestamp", "market_cap"]], on="timestamp")
            result = result.merge(volumes_df[["timestamp", "volume"]], on="timestamp")
            
            return result
        
        except Exception as e:
            st.error(f"Error fetching historical data for {token_id}: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def get_token_details(self, token_id):
        """Get detailed information about a specific token"""
        url = f"{self.BASE_URL}/coins/{token_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "true",
            "developer_data": "false"
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            st.error(f"Error fetching token details for {token_id}: {str(e)}")
            return {}
