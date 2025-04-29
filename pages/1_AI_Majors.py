import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import CoinGeckoAPI
from utils.data_processor import DataProcessor
from components.animations import render_animated_metric, render_card

st.set_page_config(
    page_title="M100D - AI Majors",
    page_icon="💰",
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
    
    /* Card styling */
    .card {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 3px solid #FFD700;
        margin-bottom: 20px;
    }
    
    /* Metrics */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FFD700;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Table styling enhancements */
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
    
    /* Improve button styling */
    [data-testid="baseButton-secondary"] {
        border-color: #FFD700 !important;
        color: #FFD700 !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: rgba(255, 215, 0, 0.1) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def render_token_explorer():
    st.markdown('<h1 class="gold-header">AI Majors</h1>', unsafe_allow_html=True)
    
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
    
    # Filter the data based on user settings
    if 'filter_settings' not in st.session_state:
        st.session_state.filter_settings = {
            "market_cap_min": 0,
            "market_cap_max": float('inf'),
            "days": 7,
            "sort_by": "market_cap",
            "sort_order": "desc",
            "category": "all"
        }
    
    # Sidebar filters
    st.sidebar.markdown('<h3 class="gold-header">Filter Options</h3>', unsafe_allow_html=True)
    
    # Market cap filter
    st.sidebar.markdown("### Market Cap Filter")
    mcap_options = ["All", "Large Cap (>$1B)", "Mid Cap ($100M-$1B)", "Small Cap ($10M-$100M)", "Micro Cap (<$10M)"]
    selected_mcap = st.sidebar.selectbox("Select Market Cap Range", mcap_options, index=0)
    
    # Sort options
    st.sidebar.markdown("### Sort Options")
    sort_options = ["Market Cap", "Price", "24h Change", "Volume"]
    sort_by = st.sidebar.selectbox("Sort By", sort_options, index=0)
    sort_order = st.sidebar.radio("Sort Order", ["Descending", "Ascending"])
    
    # Apply filters to session state
    if selected_mcap != "All":
        if selected_mcap == "Large Cap (>$1B)":
            st.session_state.filter_settings["market_cap_min"] = 1_000_000_000
            st.session_state.filter_settings["market_cap_max"] = float('inf')
        elif selected_mcap == "Mid Cap ($100M-$1B)":
            st.session_state.filter_settings["market_cap_min"] = 100_000_000
            st.session_state.filter_settings["market_cap_max"] = 1_000_000_000
        elif selected_mcap == "Small Cap ($10M-$100M)":
            st.session_state.filter_settings["market_cap_min"] = 10_000_000
            st.session_state.filter_settings["market_cap_max"] = 100_000_000
        else:  # Micro Cap
            st.session_state.filter_settings["market_cap_min"] = 0
            st.session_state.filter_settings["market_cap_max"] = 10_000_000
    else:
        st.session_state.filter_settings["market_cap_min"] = 0
        st.session_state.filter_settings["market_cap_max"] = float('inf')
    
    # Update sort settings
    st.session_state.filter_settings["sort_by"] = sort_by.lower().replace(" ", "_")
    st.session_state.filter_settings["sort_order"] = "desc" if sort_order == "Descending" else "asc"
    
    # Apply filters
    filtered_df = processor.filter_tokens(df, st.session_state.filter_settings)
    
    # Display token metrics
    st.markdown('<h2 class="gold-header">Token Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate market stats for the filtered dataset
    market_stats = processor.calculate_market_stats(filtered_df)
    
    # Show key metrics in a nice layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_animated_metric("Total Tokens", f"{market_stats.get('total_tokens', 0)}", None, color="gold")
    
    with col2:
        total_mcap = market_stats.get('total_market_cap', 0)
        formatted_mcap = processor.format_number(total_mcap)
        render_animated_metric("Total Market Cap", f"${formatted_mcap}", None, color="gold")
    
    with col3:
        avg_change = market_stats.get('avg_24h_change', 0)
        color = "green" if avg_change >= 0 else "red"
        render_animated_metric("Avg 24h Change", f"{avg_change:.2f}%", None, color=color)
    
    with col4:
        total_vol = market_stats.get('total_volume', 0)
        formatted_vol = processor.format_number(total_vol)
        render_animated_metric("24h Volume", f"${formatted_vol}", None, color="gold")
        
    # Token table with enhanced styling
    st.markdown('<h2 class="gold-header">Token List</h2>', unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.info("No tokens match your filter criteria.")
        return
    
    # Create a copy of the DataFrame with formatted columns for display
    display_df = filtered_df.copy()
    
    # Format market cap and price columns
    display_df['Market Cap'] = display_df['market_cap'].apply(processor.format_number)
    display_df['Price'] = display_df['price'].apply(lambda x: f"${x:,.6f}")
    display_df['24h Change'] = display_df['price_change_24h'].apply(lambda x: f"{x:+.2f}%")
    display_df['Volume (24h)'] = display_df['volume_24h'].apply(processor.format_number)
    
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
        height=500,
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
    with st.expander("Select a token to view detailed information"):
        selected_indices = st.multiselect(
            "Select tokens:",
            options=filtered_df['name'].tolist(),
            format_func=lambda x: f"{x} ({filtered_df[filtered_df['name'] == x]['symbol'].iloc[0]})"
        )
        
        if selected_indices:
            selected_token = filtered_df[filtered_df['name'] == selected_indices[0]]
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"<h3 class='gold-header'>{selected_token['name'].iloc[0]} ({selected_token['symbol'].iloc[0]})</h3>", unsafe_allow_html=True)
                st.markdown(f"**Price:** ${selected_token['price'].iloc[0]:,.6f}")
                st.markdown(f"**Market Cap:** {processor.format_number(selected_token['market_cap'].iloc[0])}")
                st.markdown(f"**24h Change:** {selected_token['price_change_24h'].iloc[0]:+.2f}%")
                st.markdown(f"**24h Volume:** {processor.format_number(selected_token['volume_24h'].iloc[0])}")
                
            with col2:
                # If we have an image URL, display it
                if 'image' in selected_token.columns and not pd.isna(selected_token['image'].iloc[0]):
                    st.image(selected_token['image'].iloc[0], width=100)

    # Distribution overview
    st.markdown('<h2 class="gold-header">Market Distribution</h2>', unsafe_allow_html=True)
    
    # Create a copy to avoid modifying the original
    plot_df = filtered_df.copy()
    
    if not plot_df.empty:
        # Create a pie chart of market cap distribution by category
        market_cap_by_category = plot_df.groupby('market_cap_category')['market_cap'].sum().reset_index()
        market_cap_by_category['percentage'] = (market_cap_by_category['market_cap'] / market_cap_by_category['market_cap'].sum() * 100)
        
        fig = px.pie(
            market_cap_by_category,
            values='market_cap',
            names='market_cap_category',
            title='Market Cap Distribution by Category',
            color_discrete_sequence=px.colors.sequential.Plasma,  # More vibrant colors
            hole=0.4
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='label+percent',
            marker=dict(line=dict(color='#0A0A0A', width=2))
        )
        
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=20, r=20, t=50, b=20),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            title={
                'text': "Market Cap Distribution by Category",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 20}
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    render_token_explorer()