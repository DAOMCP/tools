import streamlit as st
import pandas as pd
from utils.data_fetcher import CoinGeckoAPI

def render_sidebar():
    st.sidebar.title("M100D Controls")
    
    # Search bar
    st.sidebar.subheader("Search AI Tokens")
    search_query = st.sidebar.text_input("Search by name or symbol", "")
    
    # Display view selector
    st.sidebar.subheader("Navigation")
    view_options = ["Dashboard", "Token Details"]
    
    # Use radio buttons instead of select box for better UX
    selected_view = st.sidebar.radio("Select View", view_options, index=0 if st.session_state.view == "dashboard" else 1)
    
    if selected_view == "Dashboard":
        st.session_state.view = "dashboard"
    else:
        st.session_state.view = "token_details"
    
    # Filter section
    st.sidebar.subheader("Filter Options")
    
    # Market cap categories
    market_cap_categories = [
        "all",
        "Large Cap (>$1B)",
        "Mid Cap ($100M-$1B)",
        "Small Cap ($10M-$100M)",
        "Micro Cap ($1M-$10M)",
        "Nano Cap ($500K-$1M)",
        "Ultra Nano Cap (<$500K)"
    ]
    
    selected_category = st.sidebar.selectbox(
        "Market Cap Category",
        market_cap_categories,
        index=market_cap_categories.index(st.session_state.filter_settings.get("category", "all"))
    )
    
    # Time period selector for charts
    time_options = {
        "7": "7 Days",
        "14": "14 Days",
        "30": "30 Days",
        "90": "90 Days",
        "180": "180 Days",
        "365": "1 Year"
    }
    
    selected_time = st.sidebar.selectbox(
        "Time Period",
        list(time_options.keys()),
        index=0,
        format_func=lambda x: time_options[x]
    )
    
    # Sorting options
    sort_options = {
        "market_cap": "Market Cap",
        "price": "Price",
        "price_change_24h": "24h Change",
        "volume_24h": "24h Volume"
    }
    
    sort_by = st.sidebar.selectbox(
        "Sort By",
        list(sort_options.keys()),
        index=list(sort_options.keys()).index(st.session_state.filter_settings.get("sort_by", "market_cap")),
        format_func=lambda x: sort_options[x]
    )
    
    sort_order = st.sidebar.radio(
        "Sort Order",
        ["desc", "asc"],
        index=0 if st.session_state.filter_settings.get("sort_order", "desc") == "desc" else 1,
        format_func=lambda x: "Descending" if x == "desc" else "Ascending"
    )
    
    # Update filter settings in session state
    st.session_state.filter_settings = {
        "category": selected_category,
        "days": int(selected_time),
        "sort_by": sort_by,
        "sort_order": sort_order
    }
    
    # Add a refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        # Clear the cache for the API calls
        st.cache_data.clear()
        st.rerun()
    
    # Show token list if search is active
    if search_query:
        display_search_results(search_query)

def display_search_results(query):
    """Display search results in the sidebar"""
    st.sidebar.subheader("Search Results")
    
    # Fetch data (will use cached data if available)
    api = CoinGeckoAPI()
    df = api.get_ai_related_tokens()
    
    if df.empty:
        st.sidebar.info("No tokens found or data unavailable")
        return
    
    # Filter based on search query
    query = query.lower()
    filtered_df = df[
        df['name'].str.lower().str.contains(query) | 
        df['symbol'].str.lower().str.contains(query)
    ].head(10)
    
    if filtered_df.empty:
        st.sidebar.info("No matching tokens found")
        return
    
    # Display results in a scrollable container
    with st.sidebar.container():
        for _, row in filtered_df.iterrows():
            col1, col2 = st.sidebar.columns([1, 3])
            
            with col1:
                # Display token symbol
                st.write(f"**{row['symbol']}**")
            
            with col2:
                # Make the token name clickable
                if st.button(f"{row['name']}", key=f"search_{row['id']}"):
                    st.session_state.selected_token = row['id']
                    st.session_state.view = "token_details"
                    st.rerun()
