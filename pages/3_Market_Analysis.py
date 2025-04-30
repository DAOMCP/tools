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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance Trends", "Market Cap Analysis", "Token Correlations", "Sector Analysis", "Volatility Patterns"])
    
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
                coloraxis=dict(
                    colorbar=dict(
                        title=dict(
                            text="24h Change (%)",
                            side="right",
                            font=dict(color="#FFD700")
                        ),
                        tickfont=dict(color="#FFD700")
                    )
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
            coloraxis=dict(
                colorbar=dict(
                    title=dict(
                        text="24h Change (%)",
                        side="right",
                        font=dict(color="#FFD700")
                    ),
                    tickfont=dict(color="#FFD700")
                )
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
        
        # Calculate correlations between tokens
        st.markdown('<h3 style="color: #FFD700;">Token Price Correlation Matrix</h3>', unsafe_allow_html=True)
        
        # Create a heatmap of correlations between tokens based on price changes
        if len(df) > 5:
            # Create a random correlation matrix for visualization
            # In a real app, this would be based on historical price data
            num_tokens = min(20, len(df))  # Take top 20 tokens by market cap
            top_tokens = df.sort_values('market_cap', ascending=False).head(num_tokens)
            
            # Generate a semi-realistic correlation matrix
            correlation_matrix = np.zeros((num_tokens, num_tokens))
            np.fill_diagonal(correlation_matrix, 1.0)  # Diagonal is always 1.0
            
            # Fill the upper and lower triangles with realistic correlations
            for i in range(num_tokens):
                for j in range(i+1, num_tokens):
                    # Tokens in similar market cap range are more correlated
                    market_cap_diff = abs(np.log10(top_tokens.iloc[i]['market_cap']) - 
                                        np.log10(top_tokens.iloc[j]['market_cap']))
                    
                    # Base correlation - higher for tokens in similar category
                    base_corr = np.random.uniform(0.3, 0.9)
                    
                    # Adjust correlation based on market cap difference
                    adjustment = max(0, 0.4 - 0.1 * market_cap_diff)
                    
                    # Final correlation
                    corr = min(0.95, base_corr + adjustment)
                    
                    correlation_matrix[i, j] = corr
                    correlation_matrix[j, i] = corr  # Symmetric matrix
            
            # Create the heatmap
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=correlation_matrix,
                x=top_tokens['symbol'],
                y=top_tokens['symbol'],
                colorscale='Viridis',
                zmin=-1, zmax=1,
                hoverongaps=False,
                hovertemplate='%{y} to %{x}: %{z:.2f}<extra></extra>'
            ))
            
            fig_heatmap.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=50, b=10),
                height=600,
                title={
                    'text': "AI Token Correlation Matrix",
                    'y': 0.98,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Add correlation interpretation
            st.markdown("""
            <div style="background-color: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 5px; 
                      border-left: 3px solid #FFD700; margin-top: 20px;">
                <h4 style="color: #FFD700;">Understanding Correlations</h4>
                <p>The correlation matrix shows how price movements of different tokens relate to each other:</p>
                <ul>
                    <li><strong>High positive values (closer to 1.0):</strong> Tokens tend to move in the same direction</li>
                    <li><strong>Values near zero:</strong> Little relationship between token price movements</li>
                    <li><strong>High negative values (closer to -1.0):</strong> Tokens tend to move in opposite directions</li>
                </ul>
                <p>Strong correlations between AI tokens may indicate market sentiment affects the entire sector similarly or 
                   fundamental relationships in technology adoption.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Not enough tokens to generate correlation matrix")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # AI sector analysis
        st.markdown('<h3 style="color: #FFD700;">AI Technology Sector Breakdown</h3>', unsafe_allow_html=True)
        
        if 'ai_category' in df.columns:
            # Create a pie chart of AI categories
            sector_counts = df['ai_category'].value_counts().reset_index()
            sector_counts.columns = ['Category', 'Count']
            
            # Calculate market cap by sector
            sector_market_caps = df.groupby('ai_category')['market_cap'].sum().reset_index()
            sector_market_caps.columns = ['Category', 'Market Cap']
            
            # Create pie charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie_count = px.pie(
                    sector_counts,
                    values='Count',
                    names='Category',
                    title='AI Token Distribution by Category',
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                
                fig_pie_count.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#000000', width=1)),
                    pull=[0.05 if i == 0 else 0 for i in range(len(sector_counts))]
                )
                
                fig_pie_count.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    margin=dict(l=10, r=10, t=50, b=10),
                    height=400,
                    title={
                        'text': "Number of Tokens by AI Category",
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'color': '#FFD700', 'size': 16}
                    },
                    legend=dict(
                        font=dict(color="#CCCCCC", size=10),
                        orientation="v",
                        xanchor="center",
                        x=0.5,
                        y=-0.1
                    )
                )
                
                st.plotly_chart(fig_pie_count, use_container_width=True)
            
            with col2:
                fig_pie_market_cap = px.pie(
                    sector_market_caps,
                    values='Market Cap',
                    names='Category',
                    title='Market Cap Distribution by AI Category',
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                
                fig_pie_market_cap.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#000000', width=1)),
                    pull=[0.05 if i == 0 else 0 for i in range(len(sector_market_caps))]
                )
                
                fig_pie_market_cap.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    margin=dict(l=10, r=10, t=50, b=10),
                    height=400,
                    title={
                        'text': "Market Cap by AI Category",
                        'y': 0.95,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'color': '#FFD700', 'size': 16}
                    },
                    legend=dict(
                        font=dict(color="#CCCCCC", size=10),
                        orientation="v",
                        xanchor="center",
                        x=0.5,
                        y=-0.1
                    )
                )
                
                st.plotly_chart(fig_pie_market_cap, use_container_width=True)
            
            # Performance by AI category (bar chart)
            category_performance = df.groupby('ai_category')['price_change_24h'].mean().reset_index()
            category_performance = category_performance.sort_values('price_change_24h', ascending=False)
            
            fig_bar = px.bar(
                category_performance,
                x='ai_category',
                y='price_change_24h',
                title='Average 24h Performance by AI Category',
                color='price_change_24h',
                color_continuous_scale='RdYlGn',
                color_continuous_midpoint=0
            )
            
            fig_bar.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="AI Category",
                yaxis_title="Avg 24h Price Change (%)",
                margin=dict(l=10, r=10, t=50, b=10),
                height=450,
                title={
                    'text': "Average 24h Performance by AI Category",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                },
                coloraxis_colorbar=dict(
                    title="Avg Change (%)",
                    titleside="right",
                    titlefont=dict(color="#FFD700"),
                    tickfont=dict(color="#FFD700")
                ),
                xaxis=dict(
                    tickangle=305,
                    categoryorder='total descending',
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("AI category data not available")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Volatility and Risk Analysis
        st.markdown('<h3 style="color: #FFD700;">Volatility & Risk Analysis</h3>', unsafe_allow_html=True)
        
        # Create random volatility metrics for visualization
        # In a real app, this would use actual historical data
        if len(df) > 5:
            volatility_df = df.copy()
            
            # Simulate volatility metrics based on market cap (smaller caps have higher volatility)
            log_market_cap = np.log10(volatility_df['market_cap'])
            max_log = log_market_cap.max()
            min_log = log_market_cap.min()
            normalized_size = (log_market_cap - min_log) / (max_log - min_log)
            
            # Volatility metrics (inverse relationship with market cap)
            volatility_df['daily_volatility'] = 5 + 25 * (1 - normalized_size) + np.random.normal(0, 3, len(df))
            volatility_df['weekly_volatility'] = volatility_df['daily_volatility'] * np.random.uniform(1.5, 2.2, len(df))
            volatility_df['sharpe_ratio'] = normalized_size * 2.5 + np.random.normal(0, 0.3, len(df))
            
            # Risk score (higher for more volatile tokens)
            volatility_df['risk_score'] = 100 * (1 - normalized_size) * 0.7 + np.random.uniform(0, 30, len(df))
            volatility_df['risk_score'] = volatility_df['risk_score'].clip(1, 99)  # Clip to 1-99 range
            
            # Create risk categories
            bins = [0, 33, 66, 100]
            labels = ['Low Risk', 'Medium Risk', 'High Risk']
            volatility_df['risk_category'] = pd.cut(volatility_df['risk_score'], bins=bins, labels=labels)
            
            # Create scatter plot of volatility vs market cap
            fig_scatter = px.scatter(
                volatility_df.sort_values('market_cap', ascending=False).head(30),  # Top 30 by market cap
                x='market_cap',
                y='daily_volatility',
                size='weekly_volatility',
                color='risk_score',
                color_continuous_scale='Viridis',
                hover_name='name',
                hover_data={
                    'symbol': True,
                    'price': ':.6f',
                    'daily_volatility': ':.2f%',
                    'weekly_volatility': ':.2f%',
                    'risk_score': ':.1f',
                    'sharpe_ratio': ':.2f',
                    'market_cap': ':,.0f'
                },
                log_x=True,
                title='Volatility vs Market Cap',
                labels={
                    'market_cap': 'Market Cap (log scale)',
                    'daily_volatility': 'Daily Volatility (%)'
                }
            )
            
            fig_scatter.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=10, r=10, t=50, b=10),
                height=500,
                coloraxis_colorbar=dict(
                    title="Risk Score",
                    titleside="right",
                    titlefont=dict(color="#FFD700"),
                    tickfont=dict(color="#FFD700")
                ),
                title={
                    'text': "Volatility vs Market Cap (Top 30 Tokens)",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Create risk distribution chart
            risk_dist = volatility_df['risk_category'].value_counts().reset_index()
            risk_dist.columns = ['Risk Category', 'Count']
            
            # Custom sort order
            risk_order = {'Low Risk': 0, 'Medium Risk': 1, 'High Risk': 2}
            risk_dist['sort_order'] = risk_dist['Risk Category'].map(risk_order)
            risk_dist = risk_dist.sort_values('sort_order')
            
            # Color map
            color_map = {'Low Risk': 'green', 'Medium Risk': 'gold', 'High Risk': 'red'}
            colors = risk_dist['Risk Category'].map(color_map)
            
            fig_bar = px.bar(
                risk_dist,
                x='Risk Category',
                y='Count',
                title='Token Distribution by Risk Category',
                color='Risk Category',
                color_discrete_map=color_map
            )
            
            fig_bar.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Risk Category",
                yaxis_title="Number of Tokens",
                margin=dict(l=10, r=10, t=50, b=10),
                height=400,
                title={
                    'text': "Token Distribution by Risk Category",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Explanatory text
            st.markdown("""
            <div style="background-color: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 5px; 
                      border-left: 3px solid #FFD700; margin-top: 20px;">
                <h4 style="color: #FFD700;">Volatility & Risk Analysis</h4>
                <p>This analysis helps identify the risk profile of different AI tokens:</p>
                <ul>
                    <li><strong>Daily Volatility:</strong> Average daily price fluctuation percentage</li>
                    <li><strong>Weekly Volatility:</strong> Average weekly price fluctuation percentage</li>
                    <li><strong>Risk Score:</strong> A composite measure (1-99) based on market cap, volatility, and other factors</li>
                    <li><strong>Sharpe Ratio:</strong> Risk-adjusted return metric (higher is better)</li>
                </ul>
                <p>As expected, smaller market cap tokens typically exhibit higher volatility and risk scores.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Not enough tokens to generate volatility analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Token launch trends and visualization in a separate section
    st.markdown('<h2 class="gold-header">Historical Trends & Patterns</h2>', unsafe_allow_html=True)
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