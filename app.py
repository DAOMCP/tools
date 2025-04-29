import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.token_details import render_token_details
from components.animations import render_futuristic_header

# Set page configuration
st.set_page_config(
    page_title="M100D - AI Token Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more futuristic look
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
    }
    
    /* Make the main content area more distinct */
    [data-testid="stSidebar"] > div:first-child {
        background-image: linear-gradient(180deg, #0A1128 0%, #1A2151 100%);
        border-right: 1px solid rgba(0, 228, 255, 0.2);
    }
    
    /* Style scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 33, 81, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 228, 255, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 228, 255, 0.8);
    }
    
    /* Better table styling */
    [data-testid="stTable"] table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }
    
    [data-testid="stTable"] th {
        background-color: rgba(26, 33, 81, 0.8);
        color: white;
        border-bottom: 1px solid rgba(0, 228, 255, 0.3);
    }
    
    [data-testid="stTable"] td {
        border-bottom: 1px solid rgba(0, 228, 255, 0.1);
    }
    
    /* Improve button styling */
    [data-testid="baseButton-secondary"] {
        border-color: rgba(0, 228, 255, 0.4) !important;
        color: rgba(0, 228, 255, 1) !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        border-color: rgba(0, 228, 255, 0.8) !important;
        background-color: rgba(0, 228, 255, 0.1) !important;
        transform: translateY(-2px);
    }
    
    /* Chart container styling */
    .main .block-container [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(10, 17, 40, 0.1);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(0, 228, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    # Use futuristic header component with animations
    render_futuristic_header()

def main():
    # Initialize session state
    if "view" not in st.session_state:
        st.session_state.view = "dashboard"
    
    if "selected_token" not in st.session_state:
        st.session_state.selected_token = None
    
    if "filter_settings" not in st.session_state:
        st.session_state.filter_settings = {
            "market_cap_min": 0,
            "market_cap_max": float('inf'),
            "days": 7,
            "sort_by": "market_cap",
            "sort_order": "desc",
            "category": "all"
        }
    
    # Render the header
    render_header()
    
    # Render the sidebar
    render_sidebar()
    
    # Render the main content based on the current view
    if st.session_state.view == "dashboard":
        render_dashboard()
    elif st.session_state.view == "token_details":
        render_token_details(st.session_state.selected_token)

if __name__ == "__main__":
    main()
