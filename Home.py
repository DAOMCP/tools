import streamlit as st
from utils.data_fetcher import CoinGeckoAPI
from utils.data_processor import DataProcessor
from components.animations import render_data_cluster, render_ai_token_visualization
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configure the main page
st.set_page_config(
    page_title="M100D - AI Analytics Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styles for black and gold theme
st.markdown("""
<style>
    /* Main styles */
    .main-header {
        color: #FFD700 !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    .sub-header {
        color: #A0A0A0;
        font-size: 1.5rem !important;
        margin-top: 0 !important;
        letter-spacing: 1px;
    }
    
    .gold-header {
        color: #FFD700 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Section styling */
    .section-container {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 215, 0, 0.1);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Feature boxes */
    .feature-box {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 20px;
        height: 100%;
        border-top: 3px solid #FFD700;
        transition: transform 0.2s;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    .feature-icon {
        font-size: 2rem;
        color: #FFD700;
        margin-bottom: 15px;
    }
    
    /* Card styling */
    .page-link-card {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(255, 215, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .page-link-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    
    /* Better button styling */
    .gold-button {
        background-color: #1A1A1A !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin-top: auto !important;
        text-align: center !important;
    }
    
    .gold-button:hover {
        background-color: #FFD700 !important;
        color: #0A0A0A !important;
    }
    
    /* Hero area styling */
    .hero-content {
        position: relative;
        z-index: 1;
        padding: 40px 20px;
    }
    
    /* Background effect */
    .bg-pattern {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 10% 20%, rgba(255, 215, 0, 0.05) 0%, transparent 30%),
            radial-gradient(circle at 90% 50%, rgba(255, 215, 0, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 40% 80%, rgba(255, 215, 0, 0.05) 0%, transparent 30%);
        z-index: -1;
    }
    
    /* Stats styling */
    .stat-item {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #1A1A1A;
        border: 1px solid rgba(255, 215, 0, 0.1);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 5px;
    }
    
    .stat-label {
        color: #A0A0A0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

def render_home():
    # Hero section with background effect
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="hero-content"><div class="bg-pattern"></div>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">M<span style="color:#A0A0A0;">100</span>D</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">AI Analytics Platform</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <p style="font-size:1.1rem; margin:20px 0; line-height:1.6;">
        Welcome to M100D, your comprehensive analytics hub for AI tokens and agents. 
        Explore market trends, track performance, and gain insights into the rapidly evolving 
        world of artificial intelligence technology and investments.
        </p>
        """, unsafe_allow_html=True)
        
        # Quick navigation buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            st.markdown('<a href="/Token_Explorer" target="_self" class="gold-button" style="display:block; text-decoration:none;">Token Explorer</a>', unsafe_allow_html=True)
        with col_btn2:
            st.markdown('<a href="/Market_Analysis" target="_self" class="gold-button" style="display:block; text-decoration:none;">Market Analysis</a>', unsafe_allow_html=True)
        with col_btn3:
            st.markdown('<a href="/AI_Agents" target="_self" class="gold-button" style="display:block; text-decoration:none;">AI Agents</a>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Dynamic visualization
        render_ai_token_visualization()
    
    # Market Overview section with key metrics
    st.markdown('<h2 class="gold-header">Market Snapshot</h2>', unsafe_allow_html=True)
    
    # Initialize API and fetch data
    api = CoinGeckoAPI()
    processor = DataProcessor()
    
    with st.spinner("Loading market data..."):
        df = api.get_ai_related_tokens()
    
    if not df.empty:
        # Calculate market stats for key metrics
        market_stats = processor.calculate_market_stats(df)
        
        # Display key metrics in a nice row of stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f"""
                <div class="stat-item">
                    <div class="stat-value">{market_stats.get('total_tokens', 0)}</div>
                    <div class="stat-label">AI Tokens Tracked</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            total_mcap = market_stats.get('total_market_cap', 0)
            formatted_mcap = processor.format_number(total_mcap)
            st.markdown(
                f"""
                <div class="stat-item">
                    <div class="stat-value">${formatted_mcap}</div>
                    <div class="stat-label">Total Market Cap</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            avg_change = market_stats.get('avg_24h_change', 0)
            color = "#00FF00" if avg_change >= 0 else "#FF3D71"
            st.markdown(
                f"""
                <div class="stat-item">
                    <div class="stat-value" style="color:{color};">{avg_change:.2f}%</div>
                    <div class="stat-label">Avg 24h Change</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col4:
            total_vol = market_stats.get('total_volume', 0)
            formatted_vol = processor.format_number(total_vol)
            st.markdown(
                f"""
                <div class="stat-item">
                    <div class="stat-value">${formatted_vol}</div>
                    <div class="stat-label">24h Volume</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Add a performant market chart
        st.markdown('<h2 class="gold-header">Top Performers</h2>', unsafe_allow_html=True)
        
        # Get top performers (gainers and losers)
        gainers, losers = processor.get_top_gainers_losers(df, n=5)
        
        # Create a combined dataframe of just top and bottom 5
        top_performers = pd.concat([gainers, losers])
        
        # Create a horizontal bar chart of price changes
        fig = go.Figure()
        
        # Add bars for gainers with gold color
        fig.add_trace(go.Bar(
            y=gainers['name'],
            x=gainers['price_change_24h'],
            orientation='h',
            marker=dict(
                color='rgba(255, 215, 0, 0.8)',
                line=dict(color='rgba(255, 215, 0, 1.0)', width=1)
            ),
            name='Gainers'
        ))
        
        # Add bars for losers with red color
        fig.add_trace(go.Bar(
            y=losers['name'],
            x=losers['price_change_24h'],
            orientation='h',
            marker=dict(
                color='rgba(255, 61, 113, 0.8)',
                line=dict(color='rgba(255, 61, 113, 1.0)', width=1)
            ),
            name='Losers'
        ))
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            title="Top Gainers and Losers (24h)",
            xaxis_title="Price Change (%)",
            yaxis_title="Token",
            height=500,
            barmode='relative',
            bargap=0.15,
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
                zerolinecolor='rgba(255, 215, 0, 0.5)',
                zerolinewidth=1
            ),
            yaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
            ),
            title_font=dict(size=20, color='#FFD700'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Unable to fetch market data. Check your connection or try again later.")
    
    # Main Pages navigation section
    st.markdown('<h2 class="gold-header">Explore the Platform</h2>', unsafe_allow_html=True)
    
    # Create 2x3 grid for page links
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="page-link-card">
                <h3 style="color: #FFD700;">AI Majors</h3>
                <p style="flex-grow: 1;">Browse and filter AI tokens by market cap, price, and performance. Get detailed information on major AI tokens and their key metrics.</p>
                <div style="font-size: 1.5rem; color: #FFD700; margin: 15px 0;">💰</div>
                <a href="/AI_Majors" target="_self" class="gold-button" style="display:block; text-decoration:none;">Explore Majors</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="page-link-card">
                <h3 style="color: #00FF9E;">New AI Launch</h3>
                <p style="flex-grow: 1;">Discover newly launched AI tokens with market caps under 70M. Analyze early-stage opportunities and track emerging AI technologies.</p>
                <div style="font-size: 1.5rem; color: #00FF9E; margin: 15px 0;">🚀</div>
                <a href="/New_AI_Launch" target="_self" class="gold-button" style="display:block; text-decoration:none; color: #00FF9E !important; border-color: #00FF9E !important;">Discover New Launches</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            """
            <div class="page-link-card">
                <h3 style="color: #FFD700;">Market Analysis</h3>
                <p style="flex-grow: 1;">Dive into comprehensive market analysis with interactive charts and visualizations. Track market trends, distribution, and performance metrics.</p>
                <div style="font-size: 1.5rem; color: #FFD700; margin: 15px 0;">📊</div>
                <a href="/Market_Analysis" target="_self" class="gold-button" style="display:block; text-decoration:none;">Analyze Market</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(
            """
            <div class="page-link-card">
                <h3 style="color: #FFD700;">AI Agents</h3>
                <p style="flex-grow: 1;">Explore the world of AI agents and their capabilities. Track popularity trends, categories, and the evolving AI agent ecosystem.</p>
                <div style="font-size: 1.5rem; color: #FFD700; margin: 15px 0;">🤖</div>
                <a href="/AI_Agents" target="_self" class="gold-button" style="display:block; text-decoration:none;">Discover Agents</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col5:
        st.markdown(
            """
            <div class="page-link-card">
                <h3 style="color: #FFD700;">News Analysis</h3>
                <p style="flex-grow: 1;">Track AI crypto news sentiment and trending topics. Analyze media coverage, market narratives, and token mentions across the ecosystem.</p>
                <div style="font-size: 1.5rem; color: #FFD700; margin: 15px 0;">📰</div>
                <a href="/News_Analysis" target="_self" class="gold-button" style="display:block; text-decoration:none;">Analyze News</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col6:
        st.markdown(
            """
            <div class="page-link-card" style="background: linear-gradient(135deg, rgba(26, 26, 26, 0.8) 0%, rgba(40, 40, 40, 0.8) 100%);">
                <h3 style="color: #FFD700;">Coming Soon</h3>
                <p style="flex-grow: 1;">More analytics features are being developed to provide deeper insights into the AI token ecosystem. Stay tuned for future updates!</p>
                <div style="font-size: 1.5rem; color: #FFD700; margin: 15px 0;">⏳</div>
                <div class="gold-button" style="display:block; text-decoration:none; opacity: 0.7; cursor: not-allowed;">Coming Soon</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Features section
    st.markdown('<h2 class="gold-header">Platform Features</h2>', unsafe_allow_html=True)
    
    # Create feature boxes
    features = [
        {
            "icon": "✨",
            "title": "Real-time Data",
            "description": "Access up-to-date market data and metrics from reliable cryptocurrency and AI agent sources."
        },
        {
            "icon": "📈",
            "title": "Interactive Charts",
            "description": "Explore the market with interactive visualizations designed for clear insights and analysis."
        },
        {
            "icon": "🔍",
            "title": "Detailed Analytics",
            "description": "Dive deep into token and agent metrics with comprehensive analytical tools."
        },
        {
            "icon": "📱",
            "title": "Multi-device Access",
            "description": "Access the platform from any device with a responsive design that adapts to your screen."
        },
        {
            "icon": "🔔",
            "title": "Custom Filters",
            "description": "Filter and sort data according to your specific interests and requirements."
        },
        {
            "icon": "🌐",
            "title": "Ecosystem Insights",
            "description": "Gain valuable insights into the entire AI token and agent ecosystem in one place."
        }
    ]
    
    # Display features in a 3x2 grid
    rows = [features[i:i+3] for i in range(0, len(features), 3)]
    
    for row in rows:
        cols = st.columns(3)
        for i, feature in enumerate(row):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="feature-box">
                        <div class="feature-icon">{feature["icon"]}</div>
                        <h3 style="color: #FFD700;">{feature["title"]}</h3>
                        <p>{feature["description"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # AI Token Universe visualization
    st.markdown('<h2 class="gold-header">AI Token Universe</h2>', unsafe_allow_html=True)
    
    # Enhanced AI Token Visualization with explanation text
    st.markdown("""
    <div style="background-color: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <p style="margin-bottom: 10px;">The AI Token Universe represents the evolving ecosystem of AI-related cryptocurrency tokens. 
        The visualization illustrates relationships, relative market sizes, and positioning within the broader AI technology landscape.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendered with custom styling to ensure it appears properly
    st.markdown("""
    <style>
    .token-cosmos {
        position: relative;
        height: 300px;
        background: linear-gradient(180deg, rgba(10, 10, 10, 1) 0%, rgba(26, 26, 26, 0.5) 100%);
        border-radius: 10px;
        overflow: hidden;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .token {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,215,0,0.4) 70%, transparent 100%);
        transform-origin: center center;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #0A0A0A;
        font-size: 0.7rem;
    }
    
    .token-lg {
        background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,215,0,0.6) 70%, transparent 100%);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        animation: pulse-size 4s infinite ease-in-out;
        z-index: 10;
    }
    
    .token-sm {
        z-index: 5;
    }
    
    @keyframes orbit {
        0% { transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(var(--orbit-radius)) rotate(-360deg); }
    }
    
    @keyframes orbit-reverse {
        0% { transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg); }
        100% { transform: rotate(-360deg) translateX(var(--orbit-radius)) rotate(360deg); }
    }
    
    @keyframes pulse-size {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .orbit-line {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 1px dashed rgba(255, 215, 0, 0.2);
        border-radius: 50%;
    }
    
    .token-name {
        position: absolute;
        color: #FFD700;
        font-size: 0.7rem;
        white-space: nowrap;
        text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
    }
    </style>
    
    <div class="token-cosmos">
        <!-- Orbit circles -->
        <div class="orbit-line" style="width: 120px; height: 120px;"></div>
        <div class="orbit-line" style="width: 200px; height: 200px;"></div>
        <div class="orbit-line" style="width: 280px; height: 280px;"></div>
        
        <!-- Central node - represents the AI sector -->
        <div class="token token-lg" style="top: 50%; left: 50%; width: 50px; height: 50px; margin-top: -25px; margin-left: -25px;">AI</div>
        
        <!-- Orbiting tokens - major market cap tokens -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 30px; height: 30px; margin-top: -15px; margin-left: -15px; 
                     --orbit-radius: 60px; animation: orbit 20s infinite linear;">FET</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 34px; height: 34px; margin-top: -17px; margin-left: -17px; 
                     --orbit-radius: 100px; animation: orbit-reverse 25s infinite linear;">AGIX</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 24px; height: 24px; margin-top: -12px; margin-left: -12px; 
                     --orbit-radius: 140px; animation: orbit 30s infinite linear;">RNDR</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 22px; height: 22px; margin-top: -11px; margin-left: -11px; 
                     --orbit-radius: 80px; animation: orbit-reverse 18s infinite linear;">OCEAN</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 26px; height: 26px; margin-top: -13px; margin-left: -13px; 
                     --orbit-radius: 120px; animation: orbit 22s infinite linear;">GRT</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 20px; height: 20px; margin-top: -10px; margin-left: -10px; 
                     --orbit-radius: 90px; animation: orbit-reverse 27s infinite linear;">NMR</div>
        
        <!-- Second ring -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 18px; height: 18px; margin-top: -9px; margin-left: -9px; 
                     --orbit-radius: 130px; animation: orbit 24s infinite linear;">ICP</div>
                     
        <div class="token token-sm" style="top: 50%; left: 50%; width: 16px; height: 16px; margin-top: -8px; margin-left: -8px; 
                     --orbit-radius: 120px; animation: orbit-reverse 28s infinite linear;">CHR</div>
                     
        <!-- Outer ring - smaller tokens -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 14px; height: 14px; margin-top: -7px; margin-left: -7px; 
                     --orbit-radius: 140px; animation: orbit 32s infinite linear;">ALI</div>
                     
        <div class="token token-sm" style="top: 50%; left: 50%; width: 16px; height: 16px; margin-top: -8px; margin-left: -8px; 
                     --orbit-radius: 110px; animation: orbit-reverse 29s infinite linear;">CQT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255, 215, 0, 0.1);">
            <p>© 2025 M100D - AI Analytics Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    render_home()