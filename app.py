import streamlit as st
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.token_details import render_token_details

# Set page configuration
st.set_page_config(
    page_title="M100D - AI Token Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
def render_header():
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Using an emoji as a temporary logo (instead of an image)
        st.markdown("<h1 style='font-size: 60px; text-align: center;'>🤖</h1>", unsafe_allow_html=True)
    
    with col2:
        st.title("M100D")
        st.markdown("### AI Token Analytics Platform")
        
    st.markdown("""
    As the AI token landscape rapidly expands, it's becoming increasingly difficult to distinguish signal from noise. 
    Many projects lack transparency, technical clarity, or even basic legitimacy. 
    M100D is here to change that. We're building a comprehensive, open analytics platform 
    that brings structure and insight to the AI token ecosystem. 
    Our mission is to make this space understandable, credible, and accessible to all.
    """)
    st.markdown("---")

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
