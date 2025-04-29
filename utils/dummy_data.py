import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_tokens(n=50):
    """Generate dummy AI-related token data for testing"""
    np.random.seed(42)  # For reproducible results
    
    # Sample token names and symbols
    ai_words = ["Neural", "Brain", "Synapse", "Cortex", "Mind", "Think", "Logic", "Smart",
                "Quantum", "Deep", "Learn", "Vision", "GPT", "AI", "ML", "Intel", "Cognitive",
                "Data", "Graph", "Compute", "Bot", "Agent", "Node", "Network", "Tensor", "Vector"]
    
    suffixes = ["Network", "Chain", "Protocol", "AI", "Coin", "Token", "DAO", "Base", "Matrix", 
                "Net", "Brain", "Mind", "Core", "Intelligence", "Logic", "Data", "Stream", "Flow"]
    
    tokens = []
    used_names = set()
    
    for i in range(n):
        # Generate unique name
        while True:
            if np.random.random() < 0.7:
                # Two-word name
                name = f"{np.random.choice(ai_words)}{np.random.choice(suffixes)}"
            else:
                # Single word name
                name = np.random.choice(ai_words)
                
            if name not in used_names:
                used_names.add(name)
                break
        
        # Generate symbol (usually 3-4 letters)
        symbol = ''.join([c for c in name if c.isupper()][:4])
        if not symbol:
            # If no uppercase letters, take first 3-4 letters
            symbol = name[:min(4, len(name))].upper()
        
        # Market cap (log-normal distribution to get realistic distribution)
        market_cap_exp = np.random.normal(23, 2.5)  # log distribution centered around ~$10M
        market_cap = np.exp(market_cap_exp)
        
        # Determine market cap category
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
        
        # Price - more realistic for crypto (very wide range)
        if np.random.random() < 0.7:
            # Most tokens have low prices
            price = np.random.lognormal(mean=-1, sigma=3)
        else:
            # Some tokens have higher prices
            price = np.random.lognormal(mean=4, sigma=2)
        
        # 24h volume (correlated with market cap but with noise)
        volume_ratio = np.random.lognormal(mean=-1, sigma=1)  # This gives a ratio typically between 0.1 and 2
        volume_24h = market_cap * volume_ratio
        
        # Price changes (normal distribution)
        price_change_24h = np.random.normal(0, 10)  # std dev of 10% is realistic for crypto
        price_change_7d = np.random.normal(0, 20)   # more variance over longer periods
        
        # Last updated - within the last 1-30 days
        days_ago = np.random.randint(1, 30)
        last_updated = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        # Dummy image URL
        image = f"https://example.com/coins/{i}.png"
        
        # Token ID (for API calls)
        token_id = name.lower().replace(' ', '-')
        
        tokens.append({
            "id": token_id,
            "name": name,
            "symbol": symbol,
            "market_cap": market_cap,
            "market_cap_category": market_cap_category,
            "price": price,
            "volume_24h": volume_24h,
            "price_change_24h": price_change_24h,
            "price_change_7d": price_change_7d,
            "image": image,
            "last_updated": last_updated,
        })
    
    return pd.DataFrame(tokens)

def generate_historical_data(days=30, intervals_per_day=24):
    """Generate synthetic price history data"""
    total_intervals = days * intervals_per_day
    timestamps = []
    prices = []
    market_caps = []
    volumes = []
    
    # Generate timestamps
    now = datetime.now()
    for i in range(total_intervals):
        timestamp = now - timedelta(hours=i)
        timestamps.append(timestamp)
    
    # Sort timestamps in ascending order
    timestamps.sort()
    
    # Convert to milliseconds for API compatibility
    timestamp_ms = [int(ts.timestamp() * 1000) for ts in timestamps]
    
    # Generate price data with random walk
    price = 100.0  # Starting price
    price_volatility = 0.02  # 2% average move per interval
    
    for _ in range(total_intervals):
        # Random walk with drift
        price_change = np.random.normal(0.001, price_volatility)  # Small positive drift
        price *= (1 + price_change)
        prices.append(price)
        
        # Market cap is price * some fixed supply
        supply = 1_000_000  # 1 million tokens
        market_cap = price * supply
        market_caps.append(market_cap)
        
        # Volume is roughly proportional to price with randomness
        volume = price * supply * np.random.lognormal(-1, 1) * 0.05  # 5% avg daily volume
        volumes.append(volume)
    
    # Create dataframe
    df = pd.DataFrame({
        "timestamp": timestamp_ms,
        "date": timestamps,
        "price": prices,
        "market_cap": market_caps,
        "volume": volumes
    })
    
    return df

def generate_token_details():
    """Generate detailed information for a token"""
    return {
        "id": "neural-network",
        "name": "Neural Network",
        "symbol": "NNET",
        "categories": ["ai", "smart-contract"],
        "description": {
            "en": "Neural Network is a decentralized artificial intelligence platform that enables developers to build, train, and deploy AI models on the blockchain. The platform uses NNET tokens for governance, staking, and accessing computing resources."
        },
        "links": {
            "homepage": ["https://example.com/neural-network"],
            "blockchain_site": ["https://example.com/explorer/neural-network"],
            "twitter_screen_name": "neuralnetwork",
            "telegram_channel_identifier": "neuralnetwork_official",
            "subreddit_url": "https://reddit.com/r/neuralnetwork",
            "repos_url": {
                "github": ["https://github.com/neural-network"]
            }
        },
        "market_data": {
            "current_price": {
                "usd": 12.34
            },
            "market_cap": {
                "usd": 123400000
            },
            "market_cap_rank": 87,
            "total_volume": {
                "usd": 45600000
            },
            "high_24h": {
                "usd": 13.45
            },
            "low_24h": {
                "usd": 11.23
            },
            "price_change_percentage_24h": 5.67,
            "price_change_percentage_7d": 12.34,
            "price_change_percentage_14d": 8.9,
            "price_change_percentage_30d": -3.21,
            "price_change_percentage_60d": 15.43,
            "price_change_percentage_200d": 45.67,
            "price_change_percentage_1y": 123.4,
            "circulating_supply": 10000000,
            "total_supply": 20000000,
            "max_supply": 100000000,
            "ath": {
                "usd": 28.9
            },
            "ath_change_percentage": {
                "usd": -57.3
            },
            "ath_date": {
                "usd": "2023-12-31T00:00:00Z"
            }
        },
        "community_data": {
            "twitter_followers": 25600,
            "reddit_subscribers": 12800,
            "telegram_channel_user_count": 34500
        }
    }