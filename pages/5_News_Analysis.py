import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.web_scraper import scrape_ai_crypto_news, analyze_news_sentiment
from components.animations import render_animated_metric, render_card

st.set_page_config(
    page_title="M100D - News Analysis",
    page_icon="📰",
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
    
    /* News item styling */
    .news-item {
        background-color: rgba(26, 26, 26, 0.8);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 3px solid #FFD700;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        background-color: rgba(35, 35, 35, 0.8);
        transform: translateY(-2px);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
    }
    
    .news-date {
        color: #A0A0A0;
        font-size: 0.8rem;
    }
    
    .news-headline {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 8px 0;
        color: #FFFFFF;
    }
    
    .news-snippet {
        color: #D0D0D0;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .news-source {
        color: #A0A0A0;
        font-size: 0.8rem;
        text-align: right;
    }
    
    .token-tag {
        display: inline-block;
        background-color: rgba(255, 215, 0, 0.2);
        border-radius: 4px;
        padding: 2px 6px;
        margin-right: 6px;
        font-size: 0.8rem;
        color: #FFD700;
    }
    
    .positive {
        border-left-color: #00FF9E;
    }
    
    .negative {
        border-left-color: #FF3D71;
    }
    
    .neutral {
        border-left-color: #4285F4;
    }
</style>
""", unsafe_allow_html=True)

def render_news_analysis():
    st.markdown('<h1 class="gold-header">AI Crypto News Analysis</h1>', unsafe_allow_html=True)
    
    # Create loading spinner while fetching news data
    with st.spinner("Analyzing recent AI crypto news..."):
        # Fetch AI crypto news
        news_df = scrape_ai_crypto_news()
        
        # Analyze news sentiment
        sentiment_data = analyze_news_sentiment(news_df)
    
    if news_df.empty:
        st.error("No news data available. Please check your internet connection or try again later.")
        return
    
    # Create a layout for the dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_sentiment = sentiment_data['avg_sentiment']
        sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
        sentiment_color = "green" if avg_sentiment > 0.1 else "red" if avg_sentiment < -0.1 else "amber"
        
        render_animated_metric("Average Sentiment", f"{sentiment_label} ({avg_sentiment:.2f})", color=sentiment_color)
    
    with col2:
        render_animated_metric("Positive News", f"{sentiment_data['positive_news_count']} articles", color="green")
    
    with col3:
        render_animated_metric("Negative News", f"{sentiment_data['negative_news_count']} articles", color="red")
    
    # Create dashboard tabs
    tab1, tab2 = st.tabs(["Sentiment Trends", "News Feed"])
    
    with tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FFD700;">AI Crypto News Sentiment Trends</h3>', unsafe_allow_html=True)
        
        # Create sentiment trend visualization
        if sentiment_data['sentiment_by_date']:
            sentiment_df = pd.DataFrame(sentiment_data['sentiment_by_date'])
            
            # Create a area chart of sentiment over time
            fig_area = px.area(
                sentiment_df,
                x='date_day',
                y='sentiment',
                title='AI Crypto News Sentiment Over Time',
                labels={'date_day': 'Date', 'sentiment': 'Average Sentiment'}
            )
            
            # Custom color for fill based on sentiment values
            fig_area.update_traces(
                line=dict(color='#FFD700', width=2),
                fillcolor='rgba(255, 215, 0, 0.1)',
                hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
            )
            
            fig_area.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Date",
                yaxis_title="Sentiment Score",
                hovermode="x unified",
                margin=dict(l=10, r=10, t=50, b=10),
                height=400,
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    range=[-1, 1]
                ),
                title={
                    'text': "AI Crypto News Sentiment Over Time",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            # Add a horizontal line at 0 (neutral sentiment)
            fig_area.add_hline(
                y=0, 
                line_dash="dash", 
                line_color="#FFFFFF",
                annotation_text="Neutral",
                annotation_position="right",
                annotation_font_color="#FFFFFF"
            )
            
            st.plotly_chart(fig_area, use_container_width=True)
            
            # Distribution of sentiment
            sentiment_hist = px.histogram(
                news_df,
                x='sentiment',
                nbins=20,
                title='Distribution of News Sentiment',
                color_discrete_sequence=['#FFD700'],
                labels={'sentiment': 'Sentiment Score', 'count': 'Number of Articles'}
            )
            
            sentiment_hist.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Sentiment Score",
                yaxis_title="Number of Articles",
                margin=dict(l=10, r=10, t=50, b=10),
                height=300,
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    range=[-1, 1]
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                title={
                    'text': "Distribution of News Sentiment",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                }
            )
            
            # Add a vertical line at 0 (neutral sentiment)
            sentiment_hist.add_vline(
                x=0, 
                line_dash="dash", 
                line_color="#FFFFFF",
                annotation_text="Neutral",
                annotation_position="top",
                annotation_font_color="#FFFFFF"
            )
            
            st.plotly_chart(sentiment_hist, use_container_width=True)
        else:
            st.info("Not enough data to generate sentiment trends")
        
        # Trending tokens based on news mentions
        if sentiment_data['trending_tokens']:
            st.markdown('<h3 style="color: #FFD700;">Trending AI Tokens in News</h3>', unsafe_allow_html=True)
            
            trending_df = pd.DataFrame(sentiment_data['trending_tokens'])
            
            # Create a horizontal bar chart
            fig_bar = px.bar(
                trending_df,
                y='token',
                x='mentions',
                orientation='h',
                title='Most Mentioned AI Tokens in Recent News',
                color='mentions',
                color_continuous_scale='Viridis',
                labels={'token': 'Token', 'mentions': 'Number of Mentions'}
            )
            
            fig_bar.update_layout(
                template="plotly_dark",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title="Number of Mentions",
                yaxis_title="Token Name",
                margin=dict(l=10, r=10, t=50, b=10),
                height=350,
                xaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255, 215, 0, 0.1)',
                    linecolor='rgba(255, 215, 0, 0.5)',
                    categoryorder='total ascending'
                ),
                title={
                    'text': "Most Mentioned AI Tokens in Recent News",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': '#FFD700', 'size': 18}
                },
                coloraxis_colorbar=dict(
                    title="Mentions",
                    titleside="right",
                    titlefont=dict(color="#FFD700"),
                    tickfont=dict(color="#FFD700")
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FFD700;">Recent AI Crypto News</h3>', unsafe_allow_html=True)
        
        # Add a filter for sentiment
        col1, col2 = st.columns([3, 1])
        with col2:
            sentiment_filter = st.selectbox(
                "Filter by sentiment",
                ["All", "Positive", "Neutral", "Negative"]
            )
        
        # Filter news based on sentiment
        filtered_news = news_df
        if sentiment_filter == "Positive":
            filtered_news = news_df[news_df['sentiment'] > 0.1]
        elif sentiment_filter == "Negative":
            filtered_news = news_df[news_df['sentiment'] < -0.1]
        elif sentiment_filter == "Neutral":
            filtered_news = news_df[(news_df['sentiment'] >= -0.1) & (news_df['sentiment'] <= 0.1)]
        
        if filtered_news.empty:
            st.info(f"No {sentiment_filter.lower()} news articles found.")
        else:
            # Display news items
            for _, article in filtered_news.iterrows():
                # Determine the sentiment class
                sentiment_class = ""
                if article['sentiment'] > 0.1:
                    sentiment_class = "positive"
                elif article['sentiment'] < -0.1:
                    sentiment_class = "negative"
                else:
                    sentiment_class = "neutral"
                
                # Format date
                date_str = article['date'].strftime("%b %d, %Y • %I:%M %p")
                
                # Create tags for related tokens
                token_tags = ""
                for token in article['related_tokens']:
                    token_tags += f'<span class="token-tag">{token}</span>'
                
                # Source display
                source_display = article['source'].replace("https://", "").split("/")[0]
                
                # Create the news item HTML
                news_html = f"""
                <div class="news-item {sentiment_class}">
                    <div class="news-date">{date_str}</div>
                    <div class="news-headline">{article['headline']}</div>
                    <div class="news-snippet">{article['snippet']}</div>
                    <div>{token_tags}</div>
                    <div class="news-source">Source: {source_display}</div>
                </div>
                """
                
                st.markdown(news_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Execute the main function
if __name__ == "__main__":
    render_news_analysis()