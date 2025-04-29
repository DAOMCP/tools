import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import CoinGeckoAPI
from utils.data_processor import DataProcessor
from components.animations import render_animated_metric, render_ai_token_visualization

st.set_page_config(
    page_title="M100D - Market Analysis",
    page_icon="📊",
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
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1A1A1A;
        border-radius: 6px 6px 0 0;
        color: #A0A0A0;
        padding: 0 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2A2A2A;
        color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

def render_market_analysis():
    st.markdown('<h1 class="gold-header">AI Token Market Analysis</h1>', unsafe_allow_html=True)
    
    # Initialize API and data processor
    api = CoinGeckoAPI()
    processor = DataProcessor()
    
    # Create loading spinner while fetching data
    with st.spinner("Fetching AI token data..."):
        # Get all AI-related tokens
        df = api.get_ai_related_tokens()
    
    if df.empty:
        st.error("No data available. Please check your internet connection or try again later.")
        return
        
    # Market overview visualization
    st.markdown('<h2 class="gold-header">Market Overview</h2>', unsafe_allow_html=True)
    
    # Calculate market stats
    market_stats = processor.calculate_market_stats(df)
    
    # Visualization tabs for different market aspects
    tab1, tab2, tab3 = st.tabs(["Performance Trends", "Market Cap Analysis", "Token Activity"])
    
    with tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        if len(df) < 5:
            st.info("Not enough data available for performance trends")
        else:
            # Performance visualization
            st.markdown('<h3 style="color: #FFD700;">Price Change Distribution</h3>', unsafe_allow_html=True)
            
            # Create a histogram of 24h price changes with vibrant colors
            fig_hist = px.histogram(
                df,
                x='price_change_24h',
                nbins=30,
                title='Distribution of 24h Price Changes',
                color_discrete_sequence=['#FFD700']  # Gold color
            )
            
            fig_hist.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="24h Price Change (%)",
                yaxis_title="Number of Tokens",
                bargap=0.2,
                margin=dict(l=10, r=10, t=30, b=10),
                height=400,
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    zerolinecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)'
                ),
                title={
                    'text': "Distribution of 24h Price Changes",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            # Add a vertical line at 0%
            fig_hist.add_vline(
                x=0, 
                line_dash="dash", 
                line_color="#FFD700",
                annotation_text="0%",
                annotation_position="top right",
                annotation_font_color="#FFD700"
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Create a copy of the dataframe for scatter plot
            plot_df = df.copy()
            
            # Use absolute value of price change for size, and add a minimum size
            plot_df['bubble_size'] = np.abs(plot_df['price_change_24h']) + 5
            
            # Custom colorscale for better visualization (gold to white)
            custom_colorscale = [
                [0, 'red'],
                [0.5, '#FFD700'],  # Gold in the middle
                [1.0, 'green']
            ]
            
            # Create a scatter plot of market cap vs volume
            fig_scatter = px.scatter(
                plot_df,
                x='market_cap',
                y='volume_24h',
                size='bubble_size',
                color='price_change_24h',
                color_continuous_scale=custom_colorscale,
                color_continuous_midpoint=0,
                hover_name='name',
                hover_data={
                    'symbol': True,
                    'price': ':.6f',
                    'market_cap': ':,.0f',
                    'volume_24h': ':,.0f',
                    'price_change_24h': ':+.2f%',
                    'bubble_size': False
                },
                title='Market Cap vs. 24h Volume',
                log_x=True,
                log_y=True,
                size_max=30
            )
            
            fig_scatter.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Market Cap (log scale)",
                yaxis_title="24h Volume (log scale)",
                margin=dict(l=10, r=10, t=50, b=10),
                height=500,
                coloraxis_colorbar=dict(
                    title="24h Change (%)",
                    titleside="right",
                    titlefont=dict(color="#FFD700"),
                    tickfont=dict(color="#FFD700"),
                ),
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    zerolinecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    zerolinecolor='rgba(255, 215, 0, 0.5)'
                ),
                title={
                    'text': "Market Cap vs. 24h Volume",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Market cap distribution visualization
        st.markdown('<h3 style="color: #FFD700;">Market Cap Distribution</h3>', unsafe_allow_html=True)
        
        # Create a treemap of market cap by category
        fig_treemap = px.treemap(
            df,
            path=['market_cap_category', 'name'],
            values='market_cap',
            color='price_change_24h',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            hover_data={'price': ':.6f', 'price_change_24h': ':+.2f%', 'symbol': True},
        )
        
        fig_treemap.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=10, r=10, t=30, b=10),
            height=600,
            coloraxis_colorbar=dict(
                title="24h Change (%)",
                titleside="right",
                titlefont=dict(color="#FFD700"),
                tickfont=dict(color="#FFD700"),
            ),
            title={
                'text': "AI Token Market Cap Distribution",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 18}
            }
        )
        
        # Update hover template
        fig_treemap.update_traces(
            hovertemplate='<b>%{label}</b><br>Symbol: %{customdata[2]}<br>Market Cap: $%{value:,.0f}<br>Price: $%{customdata[0]:.6f}<br>24h Change: %{customdata[1]}<extra></extra>'
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Bar chart showing token counts by market cap category
        market_cap_counts = df.groupby('market_cap_category').size().reset_index(name='count')
        
        fig_bar = go.Figure(go.Bar(
            y=market_cap_counts['market_cap_category'],
            x=market_cap_counts['count'],
            orientation='h',
            marker=dict(
                color=px.colors.sequential.Viridis,
                line=dict(color='#FFD700', width=1)
            )
        ))
        
        fig_bar.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis_title="Number of Tokens",
            yaxis_title="Market Cap Category",
            margin=dict(l=10, r=10, t=50, b=10),
            height=400,
            xaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
            ),
            yaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
            ),
            title={
                'text': "Token Count by Market Cap Category",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 18}
            }
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # AI token visualization
        st.markdown('<h3 style="color: #FFD700;">AI Token Universe</h3>', unsafe_allow_html=True)
        render_ai_token_visualization()
        
        # Token launch trends 
        st.markdown('<h3 style="color: #FFD700;">Token Activity Over Time</h3>', unsafe_allow_html=True)
        
        # Process data to get launch trends
        trends_df = processor.analyze_token_launch_trends(df)
        
        if trends_df.empty:
            st.info("No data available for token activity trends")
        else:
            # Create a line chart of token counts over time with area fill
            fig_area = px.area(
                trends_df,
                x='month',
                y='count',
                title='AI Token Activity by Month',
                labels={'month': 'Month', 'count': 'Number of Tokens'}
            )
            
            fig_area.update_traces(
                line=dict(color='#FFD700', width=2),
                fillcolor='rgba(255, 215, 0, 0.1)',
                hovertemplate='<b>%{x|%b %Y}</b><br>Tokens: %{y}<extra></extra>'
            )
            
            fig_area.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Month",
                yaxis_title="Number of Tokens",
                hovermode="x unified",
                margin=dict(l=10, r=10, t=50, b=10),
                height=400,
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                title={
                    'text': "AI Token Activity by Month",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig_area, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_market_analysis()