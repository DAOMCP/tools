import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import CoinGeckoAPI
from utils.data_processor import DataProcessor

def render_dashboard():
    """Render the main dashboard view"""
    st.subheader("AI Token Dashboard")
    
    # Initialize data fetcher and processor
    api = CoinGeckoAPI()
    processor = DataProcessor()
    
    # Create loading spinner while fetching data
    with st.spinner("Fetching AI token data..."):
        # Get all AI-related tokens
        df = api.get_ai_related_tokens()
    
    if df.empty:
        st.error("No data available. Please check your internet connection or try again later.")
        return
    
    # Filter the data based on user settings
    filtered_df = processor.filter_tokens(df, st.session_state.filter_settings)
    
    # Market Overview Section
    market_stats = processor.calculate_market_stats(filtered_df)
    render_market_overview(market_stats)
    
    # Top Gainers and Losers
    render_gainers_losers(filtered_df)
    
    # Token list with interactive table
    render_token_table(filtered_df)
    
    # Market cap distribution chart
    render_market_cap_distribution(filtered_df)
    
    # Token launch trends chart
    render_token_launch_trends(filtered_df)
    
    # Token performance trends
    render_performance_trends(filtered_df)

def render_market_overview(stats):
    """Render the market overview section with key metrics"""
    st.subheader("Market Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total AI Tokens",
            value=f"{stats['total_tokens']:,}",
            delta=None
        )
    
    with col2:
        formatted_mcap = DataProcessor.format_number(stats['total_market_cap'])
        st.metric(
            label="Total Market Cap",
            value=formatted_mcap,
            delta=None
        )
    
    with col3:
        st.metric(
            label="Average 24h Change",
            value=f"{stats['avg_24h_change']:.2f}%",
            delta=f"{stats['avg_24h_change']:.2f}%",
            delta_color="normal"
        )
    
    # Display tokens by market cap category
    if stats['token_counts_by_cap']:
        # Create a horizontal bar chart
        categories = list(stats['token_counts_by_cap'].keys())
        counts = list(stats['token_counts_by_cap'].values())
        
        fig = go.Figure(go.Bar(
            y=categories,
            x=counts,
            orientation='h',
            marker=dict(
                color='rgba(126, 87, 194, 0.8)',
                line=dict(color='rgba(126, 87, 194, 1.0)', width=2)
            )
        ))
        
        fig.update_layout(
            title="Tokens by Market Cap Category",
            xaxis_title="Number of Tokens",
            yaxis_title="Market Cap Category",
            template="plotly_dark",
            height=400,
            margin=dict(l=0, r=10, t=30, b=0),
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_gainers_losers(df):
    """Render the top gainers and losers section"""
    st.subheader("Top Performers")
    
    # Get top 5 gainers and losers
    gainers, losers = DataProcessor.get_top_gainers_losers(df, n=5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Top Gainers (24h)")
        if gainers.empty:
            st.info("No gainers data available")
        else:
            for _, token in gainers.iterrows():
                render_token_card(token, is_gainer=True)
    
    with col2:
        st.markdown("### 📉 Top Losers (24h)")
        if losers.empty:
            st.info("No losers data available")
        else:
            for _, token in losers.iterrows():
                render_token_card(token, is_gainer=False)

def render_token_card(token, is_gainer=True):
    """Render a card with token information"""
    price_change = token.get('price_change_24h', 0)
    color = "green" if price_change >= 0 else "red"
    
    card = f"""
    <div style="padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: rgba(45, 55, 72, 0.7);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0;">{token['name']} ({token['symbol']})</h4>
                <p style="margin: 5px 0;">Price: ${token['price']:,.6f}</p>
            </div>
            <div style="text-align: right;">
                <h3 style="color: {color}; margin: 0;">{price_change:+.2f}%</h3>
                <p style="margin: 5px 0; font-size: 0.8em;">Market Cap: {DataProcessor.format_number(token['market_cap'])}</p>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card, unsafe_allow_html=True)
    
    # Make the entire card clickable
    if st.button(f"View Details for {token['symbol']}", key=f"btn_{token['id']}"):
        st.session_state.selected_token = token['id']
        st.session_state.view = "token_details"
        st.rerun()

def render_token_table(df):
    """Render an interactive table of tokens"""
    st.subheader("AI Tokens List")
    
    if df.empty:
        st.info("No tokens match your filter criteria")
        return
    
    # Create a copy of the DataFrame with formatted columns for display
    display_df = df.copy()
    
    # Format market cap and price columns
    display_df['Market Cap'] = display_df['market_cap'].apply(DataProcessor.format_number)
    display_df['Price'] = display_df['price'].apply(lambda x: f"${x:,.6f}")
    display_df['24h Change'] = display_df['price_change_24h'].apply(lambda x: f"{x:+.2f}%")
    display_df['Volume (24h)'] = display_df['volume_24h'].apply(DataProcessor.format_number)
    
    # Select columns to display
    display_df = display_df[[
        'name', 'symbol', 'Price', 'Market Cap', '24h Change', 'Volume (24h)', 'market_cap_category'
    ]]
    
    # Rename columns for better display
    display_df.columns = ['Name', 'Symbol', 'Price', 'Market Cap', '24h Change', 'Volume (24h)', 'Category']
    
    # Display the table with a height limit
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        column_config={
            "24h Change": st.column_config.Column(
                "24h Change",
                help="Price change in the last 24 hours",
                width="medium",
            )
        },
        hide_index=True
    )
    
    # Add option to view full token details
    with st.expander("Click on a row to view token details"):
        selected_indices = st.multiselect(
            "Select tokens to view details:",
            options=df['name'].tolist(),
            format_func=lambda x: f"{x} ({df[df['name'] == x]['symbol'].iloc[0]})"
        )
        
        if selected_indices:
            selected_token = df[df['name'] == selected_indices[0]]['id'].iloc[0]
            if st.button(f"View Details for {selected_indices[0]}"):
                st.session_state.selected_token = selected_token
                st.session_state.view = "token_details"
                st.rerun()

def render_market_cap_distribution(df):
    """Render market cap distribution chart"""
    st.subheader("Market Cap Distribution")
    
    if df.empty:
        st.info("No data available for market cap distribution")
        return
    
    # Create a copy to avoid modifying the original
    plot_df = df.copy()
    
    # Create a treemap of market cap by category
    fig = px.treemap(
        plot_df,
        path=['market_cap_category', 'name'],
        values='market_cap',
        color='price_change_24h',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        hover_data={'price': ':.6f', 'price_change_24h': ':+.2f%'},
        title='AI Token Market Cap Distribution'
    )
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_token_launch_trends(df):
    """Render token launch trends chart"""
    st.subheader("Token Activity Over Time")
    
    # Process data to get launch trends
    trends_df = DataProcessor.analyze_token_launch_trends(df)
    
    if trends_df.empty:
        st.info("No data available for token activity trends")
        return
    
    # Create a line chart of token counts over time
    fig = px.line(
        trends_df,
        x='month',
        y='count',
        markers=True,
        title='AI Token Activity by Month',
        labels={'month': 'Month', 'count': 'Number of Tokens'}
    )
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Number of Tokens",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=0),
        height=400
    )
    
    # Add hover annotations
    fig.update_traces(
        hovertemplate='<b>%{x|%b %Y}</b><br>Tokens: %{y}<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_performance_trends(df):
    """Render performance trends of AI tokens"""
    st.subheader("Performance Trends")
    
    if df.empty or len(df) < 5:
        st.info("Not enough data available for performance trends")
        return
    
    # Create tabs for different visualization options
    tab1, tab2 = st.tabs(["Price Change Distribution", "Market Cap vs. Volume"])
    
    with tab1:
        # Create a histogram of 24h price changes
        fig = px.histogram(
            df,
            x='price_change_24h',
            nbins=30,
            title='Distribution of 24h Price Changes',
            color_discrete_sequence=['rgba(126, 87, 194, 0.8)']
        )
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="24h Price Change (%)",
            yaxis_title="Number of Tokens",
            bargap=0.2,
            margin=dict(l=0, r=0, t=50, b=0),
            height=400
        )
        
        # Add a vertical line at 0%
        fig.add_vline(
            x=0, 
            line_dash="dash", 
            line_color="white",
            annotation_text="0%",
            annotation_position="top right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Create a scatter plot of market cap vs volume
        fig = px.scatter(
            df,
            x='market_cap',
            y='volume_24h',
            size='price_change_24h',
            color='price_change_24h',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            hover_name='name',
            hover_data={
                'symbol': True,
                'price': ':.6f',
                'market_cap': ':,.0f',
                'volume_24h': ':,.0f',
                'price_change_24h': ':+.2f%'
            },
            title='Market Cap vs. 24h Volume',
            log_x=True,
            log_y=True,
            size_max=30
        )
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Market Cap (log scale)",
            yaxis_title="24h Volume (log scale)",
            margin=dict(l=0, r=0, t=50, b=0),
            height=500
        )
        
        # Update hover template
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Symbol: %{customdata[0]}<br>Price: $%{customdata[1]:.6f}<br>Market Cap: $%{customdata[2]:,.0f}<br>Volume: $%{customdata[3]:,.0f}<br>24h Change: %{customdata[4]}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
