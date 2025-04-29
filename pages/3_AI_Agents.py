import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
from components.animations import render_animated_metric, render_card

st.set_page_config(
    page_title="M100D - AI Agents",
    page_icon="🤖",
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
    .agent-card {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 3px solid #FFD700;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Agent image styling */
    .agent-image {
        border-radius: 10px;
        border: 2px solid #FFD700;
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
    
    /* Timeline styling */
    .timeline-item {
        border-left: 2px solid #FFD700;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    
    .timeline-item:before {
        content: "";
        position: absolute;
        left: -9px;
        top: 0;
        width: 16px;
        height: 16px;
        background-color: #1A1A1A;
        border: 2px solid #FFD700;
        border-radius: 50%;
    }
    
    .timeline-date {
        color: #FFD700;
        font-weight: 500;
        margin-bottom: 5px;
    }
    
    .timeline-content {
        background-color: #1A1A1A;
        border-radius: 6px;
        padding: 15px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Function to fetch AI agent data from Cookie.fun
def fetch_agent_data():
    try:
        # Normally we would fetch from the actual API, but for this example we'll create sample data
        # If we had an API key, we would use something like:
        # response = requests.get("https://api.cookie.fun/agents", headers={"Authorization": f"Bearer {api_key}"})
        # data = response.json()
        
        # For now, let's generate sample data based on popular AI agents
        agents_data = [
            {
                "id": 1,
                "name": "Claude AI",
                "description": "Claude is an AI assistant created by Anthropic to be helpful, harmless, and honest.",
                "category": "Large Language Model",
                "use_cases": ["Content writing", "Research assistance", "Programming help", "Education"],
                "capabilities": ["Text generation", "Logic reasoning", "Code understanding", "Safety aligned"],
                "popularity_score": 95,
                "release_date": "2022-12-15",
                "last_updated": "2023-09-25",
                "pricing": "Freemium",
                "api_access": True,
                "monthly_active_users": 12500000,
                "avg_rating": 4.8
            },
            {
                "id": 2,
                "name": "ChatGPT",
                "description": "OpenAI's conversational AI model that can engage in natural dialogue and assist with a variety of tasks.",
                "category": "Large Language Model",
                "use_cases": ["Customer support", "Content generation", "Coding assistance", "Creative writing"],
                "capabilities": ["Text generation", "Conversation", "Knowledge retrieval", "Problem solving"],
                "popularity_score": 98,
                "release_date": "2022-11-30",
                "last_updated": "2023-11-06",
                "pricing": "Freemium",
                "api_access": True,
                "monthly_active_users": 18000000,
                "avg_rating": 4.7
            },
            {
                "id": 3,
                "name": "Midjourney",
                "description": "An AI image generation tool that creates detailed and artistic visuals from text descriptions.",
                "category": "Image Generation",
                "use_cases": ["Art creation", "Concept visualization", "Design inspiration", "Marketing materials"],
                "capabilities": ["Text-to-image", "Style adaptation", "High resolution output", "Creative interpretation"],
                "popularity_score": 92,
                "release_date": "2022-07-12",
                "last_updated": "2023-11-01",
                "pricing": "Subscription",
                "api_access": True,
                "monthly_active_users": 8000000,
                "avg_rating": 4.9
            },
            {
                "id": 4,
                "name": "DALL-E",
                "description": "OpenAI's AI system that creates realistic images and art from natural language descriptions.",
                "category": "Image Generation",
                "use_cases": ["Illustration", "Product visualization", "Conceptual art", "Content creation"],
                "capabilities": ["Text-to-image", "Photorealistic images", "Creative interpretation", "Style control"],
                "popularity_score": 94,
                "release_date": "2021-01-05",
                "last_updated": "2023-10-10",
                "pricing": "Credits-based",
                "api_access": True,
                "monthly_active_users": 7000000,
                "avg_rating": 4.6
            },
            {
                "id": 5,
                "name": "GitHub Copilot",
                "description": "AI programming assistant that suggests code completions and entire functions in real-time.",
                "category": "Code Assistant",
                "use_cases": ["Code completion", "Function generation", "Documentation", "Bug fixing"],
                "capabilities": ["Code suggestion", "Language support", "IDE integration", "Context awareness"],
                "popularity_score": 89,
                "release_date": "2021-06-29",
                "last_updated": "2023-11-08",
                "pricing": "Subscription",
                "api_access": False,
                "monthly_active_users": 5000000,
                "avg_rating": 4.5
            },
            {
                "id": 6,
                "name": "Gemini",
                "description": "Google's multimodal AI system designed to handle text, images, audio, and video simultaneously.",
                "category": "Multimodal AI",
                "use_cases": ["Research", "Content analysis", "Problem solving", "Creative projects"],
                "capabilities": ["Text generation", "Image understanding", "Audio processing", "Multimodal reasoning"],
                "popularity_score": 90,
                "release_date": "2023-12-06",
                "last_updated": "2024-03-15",
                "pricing": "Freemium",
                "api_access": True,
                "monthly_active_users": 9000000,
                "avg_rating": 4.6
            },
            {
                "id": 7,
                "name": "Sora",
                "description": "OpenAI's text-to-video model that creates realistic and imaginative scenes from text instructions.",
                "category": "Video Generation",
                "use_cases": ["Filmmaking", "Animation", "Marketing", "Educational content"],
                "capabilities": ["Text-to-video", "Scene generation", "Motion continuity", "Creative interpretation"],
                "popularity_score": 87,
                "release_date": "2024-02-15",
                "last_updated": "2024-03-01",
                "pricing": "Limited access",
                "api_access": False,
                "monthly_active_users": 1000000,
                "avg_rating": 4.9
            },
            {
                "id": 8,
                "name": "Perplexity AI",
                "description": "An AI search engine that provides comprehensive answers to questions with cited sources.",
                "category": "Search & Research",
                "use_cases": ["Research", "Fact-checking", "Learning", "Information synthesis"],
                "capabilities": ["Information retrieval", "Source citation", "Comprehensive answers", "Real-time information"],
                "popularity_score": 82,
                "release_date": "2022-08-30",
                "last_updated": "2024-01-20",
                "pricing": "Freemium",
                "api_access": True,
                "monthly_active_users": 4000000,
                "avg_rating": 4.4
            }
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame(agents_data)
        
        # Convert date strings to datetime objects
        df['release_date'] = pd.to_datetime(df['release_date'])
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        return df
    
    except Exception as e:
        st.error(f"Error fetching AI agent data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error

def format_number(num, precision=2):
    """Format large numbers for display"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.{precision}f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.{precision}f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"

def render_ai_agents():
    st.markdown('<h1 class="gold-header">AI Agents Ecosystem</h1>', unsafe_allow_html=True)
    
    # Create a loading spinner while fetching data
    with st.spinner("Fetching AI agents data..."):
        df = fetch_agent_data()
    
    if df.empty:
        st.error("No data available. Please check your connection or try again later.")
        return
    
    # Show key metrics
    total_agents = len(df)
    avg_popularity = df['popularity_score'].mean()
    avg_rating = df['avg_rating'].mean()
    total_users = df['monthly_active_users'].sum()
    
    # Display metrics in a row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_animated_metric("Total Agents", f"{total_agents}", None, color="gold")
    
    with col2:
        render_animated_metric("Avg Popularity", f"{avg_popularity:.1f}/100", None, color="gold")
    
    with col3:
        render_animated_metric("Avg Rating", f"{avg_rating:.1f}/5.0", None, color="gold")
    
    with col4:
        render_animated_metric("Total Monthly Users", f"{format_number(total_users, 1)}", None, color="gold")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Agents Overview", "Popularity Analysis", "Timeline"])
    
    with tab1:
        # Agents card view 
        st.markdown('<h2 class="gold-header">Top AI Agents</h2>', unsafe_allow_html=True)
        
        # Sort by popularity score
        top_agents = df.sort_values(by='popularity_score', ascending=False)
        
        # Display agent cards in rows of 3
        for i in range(0, len(top_agents), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(top_agents):
                    agent = top_agents.iloc[i + j]
                    with cols[j]:
                        st.markdown(
                            f"""
                            <div class="agent-card">
                                <h3 style="color: #FFD700;">{agent['name']}</h3>
                                <p><strong>Category:</strong> {agent['category']}</p>
                                <p>{agent['description']}</p>
                                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                                    <div>
                                        <p style="margin: 0;"><strong>Popularity:</strong> {agent['popularity_score']}/100</p>
                                        <p style="margin: 0;"><strong>Rating:</strong> {agent['avg_rating']}/5.0</p>
                                    </div>
                                    <div>
                                        <p style="margin: 0;"><strong>Users:</strong> {format_number(agent['monthly_active_users'])}</p>
                                        <p style="margin: 0;"><strong>Pricing:</strong> {agent['pricing']}</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        
        # Agent capabilities table
        st.markdown('<h2 class="gold-header">Agent Capabilities</h2>', unsafe_allow_html=True)
        
        # Create a table with agent capabilities
        capabilities_data = []
        for _, agent in df.iterrows():
            capabilities_dict = {
                'Agent': agent['name'],
                'Category': agent['category'],
                'Use Cases': ', '.join(agent['use_cases']),
                'Capabilities': ', '.join(agent['capabilities']),
                'API Available': 'Yes' if agent['api_access'] else 'No',
                'Rating': f"{agent['avg_rating']}/5.0"
            }
            capabilities_data.append(capabilities_dict)
        
        capabilities_df = pd.DataFrame(capabilities_data)
        st.dataframe(
            capabilities_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )
    
    with tab2:
        # Popularity analysis
        st.markdown('<h2 class="gold-header">Agent Popularity Analysis</h2>', unsafe_allow_html=True)
        
        # Create a bar chart of popularity scores
        fig_bar = px.bar(
            df.sort_values('popularity_score', ascending=False),
            x='name',
            y='popularity_score',
            color='category',
            title='AI Agent Popularity Scores',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        
        fig_bar.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis_title="Agent",
            yaxis_title="Popularity Score (0-100)",
            margin=dict(l=10, r=10, t=50, b=10),
            height=400,
            xaxis={
                'categoryorder': 'total descending',
                'gridcolor': 'rgba(255, 215, 0, 0.1)'
            },
            yaxis={
                'gridcolor': 'rgba(255, 215, 0, 0.1)'
            },
            title={
                'text': "AI Agent Popularity Scores",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 18}
            }
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Create a scatter plot of popularity vs. active users
        fig_scatter = px.scatter(
            df,
            x='popularity_score',
            y='monthly_active_users',
            size='avg_rating',
            color='category',
            hover_name='name',
            text='name',
            title='Popularity vs. Monthly Active Users',
            color_discrete_sequence=px.colors.sequential.Plasma,
            size_max=25
        )
        
        fig_scatter.update_traces(
            textposition='top center',
            marker=dict(line=dict(width=1, color='#FFD700'))
        )
        
        fig_scatter.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis_title="Popularity Score",
            yaxis_title="Monthly Active Users",
            margin=dict(l=10, r=10, t=50, b=10),
            height=500,
            xaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
            ),
            yaxis=dict(
                gridcolor='rgba(255, 215, 0, 0.1)',
                type='log'  # Log scale for better visualization of differences
            ),
            title={
                'text': "Popularity vs. Monthly Active Users",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 18}
            }
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Category distribution
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig_pie = px.pie(
            category_counts,
            values='Count',
            names='Category',
            title='Agent Categories Distribution',
            color_discrete_sequence=px.colors.sequential.Plasma,
            hole=0.4
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#0A0A0A', width=2))
        )
        
        fig_pie.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=10, r=10, t=50, b=10),
            height=400,
            title={
                'text': "Agent Categories Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#FFD700', 'size': 18}
            }
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab3:
        # AI Timeline view
        st.markdown('<h2 class="gold-header">AI Agents Timeline</h2>', unsafe_allow_html=True)
        
        # Sort by release date
        timeline_df = df.sort_values(by='release_date')
        
        # Display timeline items
        st.markdown('<div style="padding-left: 20px; position: relative;">', unsafe_allow_html=True)
        
        for _, agent in timeline_df.iterrows():
            release_date = agent['release_date'].strftime('%B %d, %Y')
            last_updated = agent['last_updated'].strftime('%B %d, %Y')
            
            # Calculate days since last update
            days_since_update = (datetime.now() - agent['last_updated']).days
            update_status = "Recently updated" if days_since_update < 30 else f"Last updated {days_since_update} days ago"
            
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-date">{release_date}</div>
                    <h3 style="margin: 5px 0;">{agent['name']}</h3>
                    <p>{agent['description']}</p>
                    <div class="timeline-content">
                        <p><strong>Category:</strong> {agent['category']}</p>
                        <p><strong>Popularity:</strong> {agent['popularity_score']}/100</p>
                        <p><strong>Status:</strong> {update_status}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_ai_agents()