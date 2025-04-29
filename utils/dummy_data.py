import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_dummy_tokens(n=50):
    """Generate realistic AI-related token data"""
    np.random.seed(42)  # For reproducible results
    
    # Real-like token names and symbols
    ai_prefixes = ["Neural", "Brain", "Synapse", "Cortex", "Mind", "Think", "Logic", "Smart",
                "Quantum", "Deep", "Learn", "Vision", "GPT", "LLM", "ML", "Intel", "Cognitive",
                "Data", "Graph", "Compute", "Bot", "Agent", "Node", "Network", "Tensor", "Vector", 
                "AI", "Bard", "Claude", "Gemini", "Anthrop", "Diffuse", "Stable", "Midjourney",
                "Gen", "Sentient", "Neuro", "Prompt", "Open", "Dall-E", "Large", "Language"]
    
    ai_suffixes = ["Network", "Chain", "Protocol", "AI", "Coin", "Token", "DAO", "Base", "Matrix", 
                "Net", "Brain", "Mind", "Core", "Intelligence", "Logic", "Data", "Stream", "Flow",
                "X", "Nexus", "Labs", "Tech", "Model", "Compute", "AGI", "Foundation", "Chat", "LLM"]

    # Add some realistic complete names that sound like real projects
    realistic_names = [
        "DeepBrain Chain", "SingularityNET", "Fetch.ai", "Ocean Protocol", "Numeraire", 
        "Matrix AI", "Cortex", "BrainTrust", "Phala Network", "Oasis Network",
        "Akash Network", "Agoric", "The Graph", "NuNet", "Render Network", 
        "OpenAI Token", "Bittensor", "Alethea AI", "DeepMind Protocol", "LangChain",
        "Midjourney Token", "Claude Finance", "Stability AI", "Anthropic", "Gemini AI",
        "Vector Space", "Neural Protocol", "GPT Finance", "TensorTrade", "DataDAO",
        "Diffusion AI", "Neuro Finance", "Prompt Chain", "Agents Network", "LLM Protocol"
    ]
    
    # Get unique symbols from realistic names
    def get_symbol(name):
        if "." in name:
            return name.split(".")[0].upper()
        words = [w for w in name.split() if w not in ["The", "AI", "Protocol", "Network", "Token", "Chain"]]
        if len(words) == 1:
            return words[0][:4].upper()
        else:
            return "".join([word[0] for word in words]).upper()
    
    realistic_symbols = {name: get_symbol(name) for name in realistic_names}
    
    # Generate token data
    tokens = []
    used_names = set()
    used_symbols = set()
    
    # First add the realistic tokens to ensure they're included
    for i, name in enumerate(realistic_names[:min(n, len(realistic_names))]):
        symbol = realistic_symbols[name]
        if symbol in used_symbols:
            # If symbol collision, add a number
            symbol = symbol[:3] + str(random.randint(1, 9))
        
        used_names.add(name)
        used_symbols.add(symbol)
        
        # Use log-normal distribution for realistic market cap distribution
        tier = i // 7  # Divide into tiers for varying market caps
        
        if tier == 0:  # Top tier - large cap ($1B+)
            market_cap = np.random.lognormal(mean=22, sigma=0.5)  # Centered around several billion
            price = np.random.lognormal(mean=1, sigma=1)  # Higher prices
        elif tier == 1:  # Mid tier - mid cap ($100M-$1B)
            market_cap = np.random.lognormal(mean=19.5, sigma=0.4)  # Centered around several hundred million
            price = np.random.lognormal(mean=0, sigma=1)  # Moderate prices
        else:  # Lower tiers
            market_cap = np.random.lognormal(mean=17, sigma=1)  # Smaller caps
            price = np.random.lognormal(mean=-1, sigma=1.5)  # Lower prices
        
        # Volume as percentage of market cap (higher for larger caps)
        volume_factor = np.random.uniform(0.05, 0.25) if tier < 2 else np.random.uniform(0.01, 0.15)
        volume_24h = market_cap * volume_factor
        
        # More dramatic price changes for smaller caps
        volatility_factor = 1 + (tier * 0.5)
        price_change_24h = np.random.normal(0, 4 * volatility_factor)
        price_change_7d = np.random.normal(price_change_24h/2, 8 * volatility_factor)
        
        # Add a "story" to price changes - negative for bear market, positive for bull market
        market_sentiment = np.random.choice([-1, 1], p=[0.3, 0.7])  # 70% bull market
        if market_sentiment > 0:
            price_change_24h = abs(price_change_24h) * np.random.uniform(0.8, 1.2)
            price_change_7d = abs(price_change_7d) * np.random.uniform(0.8, 1.2)
        else:
            price_change_24h = -abs(price_change_24h) * np.random.uniform(0.8, 1.2)
            price_change_7d = -abs(price_change_7d) * np.random.uniform(0.8, 1.2)
        
        # Token ID for API calls
        token_id = name.lower().replace(" ", "-").replace(".", "")
        
        # Determine market cap category
        if market_cap >= 1_000_000_000:
            market_cap_category = "Large Cap (>$1B)"
        elif market_cap >= 100_000_000:
            market_cap_category = "Mid Cap ($100M-$1B)"
        elif market_cap >= 10_000_000:
            market_cap_category = "Small Cap ($10M-$100M)"
        elif market_cap >= 1_000_000:
            market_cap_category = "Micro Cap ($1M-$10M)"
        else:
            market_cap_category = "Nano Cap (<$1M)"
        
        token = {
            "id": token_id,
            "name": name,
            "symbol": symbol,
            "market_cap": market_cap,
            "market_cap_category": market_cap_category,
            "price": price,
            "volume_24h": volume_24h,
            "price_change_24h": price_change_24h,
            "price_change_7d": price_change_7d,
            "last_updated": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
            "image": f"https://via.placeholder.com/100/FFDD00/000000?text={symbol}",
            "is_ai_token": True,
            "ai_category": np.random.choice([
                "Large Language Models", 
                "Computer Vision", 
                "AI Infrastructure", 
                "AI Data", 
                "AI Agents",
                "AI Compute",
                "Generative Models"
            ]),
            "launch_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime("%Y-%m-%d")
        }
        
        tokens.append(token)
    
    # Fill in the rest with generated names if needed
    for i in range(len(tokens), n):
        # Generate unique name
        while True:
            if np.random.random() < 0.2:
                # Three-word name (less common)
                mid_word = np.random.choice(ai_prefixes) if np.random.random() < 0.5 else np.random.choice(ai_suffixes)
                name = f"{np.random.choice(ai_prefixes)}{mid_word}{np.random.choice(ai_suffixes)}"
            elif np.random.random() < 0.7:
                # Two-word name (common)
                name = f"{np.random.choice(ai_prefixes)}{np.random.choice(ai_suffixes)}"
            else:
                # Single word name (less common)
                name = np.random.choice(ai_prefixes + ai_suffixes)
                
            if name not in used_names:
                used_names.add(name)
                break
        
        # Generate symbol (usually 3-4 letters)
        symbol = ''.join([c for c in name if c.isupper()][:4])
        if not symbol or symbol in used_symbols:
            # If no uppercase letters or collision, create a symbol from first letters
            words = [c for c in name if c[0].isupper()] if any(c[0].isupper() for c in name) else name
            if isinstance(words, str):
                symbol = words[:min(4, len(words))].upper()
            else:
                symbol = ''.join([word[0] for word in words])[:4].upper()
        
        if symbol in used_symbols:
            # If still a collision, add a number
            symbol = symbol[:3] + str(random.randint(1, 9))
            
        used_symbols.add(symbol)
        
        # Market cap tiers for remaining tokens - mostly small and micro caps
        tier = i % 5  # 0=small, 1-2=micro, 3-4=nano
        
        if tier == 0:  # Small cap
            market_cap = np.random.lognormal(mean=17.5, sigma=0.5)  # $10M-$100M range
            price = np.random.lognormal(mean=-1, sigma=1)
        elif tier <= 2:  # Micro cap
            market_cap = np.random.lognormal(mean=15.5, sigma=0.5)  # $1M-$10M range
            price = np.random.lognormal(mean=-2, sigma=1.5)
        else:  # Nano cap
            market_cap = np.random.lognormal(mean=13.5, sigma=0.7)  # <$1M range
            price = np.random.lognormal(mean=-3, sigma=2)
        
        # Smaller caps typically have lower volumes
        volume_factor = np.random.uniform(0.005, 0.1) 
        volume_24h = market_cap * volume_factor
        
        # Higher volatility for smaller caps
        price_change_24h = np.random.normal(0, 8 + (4-tier)*2)
        price_change_7d = np.random.normal(price_change_24h/2, 15 + (4-tier)*3)
        
        # Market sentiment more extreme for smaller caps
        market_sentiment = np.random.choice([-1, 1], p=[0.4, 0.6])  # 60% bullish
        if market_sentiment > 0:
            price_change_24h = abs(price_change_24h) * np.random.uniform(0.9, 1.5)
            price_change_7d = abs(price_change_7d) * np.random.uniform(0.9, 1.7)
        else:
            price_change_24h = -abs(price_change_24h) * np.random.uniform(0.9, 1.5)
            price_change_7d = -abs(price_change_7d) * np.random.uniform(0.9, 1.7)
        
        # Token ID for API calls
        token_id = name.lower().replace(" ", "-").replace(".", "")
        
        # Determine market cap category
        if market_cap >= 1_000_000_000:
            market_cap_category = "Large Cap (>$1B)"
        elif market_cap >= 100_000_000:
            market_cap_category = "Mid Cap ($100M-$1B)"
        elif market_cap >= 10_000_000:
            market_cap_category = "Small Cap ($10M-$100M)"
        elif market_cap >= 1_000_000:
            market_cap_category = "Micro Cap ($1M-$10M)"
        else:
            market_cap_category = "Nano Cap (<$1M)"
        
        token = {
            "id": token_id,
            "name": name,
            "symbol": symbol,
            "market_cap": market_cap,
            "market_cap_category": market_cap_category,
            "price": price,
            "volume_24h": volume_24h,
            "price_change_24h": price_change_24h,
            "price_change_7d": price_change_7d,
            "last_updated": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
            "image": f"https://via.placeholder.com/100/FFDD00/000000?text={symbol}",
            "is_ai_token": True,
            "ai_category": np.random.choice([
                "Large Language Models", 
                "Computer Vision", 
                "AI Infrastructure", 
                "AI Data", 
                "AI Agents",
                "AI Compute",
                "Generative Models"
            ]),
            "launch_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime("%Y-%m-%d")
        }
        
        tokens.append(token)
    
    # Convert to DataFrame
    df = pd.DataFrame(tokens)
    return df

def generate_historical_data(days=30, intervals_per_day=24):
    """Generate realistic price history data with patterns"""
    np.random.seed(42)  # For reproducible results
    
    # Create a more interesting price series with trends, cycles and volatility clusters
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, periods=days*intervals_per_day)
    
    # Base parameters
    initial_price = np.random.uniform(1.0, 20.0)
    
    # Time components
    t = np.linspace(0, days, len(date_range))
    
    # Long-term trend - slight uptrend
    trend_direction = np.random.choice([-1, 1], p=[0.3, 0.7])  # 70% bullish
    trend_strength = np.random.uniform(0.001, 0.005) * trend_direction
    trend = trend_strength * t
    
    # Market cycles - medium term oscillations
    cycle_period = np.random.uniform(7, 14)  # 1-2 week cycles
    cycle_amplitude = np.random.uniform(0.1, 0.3)
    market_cycle = cycle_amplitude * np.sin(2 * np.pi * t / cycle_period)
    
    # Short term oscillations - daily/intraday patterns
    short_cycle = 0.05 * np.sin(2 * np.pi * t) + 0.03 * np.cos(4 * np.pi * t)
    
    # Volatility clustering - periods of high/low volatility
    volatility_base = np.random.uniform(0.01, 0.04)
    volatility_cycle = np.random.uniform(10, 20)  # Length of volatility cycle
    volatility = volatility_base * (1 + 0.5 * np.sin(2 * np.pi * t / volatility_cycle))
    
    # Market events - sudden movements
    num_events = int(days / 10) + 1  # Approximately one event every 10 days
    event_locations = np.random.choice(range(len(date_range)), size=num_events, replace=False)
    event_impact = np.zeros(len(date_range))
    
    for loc in event_locations:
        # Event magnitude - positive or negative shock
        magnitude = np.random.uniform(-0.15, 0.15)
        
        # Event duration - how long the effect lasts
        duration = int(np.random.uniform(1, 3) * intervals_per_day)
        
        # Apply the event with decay
        for i in range(min(duration, len(date_range) - loc)):
            decay = 1 - (i / duration)
            if loc + i < len(event_impact):
                event_impact[loc + i] += magnitude * decay
    
    # Generate price series with all components
    returns = np.random.normal(0, volatility, size=len(date_range))
    noise_component = np.cumsum(returns)  # Random walk component
    normalized_noise = noise_component / np.max(np.abs(noise_component)) * 0.3  # Scale noise
    
    # Combine all components
    price_components = trend + market_cycle + short_cycle + normalized_noise + event_impact
    price_series = initial_price * np.exp(price_components)  # Exponential to ensure positive prices
    
    # Make sure the price never goes too close to zero
    price_series = np.maximum(0.01, price_series)
    
    # Volume often correlates with price volatility and has intraday patterns
    volume_base = initial_price * np.random.uniform(1e6, 1e8)  # Base volume scaled to price
    volume_daily_pattern = 0.5 + 0.5 * np.sin(np.pi * (t * intervals_per_day % intervals_per_day) / intervals_per_day)
    volume_volatility = 1 + 5 * np.abs(np.diff(price_series, prepend=price_series[0]))  # Higher volume on big moves
    
    volume_series = volume_base * volume_daily_pattern * volume_volatility
    
    # Market cap calculation with gradually increasing supply
    initial_supply = np.random.uniform(1e7, 1e9)
    supply_growth = np.random.uniform(0, 0.0001)  # Daily supply growth rate
    supply_series = initial_supply * (1 + supply_growth) ** t
    
    market_cap_series = price_series * supply_series
    
    # Create the DataFrame with additional columns for analysis
    data = {
        "timestamp": [int(dt.timestamp() * 1000) for dt in date_range],
        "date": date_range,
        "price": price_series,
        "market_cap": market_cap_series,
        "volume": volume_series,
        "supply": supply_series,
        "volatility": volatility,
        # Technical indicators
        "sma_7": pd.Series(price_series).rolling(7).mean().values,
        "sma_30": pd.Series(price_series).rolling(30).mean().values,
        "price_change_pct": pd.Series(price_series).pct_change().values * 100,
    }
    
    df = pd.DataFrame(data)
    
    # Calculate additional technical indicators
    df["rsi_14"] = calculate_rsi(df["price"], 14)
    df["bollinger_upper"], df["bollinger_lower"] = calculate_bollinger_bands(df["price"], 20)
    
    # Add a column identifying notable market events for annotations
    df["is_notable_event"] = False
    for loc in event_locations:
        if loc < len(df):
            df.loc[loc, "is_notable_event"] = True
            df.loc[loc, "event_description"] = np.random.choice([
                "Partnership Announcement", "Token Burn", "Exchange Listing", 
                "Protocol Upgrade", "Security Incident", "Major Investment",
                "Regulatory News", "Market Trend Change", "New Product Launch"
            ])
    
    return df

def calculate_rsi(prices, window=14):
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = delta.mask(delta < 0, 0)
    loss = -delta.mask(delta > 0, 0)
    
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, lower_band

def generate_token_details():
    """Generate comprehensive token information with realistic detail"""
    np.random.seed(int(datetime.now().timestamp() % 1000))  # Semi-random seed
    
    token_names = ["Neural Network", "DeepBrain Chain", "SingularityNET", "Cortex AI", 
                "Bittensor", "Fetch.ai", "Ocean Protocol", "The Graph", "Numeraire", 
                "Oasis Network", "Akash Network", "Render Token", "Phala Network"]
    
    token_name = np.random.choice(token_names)
    token_symbol = ''.join([c[0] for c in token_name.split() if c not in ["The", "AI", "Protocol", "Network", "Token", "Chain"]]).upper()
    
    # Ensure symbol is at least 2 characters
    if len(token_symbol) < 2:
        token_symbol = token_name[:3].upper()
    
    # Use token name for ID
    token_id = token_name.lower().replace(" ", "-").replace(".", "")
    
    # Detailed descriptions based on AI technology focus
    descriptions = {
        "Neural Network": "Neural Network is pioneering decentralized artificial intelligence with a focus on high-performance neural networks. The protocol enables smart contracts to utilize sophisticated machine learning algorithms for complex decision-making, pattern recognition, and predictive analytics. By combining neural networks with blockchain technology, NNW creates a new class of decentralized applications that continuously learn and adapt from on-chain data.",
        
        "DeepBrain Chain": "DeepBrain Chain is a decentralized neural network computing platform that provides high-performance computing power for AI applications. Through blockchain technology, DBC connects distributed computing resources worldwide, offering cost-effective AI training services while ensuring data privacy and security. The platform allows AI developers to access massive computing resources at a fraction of traditional cloud costs.",
        
        "SingularityNET": "SingularityNET is building the world's first decentralized marketplace for AI algorithms and services. The platform connects AI developers with businesses and consumers, allowing anyone to create, share, and monetize AI services at scale. With a focus on creating beneficial general intelligence, SingularityNET aims to ensure that AI remains open, accessible, and aligned with human values.",
        
        "Cortex AI": "Cortex AI is developing an on-chain AI computing system that allows smart contracts to incorporate machine learning capabilities. By enabling AI models to execute directly on the blockchain, CTXC makes advanced analytics and learning algorithms available to decentralized applications. This breakthrough technology enables autonomous decision-making in smart contracts based on real-world data and sophisticated inference processes.",
        
        "Bittensor": "Bittensor is creating a decentralized machine learning network where AI models can be trained collaboratively while maintaining data privacy. The protocol incentivizes high-quality machine learning contributions through a consensus mechanism that rewards valuable intelligence. By creating a permissionless marketplace for intelligence, TAO allows AI capabilities to be shared, improved, and properly valued across the network.",
        
        "Fetch.ai": "Fetch.ai is building an open-access, tokenized, decentralized machine learning network to enable smart infrastructure. Through autonomous economic agents that can observe, learn, and take actions, FET creates an environment where digital entities can perform useful economic work on behalf of individuals, businesses, and organizations. This network of AI agents can solve complex coordination problems through collective intelligence.",
        
        "Ocean Protocol": "Ocean Protocol enables data sharing while preserving privacy and control, unlocking the value of data for AI applications. The platform allows data to be shared and sold securely while maintaining ownership and privacy, creating a decentralized data marketplace for the AI economy. By connecting data providers with data consumers, OCEAN facilitates the development of data-driven AI solutions across industries.",
        
        "The Graph": "The Graph indexes blockchain data to enable efficient querying and data retrieval for decentralized applications. By creating a decentralized protocol for indexing and querying blockchain data, GRT provides the infrastructure necessary for sophisticated data analysis and AI applications in the blockchain space. This indexing layer makes blockchain data accessible and usable for complex analytical processes.",
        
        "Numeraire": "Numeraire is a cryptographic token used by data scientists in the Numerai hedge fund tournament to stake predictions in machine learning competitions. By incentivizing data scientists to build accurate financial prediction models, NMR creates a collaborative approach to building investment strategies. This tokenized data science competition harnesses collective intelligence to create sophisticated market models.",
        
        "Oasis Network": "Oasis Network is a privacy-first blockchain platform designed for open finance and a responsible data economy. With its privacy-preserving technology, ROSE enables secure computation and confidential smart contracts, making it ideal for sensitive AI applications that require data privacy. The platform's unique architecture separates consensus from execution, enhancing scalability and versatility.",
        
        "Akash Network": "Akash Network provides a decentralized cloud computing marketplace for deploying AI applications. By connecting users who need computing resources with providers who have excess capacity, AKT creates an efficient marketplace for cloud resources. This decentralized cloud platform significantly reduces the cost of training and deploying AI models compared to traditional cloud providers.",
        
        "Render Token": "Render Token is creating a distributed GPU rendering network for 3D graphics, AI rendering, and deep learning. The platform connects users who need GPU computing power with those who have idle resources, creating a more efficient rendering ecosystem. By leveraging blockchain technology, RNDR enables efficient distribution and monetization of GPU computing for advanced AI visualization applications.",
        
        "Phala Network": "Phala Network provides confidential smart contracts powered by Trusted Execution Environments, enabling privacy-preserving computation for AI applications. Through its unique architecture, PHA allows sensitive data to be processed securely without exposure, even to node operators. This confidential computing infrastructure is essential for AI applications that require both privacy and trustless execution."
    }
    
    # Social metrics - realistic distributions
    followers_base = np.random.lognormal(mean=9, sigma=1.5)  # Centered around 10k followers
    twitter_followers = int(followers_base * np.random.uniform(0.8, 1.5))
    reddit_subscribers = int(followers_base * np.random.uniform(0.3, 1.0))
    telegram_users = int(followers_base * np.random.uniform(0.5, 2.0))
    
    # Financial data - realistic relationships
    price = np.random.lognormal(mean=0, sigma=2)  # Wide range of possible prices
    circulating_supply = np.random.uniform(50_000_000, 1_000_000_000)
    market_cap = price * circulating_supply
    
    # Volume as percentage of market cap (realistic range)
    volume_factor = np.random.uniform(0.02, 0.2)
    volume = market_cap * volume_factor
    
    # Price changes - correlated with some randomness
    price_change_24h = np.random.normal(0, 5)
    direction_persistence = np.random.uniform(0.5, 0.8)  # How much 7d change follows 24h trend
    price_change_7d = price_change_24h * direction_persistence + np.random.normal(0, 8) * (1-direction_persistence)
    price_change_30d = price_change_7d * direction_persistence + np.random.normal(0, 15) * (1-direction_persistence)
    
    # Token economics - realistic relationships
    total_supply = circulating_supply * np.random.uniform(1.2, 2.5)
    max_supply = None if np.random.random() < 0.3 else total_supply * np.random.uniform(1, 1.5)
    
    token_data = {
        "id": token_id,
        "symbol": token_symbol,
        "name": token_name,
        "description": {
            "en": descriptions.get(token_name, "A decentralized AI protocol leveraging blockchain technology to create a new paradigm for machine learning applications.")
        },
        "links": {
            "homepage": [f"https://{token_id.replace('-', '.')}.io"],
            "blockchain_site": [
                "https://etherscan.io/token/0x" + ''.join(random.choices('0123456789abcdef', k=40)),
                "https://bscscan.com/token/0x" + ''.join(random.choices('0123456789abcdef', k=40))
            ],
            "twitter_screen_name": token_name.replace(" ", ""),
            "telegram_channel_identifier": f"{token_name.replace(' ', '')}Official",
            "subreddit_url": f"https://reddit.com/r/{token_name.replace(' ', '')}",
            "repos_url": {
                "github": [f"https://github.com/{token_name.replace(' ', '')}"]
            }
        },
        "image": {
            "thumb": f"https://via.placeholder.com/64/FFDD00/000000?text={token_symbol}",
            "small": f"https://via.placeholder.com/128/FFDD00/000000?text={token_symbol}",
            "large": f"https://via.placeholder.com/200/FFDD00/000000?text={token_symbol}"
        },
        "market_data": {
            "current_price": {"usd": price},
            "market_cap": {"usd": market_cap},
            "total_volume": {"usd": volume},
            "price_change_percentage_24h": price_change_24h,
            "price_change_percentage_7d": price_change_7d,
            "price_change_percentage_30d": price_change_30d,
            "market_cap_rank": int(np.random.uniform(30, 500)),
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
            "max_supply": max_supply
        },
        "community_data": {
            "twitter_followers": twitter_followers,
            "reddit_subscribers": reddit_subscribers,
            "telegram_channel_user_count": telegram_users,
            "github_contributors": int(np.random.lognormal(mean=2.5, sigma=0.7)),
            "github_stars": int(np.random.lognormal(mean=6, sigma=1.2))
        },
        "developer_activity": {
            "commits_last_30_days": int(np.random.lognormal(mean=4, sigma=0.8)),
            "code_additions_deletions_4_weeks": {
                "additions": int(np.random.lognormal(mean=7, sigma=1.0)),
                "deletions": int(np.random.lognormal(mean=6, sigma=0.9))
            }
        },
        "ai_metrics": {
            "technology_focus": np.random.choice([
                "Natural Language Processing",
                "Computer Vision",
                "Reinforcement Learning",
                "AI Infrastructure",
                "Generative Models",
                "Federated Learning",
                "AI Marketplaces",
                "Data Ownership",
                "Autonomous Agents"
            ], size=2, replace=False).tolist(),
            "ai_applications": np.random.choice([
                "Financial Services",
                "Healthcare",
                "Supply Chain",
                "Content Creation",
                "Gaming",
                "Social Media",
                "IoT",
                "Cybersecurity",
                "Climate Tech"
            ], size=3, replace=False).tolist(),
            "computational_efficiency": np.random.uniform(60, 99),
            "decentralization_score": np.random.uniform(50, 95)
        },
        "launch_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d"),
        "last_updated": datetime.now().isoformat()
    }
    
    return token_data