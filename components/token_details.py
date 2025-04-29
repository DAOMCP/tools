import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_fetcher import CoinGeckoAPI
from utils.data_processor import DataProcessor

def render_token_details(token_id):
    """Render detailed view for a specific token"""
    if not token_id:
        st.info("Please select a token to view its details")
        if st.button("Back to Dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()
        return
    
    # Initialize API and fetch token details
    api = CoinGeckoAPI()
    
    with st.spinner(f"Loading token details..."):
        token_details = api.get_token_details(token_id)
        
        # Fetch historical data for the selected time period
        days = st.session_state.filter_settings.get("days", 7)
        historical_data = api.get_token_historical_data(token_id, days=days)
    
    if not token_details:
        st.error("Failed to load token details. Please try again.")
        if st.button("Back to Dashboard"):
            st.session_state.view = "dashboard"
            st.rerun()
        return
    
    # Back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back"):
            st.session_state.view = "dashboard"
            st.rerun()
    
    # Render token header
    render_token_header(token_details)
    
    # Price chart and stats
    render_price_chart(historical_data, token_details)
    
    # Additional information
    render_token_information(token_details)
    
    # Community and social info
    render_social_info(token_details)

def render_token_header(token_details):
    """Render the token header with basic information"""
    name = token_details.get("name", "Unknown Token")
    symbol = token_details.get("symbol", "").upper()
    
    # Get current price and market data
    market_data = token_details.get("market_data", {})
    current_price = market_data.get("current_price", {}).get("usd", 0)
    price_change_24h = market_data.get("price_change_percentage_24h", 0)
    
    # Header with token name and symbol
    st.markdown(f"# {name} ({symbol})")
    
    # Price information
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"${current_price:,.6f}",
            delta=f"{price_change_24h:.2f}%" if price_change_24h else None,
            delta_color="normal"
        )
    
    with col2:
        market_cap = market_data.get("market_cap", {}).get("usd", 0)
        st.metric(
            label="Market Cap",
            value=DataProcessor.format_number(market_cap),
            delta=None
        )
    
    with col3:
        # Get ATH (All-Time High)
        ath = market_data.get("ath", {}).get("usd", 0)
        ath_change = market_data.get("ath_change_percentage", {}).get("usd", 0)
        ath_date = market_data.get("ath_date", {}).get("usd", "")
        
        if ath:
            ath_date_formatted = "Unknown"
            if ath_date:
                try:
                    ath_date_formatted = pd.to_datetime(ath_date).strftime('%d %b %Y')
                except:
                    pass
                    
            st.metric(
                label=f"All-Time High ({ath_date_formatted})",
                value=f"${ath:,.6f}",
                delta=f"{ath_change:.2f}%" if ath_change else None,
                delta_color="normal"
            )

def render_price_chart(historical_data, token_details):
    """Render price and volume charts"""
    st.subheader("Price History")
    
    if historical_data.empty:
        st.info("No historical data available for this token")
        return
    
    # Create tabs for different charts
    tab1, tab2, tab3 = st.tabs(["Price", "Volume", "Market Cap"])
    
    with tab1:
        # Price chart
        fig = go.Figure()
        
        # Add price line
        fig.add_trace(
            go.Scatter(
                x=historical_data['date'],
                y=historical_data['price'],
                mode='lines',
                name='Price',
                line=dict(color='rgb(126, 87, 194)', width=2),
                hovertemplate='<b>%{x|%d %b %Y %H:%M}</b><br>$%{y:.6f}<extra></extra>'
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f"{token_details.get('name', 'Token')} Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_dark",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=50, b=0),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Volume chart
        fig = go.Figure()
        
        # Add volume bars
        fig.add_trace(
            go.Bar(
                x=historical_data['date'],
                y=historical_data['volume'],
                name='Volume',
                marker=dict(color='rgba(126, 87, 194, 0.7)'),
                hovertemplate='<b>%{x|%d %b %Y %H:%M}</b><br>$%{y:,.0f}<extra></extra>'
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f"{token_details.get('name', 'Token')} Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume (USD)",
            template="plotly_dark",
            hovermode="x unified",
            margin=dict(l=0, r=0, t=50, b=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Market cap chart
        fig = go.Figure()
        
        # Add market cap line
        fig.add_trace(
            go.Scatter(
                x=historical_data['date'],
                y=historical_data['market_cap'],
                mode='lines',
                name='Market Cap',
                line=dict(color='rgb(255, 171, 0)', width=2),
                hovertemplate='<b>%{x|%d %b %Y %H:%M}</b><br>$%{y:,.0f}<extra></extra>'
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f"{token_details.get('name', 'Token')} Market Cap History",
            xaxis_title="Date",
            yaxis_title="Market Cap (USD)",
            template="plotly_dark",
            hovermode="x unified",
            margin=dict(l=0, r=0, t=50, b=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_token_information(token_details):
    """Render additional token information"""
    st.subheader("Token Information")
    
    # Split the description and other info into tabs
    tab1, tab2 = st.tabs(["About", "Market Data"])
    
    with tab1:
        # Description
        description = token_details.get("description", {}).get("en", "No description available.")
        if description:
            st.markdown(description)
        else:
            st.info("No description available for this token.")
        
        # Links
        links = token_details.get("links", {})
        if links:
            st.subheader("Official Links")
            
            # Homepage
            homepages = links.get("homepage", [])
            if homepages and homepages[0]:
                st.markdown(f"🏠 [Official Website]({homepages[0]})")
            
            # Explorer
            explorers = links.get("blockchain_site", [])
            if explorers and explorers[0]:
                st.markdown(f"🔍 [Block Explorer]({explorers[0]})")
            
            # Repositories
            repos = links.get("repos_url", {}).get("github", [])
            if repos and repos[0]:
                st.markdown(f"💻 [GitHub Repository]({repos[0]})")
            
            # White paper
            whitepaper = links.get("whitepaper", "")
            if whitepaper:
                st.markdown(f"📄 [Whitepaper]({whitepaper})")
    
    with tab2:
        # Market data
        market_data = token_details.get("market_data", {})
        if not market_data:
            st.info("No market data available for this token.")
            return
        
        # Market cap rank
        market_cap_rank = market_data.get("market_cap_rank", "N/A")
        st.metric("Market Cap Rank", f"#{market_cap_rank}" if market_cap_rank else "N/A")
        
        # Create 3 columns for market stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 24h volume
            volume = market_data.get("total_volume", {}).get("usd", 0)
            st.metric("24h Volume", DataProcessor.format_number(volume))
            
            # Circulating supply
            circ_supply = market_data.get("circulating_supply", 0)
            st.metric("Circulating Supply", f"{circ_supply:,.0f}" if circ_supply else "N/A")
        
        with col2:
            # 24h high/low
            high_24h = market_data.get("high_24h", {}).get("usd", 0)
            low_24h = market_data.get("low_24h", {}).get("usd", 0)
            
            st.metric("24h High", f"${high_24h:,.6f}" if high_24h else "N/A")
            st.metric("24h Low", f"${low_24h:,.6f}" if low_24h else "N/A")
        
        with col3:
            # Total supply
            total_supply = market_data.get("total_supply", 0)
            max_supply = market_data.get("max_supply", 0)
            
            st.metric("Total Supply", f"{total_supply:,.0f}" if total_supply else "N/A")
            st.metric("Max Supply", f"{max_supply:,.0f}" if max_supply else "∞")
        
        # Price change percentages
        st.subheader("Price Change")
        
        changes = {
            "24h": market_data.get("price_change_percentage_24h", 0),
            "7d": market_data.get("price_change_percentage_7d", 0),
            "14d": market_data.get("price_change_percentage_14d", 0),
            "30d": market_data.get("price_change_percentage_30d", 0),
            "60d": market_data.get("price_change_percentage_60d", 0),
            "200d": market_data.get("price_change_percentage_200d", 0),
            "1y": market_data.get("price_change_percentage_1y", 0)
        }
        
        # Filter out None values
        changes = {k: v for k, v in changes.items() if v is not None}
        
        if changes:
            # Create bar chart for price changes
            fig = go.Figure()
            
            fig.add_trace(
                go.Bar(
                    x=list(changes.keys()),
                    y=list(changes.values()),
                    marker=dict(
                        color=['red' if v < 0 else 'green' for v in changes.values()],
                    ),
                    text=[f"{v:.2f}%" for v in changes.values()],
                    textposition='auto',
                    hovertemplate='%{text}<extra></extra>'
                )
            )
            
            fig.update_layout(
                title="Price Change by Time Period",
                xaxis_title="Time Period",
                yaxis_title="Percentage Change",
                template="plotly_dark",
                margin=dict(l=0, r=0, t=50, b=0),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No price change data available.")

def render_social_info(token_details):
    """Render community and social information"""
    st.subheader("Community & Social")
    
    # Get community data
    community_data = token_details.get("community_data", {})
    if not community_data:
        st.info("No community data available for this token.")
        return
    
    # Social media links
    links = token_details.get("links", {})
    
    if links:
        social_links = []
        
        # Twitter
        twitter = links.get("twitter_screen_name", "")
        if twitter:
            social_links.append(f"[Twitter](https://twitter.com/{twitter})")
        
        # Telegram
        telegram = links.get("telegram_channel_identifier", "")
        if telegram:
            social_links.append(f"[Telegram](https://t.me/{telegram})")
        
        # Reddit
        reddit = links.get("subreddit_url", "")
        if reddit:
            social_links.append(f"[Reddit]({reddit})")
        
        # Discord
        discord = links.get("chat_url", "")
        if discord and "discord" in discord:
            social_links.append(f"[Discord]({discord})")
        
        if social_links:
            # Display social links in columns
            cols = st.columns(len(social_links))
            for i, link in enumerate(social_links):
                cols[i].markdown(link, unsafe_allow_html=True)
    
    # Community stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        twitter_followers = community_data.get("twitter_followers", 0)
        st.metric("Twitter Followers", f"{twitter_followers:,}" if twitter_followers else "N/A")
    
    with col2:
        reddit_subscribers = community_data.get("reddit_subscribers", 0)
        st.metric("Reddit Subscribers", f"{reddit_subscribers:,}" if reddit_subscribers else "N/A")
    
    with col3:
        telegram_members = community_data.get("telegram_channel_user_count", 0)
        st.metric("Telegram Members", f"{telegram_members:,}" if telegram_members else "N/A")
