import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_processor import DataProcessor
from components.animations import render_animated_metric, render_card
import random

st.set_page_config(
    page_title="M100D - New AI Launch",
    page_icon="🚀",
    layout="wide"
)

# Custom styles for black and gold theme
st.markdown("""
<style>
    /* Custom Gold Accents */
    .gold-header {
        color: #FFD700 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.2);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Chart container styling */
    .chart-container {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-top: 2px solid #FFD700;
        margin-bottom: 20px;
    }
    
    /* Token card styling */
    .token-card {
        background-color: rgba(26, 26, 26, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 3px solid #FFD700;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .token-card:hover {
        background-color: rgba(35, 35, 35, 0.8);
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }
    
    .token-symbol {
        font-size: 0.9rem;
        color: #A0A0A0;
    }
    
    .token-name {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 8px 0;
        color: #FFFFFF;
    }
    
    .token-price {
        color: #FFD700;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    
    .token-mcap {
        color: #D0D0D0;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .token-change {
        font-weight: 500;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 5px;
        font-size: 0.9rem;
    }
    
    .positive {
        background-color: rgba(0, 255, 158, 0.2);
        color: #00FF9E;
    }
    
    .negative {
        background-color: rgba(255, 61, 113, 0.2);
        color: #FF3D71;
    }
    
    .category-badge {
        display: inline-block;
        background-color: rgba(255, 215, 0, 0.1);
        border-radius: 4px;
        padding: 2px 6px;
        margin-right: 6px;
        margin-top: 10px;
        font-size: 0.8rem;
        color: #FFD700;
    }
    
    /* Filters styling */
    .filter-container {
        background-color: rgba(26, 26, 26, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Better button styling */
    .gold-button {
        background-color: #1A1A1A !important;
        color: #FFD700 !important;
        border: 2px solid #FFD700 !important;
        border-radius: 30px !important;
        padding: 8px 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        margin-top: auto !important;
        text-align: center !important;
        font-size: 0.9rem !important;
        display: inline-block !important;
        text-decoration: none !important;
    }
    
    .gold-button:hover {
        background-color: rgba(255, 215, 0, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Table styling */
    [data-testid="stTable"] table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }
    
    [data-testid="stTable"] th {
        background-color: #1A1A1A;
        color: #FFD700 !important;
        font-weight: 600;
        border-bottom: 2px solid #FFD700;
        padding: 10px;
    }
    
    [data-testid="stTable"] td {
        border-bottom: 1px solid rgba(255, 215, 0, 0.1);
        padding: 8px 10px;
    }
</style>
""", unsafe_allow_html=True)

# Generate AI token categories
AI_CATEGORIES = [
    "Large Language Models", "Computer Vision", "Generative AI", "AI Infrastructure", 
    "Robot Process Automation", "Neural Networks", "AI Data Management", "Edge AI",
    "MLOps", "AI Agents", "Federated Learning", "AI Hardware Optimization", 
    "Autonomous Systems", "AI Marketplaces", "AI Governance"
]

def generate_small_cap_tokens(n=80):
    """
    Generate small cap AI tokens (under 70M market cap)
    """
    processor = DataProcessor()
    tokens = []
    now = datetime.now()
    
    # Pre-define some realistic token names and symbols
    ai_token_names = [
        "NeuralNet", "CogniSys", "AIMatrix", "DeepThink", "BrainWave",
        "SentiCore", "Intellicoin", "NeuroCash", "AIGovernance", "CyberNex",
        "QuantumAI", "MindFrame", "CortexAI", "NeuralLabs", "Cognition",
        "DeepMind", "SentiNet", "LogicAI", "BrainTrust", "AIEcosystem",
        "NeuraLink", "CogniCoin", "AIShard", "NexusAI", "VisionCore",
        "DataNex", "CogniNet", "AIHarbor", "NeuralCore", "SentiCoin",
        "QuantumCore", "MindNet", "CortexNet", "NeuralFinance", "CogniData",
        "DeepLearn", "SentiAI", "LogicCore", "BrainChain", "AIFlow",
        "NeuraCore", "CogniVerse", "AINexus", "NexusCode", "VisionAI",
        "DataAI", "CogniScan", "AIDecision", "NeuralTech", "SentiTrust",
        "QuantumMind", "MindScan", "CortexChain", "NeuralVerse", "CogniLearn",
        "DeepScan", "SentiCore", "LogicDecision", "BrainSync", "AIBlock",
        "NeuraFlow", "CogniSync", "AIConnect", "NexusFlow", "VisionTech",
        "DataSync", "CogniFlow", "AIHive", "NeuralHive", "SentiNet",
        "QuantumSync", "MindFlow", "CortexConnect", "NeuralBlock", "CogniHub",
        "DeepSync", "SentiLink", "LogicHub", "BrainNet", "AILearn",
    ]
    
    # Shuffle to get random combinations
    random.shuffle(ai_token_names)
    
    # Generate sample tokens
    for i in range(n):
        name = ai_token_names[i % len(ai_token_names)]
        if i >= len(ai_token_names):
            name = f"{name} {i // len(ai_token_names) + 1}"
            
        # Create token symbol (2-5 chars)
        symbol = ''.join([c for c in name if c.isupper()]) or name[:3].upper()
        if len(symbol) > 5:
            symbol = symbol[:5]
        elif len(symbol) < 2:
            symbol = name[:3].upper()
            
        # Random market cap between 500k and 70M, with more in the lower ranges
        # Use exponential distribution to weight towards lower values
        market_cap = min(70000000, 500000 + np.random.exponential(10000000))
        
        # Decide if token is very new (launched within 30 days)
        is_new = random.random() < 0.7  # 70% chance token is new
        
        # Generate launch date
        if is_new:
            # Last 30 days
            days_ago = random.randint(1, 30)
        else:
            # Last 90 days
            days_ago = random.randint(31, 90)
            
        launch_date = now - timedelta(days=days_ago)
        
        # Random price between $0.00001 and $10
        # Use log distribution to get realistic price ranges
        price = np.exp(random.uniform(np.log(0.00001), np.log(10)))
        
        # Calculate circulating supply based on market cap and price
        circ_supply = market_cap / price
        
        # Random 24h change -20% to +40%, weighted toward positive for new tokens
        if is_new:
            price_change_24h = random.uniform(-15, 50)  # More likely to have positive change
        else:
            price_change_24h = random.uniform(-20, 40)
            
        # Random 7d change, somewhat correlated with 24h change
        base_7d_change = price_change_24h * 1.5
        price_change_7d = max(-50, min(100, base_7d_change + random.uniform(-20, 20)))
        
        # Random volume, correlated with market cap
        volume_factor = random.uniform(0.05, 0.3)  # 5-30% of market cap
        volume_24h = market_cap * volume_factor
        
        # Assign random category from AI categories
        category = random.choice(AI_CATEGORIES)
        
        # Assign market cap category
        if market_cap < 1000000:  # < $1M
            market_cap_category = "Nano Cap (<$1M)"
        elif market_cap < 10000000:  # < $10M
            market_cap_category = "Micro Cap ($1M-$10M)"
        else:  # $10M-$70M
            market_cap_category = "Small Cap ($10M-$70M)"
            
        # Generate a risk score (higher = riskier)
        # Factors: new launch, low market cap, high volatility, low volume relative to mcap
        risk_factors = []
        if days_ago < 10:
            risk_factors.append(3)  # Very new token
        elif days_ago < 30:
            risk_factors.append(2)  # New token
            
        if market_cap < 1000000:
            risk_factors.append(3)  # Very small cap
        elif market_cap < 5000000:
            risk_factors.append(2)  # Small cap
            
        if abs(price_change_24h) > 30:
            risk_factors.append(2)  # High volatility
            
        if volume_24h < market_cap * 0.05:
            risk_factors.append(2)  # Low liquidity
            
        risk_score = min(10, sum(risk_factors) if risk_factors else 1)
        
        # Generate random token descriptions
        descriptions = [
            f"An AI-powered {category.lower()} platform with advanced neural networks",
            f"Decentralized {category.lower()} infrastructure for enterprise applications",
            f"Next-generation {category.lower()} solution with proprietary algorithms",
            f"{category} protocol building tokenized AI systems for developers",
            f"Community-driven {category.lower()} ecosystem focused on innovation",
            f"Cutting-edge {category.lower()} technology for real-time applications",
            f"A {category.lower()} project developing open-source AI tools",
            f"Innovative {category.lower()} framework for data scientists",
            f"{category} token with cross-chain interoperability features",
            f"Scalable {category.lower()} infrastructure for AI model deployment"
        ]
        description = random.choice(descriptions)
        
        # Create token dict
        token = {
            'name': name,
            'symbol': symbol,
            'price': price,
            'market_cap': market_cap,
            'price_change_24h': price_change_24h,
            'price_change_7d': price_change_7d,
            'volume_24h': volume_24h,
            'circulating_supply': circ_supply,
            'launch_date': launch_date,
            'days_since_launch': days_ago,
            'category': category,
            'market_cap_category': market_cap_category,
            'risk_score': risk_score,
            'description': description
        }
        
        tokens.append(token)
    
    # Convert to DataFrame
    df = pd.DataFrame(tokens)
    
    return df

def render_new_ai_launch():
    st.markdown('<h1 class="gold-header">New AI Launch</h1>', unsafe_allow_html=True)
    
    # Introduction text
    st.markdown("""
    <div style="background-color: rgba(255, 215, 0, 0.1); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <p style="margin-bottom: 15px;">This section focuses on newly launched AI tokens with market caps under 70 million USD. 
        These represent emerging opportunities in the AI token ecosystem, but often come with higher volatility and risk.</p>
        <p><strong style="color: #FFD700;">Note:</strong> Always conduct thorough research before investing in smaller-cap tokens.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize data processor
    processor = DataProcessor()
    
    # Generate our small cap AI tokens
    with st.spinner("Loading new AI token data..."):
        df = generate_small_cap_tokens(80)
    
    if df.empty:
        st.error("No data available. Please try again later.")
        return
    
    # Show key metrics about new tokens
    st.markdown('<h2 class="gold-header">New Token Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate some metrics
    total_tokens = len(df)
    avg_token_age = df['days_since_launch'].mean()
    total_mcap = df['market_cap'].sum()
    avg_price_change = df['price_change_24h'].mean()
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_animated_metric("Total New Tokens", f"{total_tokens}", None, color="gold")
    
    with col2:
        render_animated_metric("Avg. Token Age", f"{avg_token_age:.1f} days", None, color="gold")
    
    with col3:
        formatted_mcap = processor.format_number(total_mcap)
        render_animated_metric("Combined Market Cap", f"${formatted_mcap}", None, color="gold")
    
    with col4:
        color = "green" if avg_price_change >= 0 else "red"
        sign = "+" if avg_price_change >= 0 else ""
        render_animated_metric("Avg 24h Change", f"{sign}{avg_price_change:.2f}%", None, color=color)
    
    # Create filter controls
    st.markdown('<h2 class="gold-header">Filters & Analysis</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    # Create filter tabs
    tab1, tab2, tab3 = st.tabs(["Market Cap Distribution", "Recent Launches", "Risk Analysis"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Market cap distribution chart
            fig = px.pie(
                df, 
                names='market_cap_category', 
                title='Distribution by Market Cap',
                color_discrete_sequence=px.colors.sequential.Plasma,
                hole=0.4
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0A0A0A', width=2))
            )
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                title={
                    'text': "Distribution by Market Cap",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Show category breakdown
            st.markdown('<h3 style="color: #FFD700; font-size: 1.2rem;">Category Breakdown</h3>', unsafe_allow_html=True)
            
            category_counts = df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            for i, row in category_counts.iterrows():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>{row['Category']}</div>
                    <div style="color: #FFD700;">{row['Count']}</div>
                </div>
                <div style="height: 5px; background: rgba(255, 215, 0, 0.1); border-radius: 2px; margin-bottom: 15px;">
                    <div style="height: 5px; width: {row['Count'] / category_counts['Count'].max() * 100}%; background: #FFD700; border-radius: 2px;"></div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        # Recent launches chart (last 30 days)
        st.markdown('<h3 style="color: #FFD700; font-size: 1.2rem;">Tokens Launched in Last 30 Days</h3>', unsafe_allow_html=True)
        
        # Group by days since launch
        launch_data = df[df['days_since_launch'] <= 30].copy()
        
        if not launch_data.empty:
            # Add a datestamp column
            launch_data['date_bucket'] = pd.to_datetime(launch_data['launch_date']).dt.strftime('%Y-%m-%d')
            
            # Count launches by date
            launch_counts = launch_data.groupby('date_bucket').size().reset_index()
            launch_counts.columns = ['Date', 'Count']
            launch_counts['Date'] = pd.to_datetime(launch_counts['Date'])
            launch_counts = launch_counts.sort_values('Date')
            
            # Create a timeseries chart
            fig = px.bar(
                launch_counts,
                x='Date',
                y='Count',
                title='AI Token Launches (Last 30 Days)',
                labels={'Count': 'Number of Launches', 'Date': 'Launch Date'}
            )
            
            fig.update_traces(
                marker_color='rgba(255, 215, 0, 0.8)',
                marker_line_color='rgba(255, 215, 0, 1.0)',
                marker_line_width=1
            )
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Launch Date",
                yaxis_title="Number of Tokens",
                height=400,
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                title={
                    'text': "AI Token Launches (Last 30 Days)",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show performance metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Average performance by recency
                df['age_group'] = pd.cut(
                    df['days_since_launch'], 
                    bins=[0, 7, 14, 30, 60, 90], 
                    labels=['< 7 days', '7-14 days', '14-30 days', '30-60 days', '60-90 days']
                )
                
                avg_perf_by_age = df.groupby('age_group')['price_change_24h'].mean().reset_index()
                
                fig = px.bar(
                    avg_perf_by_age, 
                    x='age_group', 
                    y='price_change_24h',
                    title='Average 24h Performance by Token Age',
                    labels={'age_group': 'Token Age', 'price_change_24h': 'Avg. 24h Change (%)'},
                    color='price_change_24h',
                    color_continuous_scale=['#FF3D71', '#A0A0A0', '#00FF9E'],
                    color_continuous_midpoint=0
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    height=350,
                    margin=dict(l=10, r=10, t=50, b=10),
                    xaxis=dict(
                        gridcolor='rgba(255, 215, 0, 0.1)',
                        linecolor='rgba(255, 215, 0, 0.5)'
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255, 215, 0, 0.1)',
                        linecolor='rgba(255, 215, 0, 0.5)'
                    ),
                    title={
                        'text': "Average 24h Performance by Token Age",
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'color': '#FFD700', 'size': 16}
                    }
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Compare volume between older and newer tokens
                df['new_token'] = df['days_since_launch'] <= 30
                
                volume_by_age = df.groupby('new_token')['volume_24h'].mean().reset_index()
                volume_by_age['new_token'] = volume_by_age['new_token'].map({True: 'New Tokens (≤30d)', False: 'Older Tokens (>30d)'})
                volume_by_age.columns = ['Token Age', 'Average Volume']
                
                fig = px.bar(
                    volume_by_age, 
                    x='Token Age', 
                    y='Average Volume',
                    title='Average 24h Volume by Token Age',
                    labels={'Average Volume': 'Avg. 24h Volume ($)'},
                    color='Token Age',
                    color_discrete_map={'New Tokens (≤30d)': '#FFD700', 'Older Tokens (>30d)': '#A0A0A0'}
                )
                
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    height=350,
                    margin=dict(l=10, r=10, t=50, b=10),
                    xaxis=dict(
                        gridcolor='rgba(255, 215, 0, 0.1)',
                        linecolor='rgba(255, 215, 0, 0.5)'
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255, 215, 0, 0.1)',
                        linecolor='rgba(255, 215, 0, 0.5)',
                        type='log'  # Log scale for better visualization
                    ),
                    title={
                        'text': "Average 24h Volume by Token Age",
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'color': '#FFD700', 'size': 16}
                    }
                )
                
                # Format y-axis ticks with dollar signs
                fig.update_yaxes(
                    tickprefix="$",
                    tickformat=".2s"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No tokens launched in the last 30 days.")
    
    with tab3:
        st.markdown('<h3 style="color: #FFD700; font-size: 1.2rem;">Risk Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Risk score vs Market Cap scatter plot
            fig = px.scatter(
                df,
                x='market_cap',
                y='risk_score',
                color='days_since_launch',
                size='volume_24h',
                hover_name='name',
                hover_data={
                    'symbol': True,
                    'price': ':.6f',
                    'market_cap': ':,.0f',
                    'days_since_launch': ':.0f',
                    'price_change_24h': ':+.2f%',
                    'risk_score': ':.1f',
                    'volume_24h': ':,.0f'
                },
                color_continuous_scale=px.colors.sequential.Viridis_r,  # Reversed so newer tokens are brighter
                labels={
                    'market_cap': 'Market Cap ($)',
                    'risk_score': 'Risk Score (1-10)',
                    'days_since_launch': 'Days Since Launch'
                },
                title='Risk Assessment of New AI Tokens',
                log_x=True  # Log scale for market cap
            )
            
            fig.update_traces(
                marker=dict(
                    line=dict(width=1, color='#000000')
                )
            )
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                height=500,
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    title={'font': {'color': '#CCCCCC'}}
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    title={'font': {'color': '#CCCCCC'}}
                ),
                coloraxis_colorbar=dict(
                    title="Days Since<br>Launch",
                    thicknessmode="pixels", thickness=20,
                    lenmode="pixels", len=300,
                    yanchor="top", y=1,
                    ticks="outside", ticksuffix=" days",
                    title_font=dict(color="#CCCCCC"),
                    tickfont=dict(color="#CCCCCC")
                ),
                title={
                    'text': "Risk Assessment of New AI Tokens",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            # Format x-axis ticks with dollar signs
            fig.update_xaxes(
                tickprefix="$",
                tickformat=".2s"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk score distribution
            st.markdown("""
            <div style="background-color: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h4 style="color: #FFD700; margin-top: 0;">Risk Score Explained</h4>
                <p style="margin-bottom: 10px; font-size: 0.9rem;">The risk score (1-10) is calculated based on:</p>
                <ul style="margin-bottom: 0; padding-left: 20px; font-size: 0.9rem;">
                    <li>Token age (newer = higher risk)</li>
                    <li>Market capitalization (smaller = higher risk)</li>
                    <li>Price volatility (higher volatility = higher risk)</li>
                    <li>Liquidity ratio (lower volume/mcap = higher risk)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk distribution chart
            risk_distribution = df['risk_score'].value_counts().reset_index()
            risk_distribution.columns = ['Risk Score', 'Count']
            risk_distribution = risk_distribution.sort_values('Risk Score')
            
            fig = px.bar(
                risk_distribution,
                x='Risk Score',
                y='Count',
                title='Distribution of Risk Scores',
                color='Risk Score',
                color_continuous_scale=['#00FF9E', '#FFD700', '#FF3D71'],
                labels={'Count': 'Number of Tokens'}
            )
            
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                height=300,
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    dtick=1  # Force integer ticks
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                coloraxis_colorbar_visible=False,
                title={
                    'text': "Distribution of Risk Scores",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 16}
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show top new launches
    st.markdown('<h2 class="gold-header">Top New AI Token Launches</h2>', unsafe_allow_html=True)
    
    # Filter to tokens launched in last 30 days
    new_tokens = df[df['days_since_launch'] <= 30].copy()
    
    # Sort by performance for "hot" new tokens
    hot_new_tokens = new_tokens.sort_values('price_change_24h', ascending=False).head(12)
    
    # Create 3x4 grid for token cards
    rows = [hot_new_tokens.iloc[i:i+4] for i in range(0, len(hot_new_tokens), 4)]
    
    for row_tokens in rows:
        cols = st.columns(4)
        for i, (_, token) in enumerate(row_tokens.iterrows()):
            with cols[i]:
                # Format values
                price_str = f"${token['price']:.6f}"
                mcap_str = processor.format_number(token['market_cap'])
                
                # Determine price change color and sign
                change_color = "positive" if token['price_change_24h'] >= 0 else "negative"
                change_sign = "+" if token['price_change_24h'] >= 0 else ""
                change_str = f"{change_sign}{token['price_change_24h']:.2f}%"
                
                # Calculate days since launch
                days_str = f"{token['days_since_launch']:.0f} days ago"
                
                st.markdown(f"""
                <div class="token-card">
                    <div class="token-symbol">{token['symbol']}</div>
                    <div class="token-name">{token['name']}</div>
                    <div class="token-price">{price_str}</div>
                    <div class="token-mcap">MCap: {mcap_str}</div>
                    <div class="token-change {change_color}">{change_str} (24h)</div>
                    <div style="font-size: 0.8rem; margin-top: 8px; color: #A0A0A0;">Launched: {days_str}</div>
                    <div class="category-badge">{token['category']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Show all new tokens in a table
    st.markdown('<h2 class="gold-header">New AI Launch Table</h2>', unsafe_allow_html=True)
    
    # Add filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        market_cap_filter = st.selectbox(
            "Filter by Market Cap",
            ["All", "Nano Cap (<$1M)", "Micro Cap ($1M-$10M)", "Small Cap ($10M-$70M)"]
        )
    
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(list(df['category'].unique()))
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Launch Date (Newest)", "Market Cap (Highest)", "24h Change (Best)", "Risk Score (Lowest)"]
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if market_cap_filter != "All":
        filtered_df = filtered_df[filtered_df['market_cap_category'] == market_cap_filter]
        
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    # Apply sorting
    if sort_by == "Launch Date (Newest)":
        filtered_df = filtered_df.sort_values('days_since_launch')
    elif sort_by == "Market Cap (Highest)":
        filtered_df = filtered_df.sort_values('market_cap', ascending=False)
    elif sort_by == "24h Change (Best)":
        filtered_df = filtered_df.sort_values('price_change_24h', ascending=False)
    elif sort_by == "Risk Score (Lowest)":
        filtered_df = filtered_df.sort_values('risk_score')
    
    # Prepare display dataframe
    display_df = filtered_df.copy()
    
    # Format columns for display
    display_df['Price'] = display_df['price'].apply(lambda x: f"${x:.6f}")
    display_df['Market Cap'] = display_df['market_cap'].apply(processor.format_number)
    display_df['24h Change'] = display_df['price_change_24h'].apply(lambda x: f"{'+' if x >= 0 else ''}{x:.2f}%")
    display_df['Volume (24h)'] = display_df['volume_24h'].apply(processor.format_number)
    display_df['Launch Date'] = pd.to_datetime(display_df['launch_date']).dt.strftime('%b %d, %Y')
    display_df['Age (Days)'] = display_df['days_since_launch'].round().astype(int)
    display_df['Risk Score'] = display_df['risk_score'].round(1)
    
    # Select and rename columns for display
    display_df = display_df[[
        'name', 'symbol', 'Price', 'Market Cap', '24h Change', 'Volume (24h)', 
        'Launch Date', 'Age (Days)', 'category', 'Risk Score'
    ]]
    
    display_df.columns = [
        'Name', 'Symbol', 'Price', 'Market Cap', '24h Change', 'Volume (24h)', 
        'Launch Date', 'Age (Days)', 'Category', 'Risk Score'
    ]
    
    # Show the data table
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500,
        column_config={
            "24h Change": st.column_config.Column(
                "24h Change",
                help="Price change in the last 24 hours",
                width="medium"
            ),
            "Risk Score": st.column_config.ProgressColumn(
                "Risk Score",
                help="Risk assessment score (1-10). Higher values indicate higher risk.",
                min_value=0,
                max_value=10,
                format="%.1f",
                width="medium"
            )
        },
        hide_index=True
    )
    
    # Show token descriptions for selected tokens
    with st.expander("Select a token to view detailed information"):
        selected_token_name = st.selectbox(
            "Select token:",
            options=filtered_df['name'].tolist(),
            format_func=lambda x: f"{x} ({filtered_df[filtered_df['name'] == x]['symbol'].iloc[0]})"
        )
        
        if selected_token_name:
            selected_token = filtered_df[filtered_df['name'] == selected_token_name].iloc[0]
            
            st.markdown(f"<h3 style='color: #FFD700;'>{selected_token['name']} ({selected_token['symbol']})</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {selected_token['description']}")
                st.markdown(f"**Category:** {selected_token['category']}")
                st.markdown(f"**Launch Date:** {pd.to_datetime(selected_token['launch_date']).strftime('%B %d, %Y')} ({selected_token['days_since_launch']:.0f} days ago)")
                st.markdown(f"**Price:** ${selected_token['price']:.6f}")
                st.markdown(f"**Market Cap:** {processor.format_number(selected_token['market_cap'])}")
                st.markdown(f"**Circulating Supply:** {processor.format_number(selected_token['circulating_supply'])}")
                
            with col2:
                # Create a risk meter visualization
                risk_fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = selected_token['risk_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "#FFFFFF"},
                        'bar': {'color': "#FFD700"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "#FFFFFF",
                        'steps': [
                            {'range': [0, 3], 'color': 'rgba(0, 255, 158, 0.3)'},
                            {'range': [3, 7], 'color': 'rgba(255, 215, 0, 0.3)'},
                            {'range': [7, 10], 'color': 'rgba(255, 61, 113, 0.3)'}
                        ]
                    },
                    title = {'text': "Risk Score", 'font': {'color': '#FFD700'}}
                ))
                
                risk_fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    height=200,
                    margin=dict(l=20, r=20, t=40, b=20),
                    font={'color': "#FFFFFF"}
                )
                
                st.plotly_chart(risk_fig, use_container_width=True)
                
                # Simple performance indicators
                change_24h_color = "#00FF9E" if selected_token['price_change_24h'] >= 0 else "#FF3D71"
                change_7d_color = "#00FF9E" if selected_token['price_change_7d'] >= 0 else "#FF3D71"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div>24h Change:</div>
                    <div style="color: {change_24h_color}; font-weight: bold;">
                        {'+' if selected_token['price_change_24h'] >= 0 else ''}{selected_token['price_change_24h']:.2f}%
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                    <div>7d Change:</div>
                    <div style="color: {change_7d_color}; font-weight: bold;">
                        {'+' if selected_token['price_change_7d'] >= 0 else ''}{selected_token['price_change_7d']:.2f}%
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                    <div>24h Volume:</div>
                    <div>${processor.format_number(selected_token['volume_24h'])}</div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_new_ai_launch()