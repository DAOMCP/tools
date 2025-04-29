import trafilatura
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import re

def get_website_text_content(url: str) -> str:
    """
    This function takes a URL and returns the main text content of the website.
    The text content is extracted using trafilatura and is easier to understand
    than raw HTML.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        Extracted text content
    """
    try:
        # Send a request to the website
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text
    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return None

def scrape_ai_crypto_news():
    """
    Scrape news articles about AI and crypto from various sources
    
    This is a simulation of scraping for the demo application
    
    Returns:
        DataFrame with news data
    """
    # This simulates scraping from various news sources
    news_sources = [
        "https://www.coindesk.com/tag/artificial-intelligence/",
        "https://cointelegraph.com/tags/artificial-intelligence",
        "https://decrypt.co/news",
        "https://www.theblock.co/category/ai",
        "https://www.theverge.com/crypto"
    ]
    
    # Generate some realistic news articles
    ai_topics = [
        "GPT Token", "AI Infrastructure", "Machine Learning Network", 
        "Neural Protocol", "Deep Learning Chain", "AI Governance", 
        "LLM Token", "Compute Network", "Intelligent Systems", 
        "AI Data Protocol", "Decentralized Intelligence"
    ]
    
    crypto_topics = [
        "Market Analysis", "DeFi Protocol", "Layer-2", "Web3", "NFT", 
        "Exchange Listing", "Privacy", "Regulation", "Governance", 
        "Protocol Upgrade", "Bridge Technology"
    ]
    
    # Article template generators
    article_templates = [
        "{ai_topic} Partners with {crypto_topic} Platform to Enhance AI Capabilities",
        "New {ai_topic} Token Surges After Announcing {crypto_topic} Integration",
        "{ai_topic} Protocol Releases Roadmap for {crypto_topic} Features",
        "Investors Rally Behind {ai_topic} Following Successful {crypto_topic} Implementation",
        "Researchers Develop Novel {ai_topic} Solution for {crypto_topic} Challenges",
        "{ai_topic} Foundation Secures $25M Funding to Advance {crypto_topic} Development",
        "Leading {crypto_topic} Platform Adopts {ai_topic} for Enhanced Analytics",
        "Major Exchange Lists {ai_topic} Token Following {crypto_topic} Breakthrough",
        "{ai_topic} Whitepaper Reveals Revolutionary Approach to {crypto_topic}",
        "Industry Veterans Launch {ai_topic} Project Focused on {crypto_topic} Solutions"
    ]
    
    # Generate random news data
    now = datetime.now()
    news_data = []
    
    for _ in range(20):  # Generate 20 news articles
        ai_topic = random.choice(ai_topics)
        crypto_topic = random.choice(crypto_topics)
        headline = random.choice(article_templates).format(ai_topic=ai_topic, crypto_topic=crypto_topic)
        
        # Random date within the last 30 days
        days_ago = random.randint(0, 30)
        article_date = now - timedelta(days=days_ago, 
                                      hours=random.randint(0, 23), 
                                      minutes=random.randint(0, 59))
        
        # Sentiment scoring - higher scores for more positive headlines
        sentiment_words = {
            'positive': ['surge', 'rally', 'success', 'advance', 'enhance', 'revolutionary', 'breakthrough'],
            'negative': ['challenge', 'issue', 'problem', 'concern', 'risk', 'decline', 'crash']
        }
        
        # Basic sentiment analysis by keyword matching
        headline_lower = headline.lower()
        sentiment_score = 0
        for word in sentiment_words['positive']:
            if word.lower() in headline_lower:
                sentiment_score += random.uniform(0.1, 0.3)
        for word in sentiment_words['negative']:
            if word.lower() in headline_lower:
                sentiment_score -= random.uniform(0.1, 0.3)
                
        # Add some randomness to sentiment
        sentiment_score += random.uniform(-0.1, 0.1)
        sentiment_score = max(-1.0, min(1.0, sentiment_score))  # Clip to [-1, 1]
        
        # Generate a snippet of the article
        snippet = f"The {ai_topic} project has announced a new development related to {crypto_topic}, "
        snippet += f"which could significantly impact the AI token ecosystem. "
        snippet += f"Industry experts suggest this may lead to increased adoption and utility for AI-focused blockchain projects."
        
        # Extract related tokens from the headline
        related_tokens = []
        if 'GPT' in ai_topic:
            related_tokens.extend(['GPT Finance', 'OpenAI Token'])
        if 'Neural' in ai_topic:
            related_tokens.extend(['Neural Network', 'SingularityNET'])
        if 'Deep' in ai_topic:
            related_tokens.extend(['DeepBrain Chain', 'DeepMind Protocol'])
        if 'Data' in crypto_topic or ai_topic:
            related_tokens.append('Ocean Protocol')
        if 'Learning' in ai_topic:
            related_tokens.append('Fetch.ai')
        if 'Infrastructure' in ai_topic or 'Compute' in ai_topic:
            related_tokens.extend(['Render Token', 'Akash Network'])
            
        # Ensure we have at least one related token
        if not related_tokens:
            related_tokens = ['SingularityNET', 'Fetch.ai', 'Ocean Protocol']
            
        # Keep only up to 3 related tokens
        related_tokens = related_tokens[:min(3, len(related_tokens))]
        
        news_data.append({
            'headline': headline,
            'source': random.choice(news_sources),
            'date': article_date,
            'sentiment': sentiment_score,
            'snippet': snippet,
            'related_tokens': related_tokens,
            'url': f"https://example.com/news/{ai_topic.replace(' ', '-').lower()}-{crypto_topic.replace(' ', '-').lower()}"
        })
    
    # Sort by date, most recent first
    news_df = pd.DataFrame(news_data)
    news_df = news_df.sort_values('date', ascending=False)
    
    return news_df

def analyze_news_sentiment(news_df):
    """
    Analyze news sentiment and create summary statistics
    
    Args:
        news_df: DataFrame of news articles
        
    Returns:
        Dictionary with sentiment analysis results
    """
    if news_df.empty or 'sentiment' not in news_df.columns:
        return {
            'avg_sentiment': 0,
            'positive_news_count': 0,
            'negative_news_count': 0,
            'neutral_news_count': 0,
            'sentiment_by_date': [],
            'trending_tokens': []
        }
        
    # Calculate basic sentiment stats
    avg_sentiment = news_df['sentiment'].mean()
    
    # Count positive/negative/neutral articles
    positive_news = news_df[news_df['sentiment'] > 0.1]
    negative_news = news_df[news_df['sentiment'] < -0.1]
    neutral_news = news_df[(news_df['sentiment'] >= -0.1) & (news_df['sentiment'] <= 0.1)]
    
    # Sentiment trend over time
    news_df['date_day'] = news_df['date'].dt.date
    sentiment_by_date = news_df.groupby('date_day')['sentiment'].mean().reset_index()
    sentiment_by_date = sentiment_by_date.sort_values('date_day')
    
    # Find trending tokens (most frequently mentioned in news)
    token_mentions = {}
    for tokens in news_df['related_tokens']:
        for token in tokens:
            if token in token_mentions:
                token_mentions[token] += 1
            else:
                token_mentions[token] = 1
                
    trending_tokens = [{"token": k, "mentions": v} for k, v in sorted(token_mentions.items(), 
                                                                      key=lambda item: item[1], 
                                                                      reverse=True)]
    
    return {
        'avg_sentiment': avg_sentiment,
        'positive_news_count': len(positive_news),
        'negative_news_count': len(negative_news),
        'neutral_news_count': len(neutral_news),
        'sentiment_by_date': sentiment_by_date.to_dict('records'),
        'trending_tokens': trending_tokens[:5]  # Top 5 trending tokens
    }