import streamlit as st

def render_futuristic_header():
    """Render a futuristic, animated header for the app"""
    
    # CSS for glowing text effect and animation with gold theme
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7), 0 0 20px rgba(255, 215, 0, 0.5), 0 0 30px rgba(255, 215, 0, 0.3); }
        50% { text-shadow: 0 0 15px rgba(255, 215, 0, 0.9), 0 0 25px rgba(255, 215, 0, 0.7), 0 0 35px rgba(255, 215, 0, 0.5); }
        100% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.7), 0 0 20px rgba(255, 215, 0, 0.5), 0 0 30px rgba(255, 215, 0, 0.3); }
    }
    
    @keyframes shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 100% 0; }
    }
    
    .neon-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
        color: white;
        animation: pulse 2s infinite;
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #FFD700, #A67C00, #FFD700);
        background-size: 200% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: shimmer 3s infinite linear;
    }
    
    .hero-container {
        background: rgba(26, 26, 26, 0.5);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
    }
    
    .moving-background {
        position: relative;
        overflow: hidden;
    }
    
    .moving-background:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 10% 20%, rgba(255, 215, 0, 0.03) 0%, transparent 20%),
            radial-gradient(circle at 90% 50%, rgba(255, 215, 0, 0.03) 0%, transparent 25%),
            radial-gradient(circle at 30% 80%, rgba(255, 215, 0, 0.03) 0%, transparent 20%);
        z-index: -1;
        animation: move-bg 15s linear infinite;
    }
    
    @keyframes move-bg {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    
    .subtitle {
        font-size: 1.3rem !important;
        opacity: 0.9;
        margin-top: 0 !important;
        color: #A0A0A0;
    }
    
    .description {
        line-height: 1.6;
        max-width: 90%;
        margin: 15px auto;
    }
    
    .datapoint {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Card hover effects */
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(255, 215, 0, 0.15);
        transition: all 0.3s ease-in-out;
    }
    
    /* Glow around metrics */
    .metric-container {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .metric-container:after {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        z-index: -1;
        border-radius: 10px;
        background: linear-gradient(45deg, #FFD700, transparent, #A67C00);
        animation: rotate 3s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Futuristic header with animation
    st.markdown('<div class="hero-container moving-background">', unsafe_allow_html=True)
    
    # Logo and title
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image("assets/logo.svg", width=120)
    
    with col2:
        st.markdown('<h1 class="neon-title">M<span class="gradient-text">100</span>D</h1>', unsafe_allow_html=True)
        st.markdown('<h3 class="subtitle">AI Token Analytics Platform</h3>', unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <p class="description">
    As the AI token landscape rapidly expands, it's becoming increasingly difficult to distinguish signal from noise. 
    Many projects lack transparency, technical clarity, or even basic legitimacy. 
    M100D is here to change that. We're building a comprehensive, open analytics platform 
    that brings structure and insight to the AI token ecosystem. 
    Our mission is to make this space understandable, credible, and accessible to all.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_animated_metric(label, value, delta=None, color="gold"):
    """Render a metric with glow animation"""
    
    delta_html = ""
    if delta is not None:
        is_positive = delta >= 0
        delta_color = "#00FF9E" if is_positive else "#FF3D71"  # Green for positive, red for negative
        delta_arrow = "↑" if is_positive else "↓"
        delta_html = f'<span style="color: {delta_color}; font-size: 0.8rem">{delta_arrow} {abs(delta)}</span>'
    
    color_map = {
        "gold": "#FFD700",  # Gold for primary
        "amber": "#FFC107",  # Amber for secondary
        "green": "#00FF9E",  # Green for positive changes
        "red": "#FF3D71",    # Red for negative changes
        "blue": "#4285F4"    # Blue accent
    }
    
    glow_color = color_map.get(color, "#FFD700")  # Default to gold if color not found
    
    html = f"""
    <div class="metric-container datapoint" style="background: rgba(26, 26, 26, 0.6); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(255, 215, 0, 0.1);">
        <div style="font-size: 0.9rem; color: #A0A0A0; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: {glow_color}; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);">{value} {delta_html}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_card(title, content, color="gold", icon=None):
    """Render a card with hover effects"""
    
    color_map = {
        "gold": "#FFD700",    # Gold for primary
        "amber": "#FFC107",   # Amber for secondary
        "green": "#00FF9E",   # Green for positive changes
        "red": "#FF3D71",     # Red for negative changes
        "blue": "#4285F4"     # Blue accent
    }
    
    card_color = color_map.get(color, "#FFD700")
    icon_html = f'<span style="margin-right: 5px;">{icon}</span>' if icon else ''
    
    html = f"""
    <div class="card-container datapoint" style="background: rgba(26, 26, 26, 0.6); 
         border-left: 3px solid {card_color}; padding: 18px; border-radius: 8px; 
         margin-bottom: 18px; transition: all 0.3s ease; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 12px; 
             color: {card_color}; letter-spacing: 0.5px;">{icon_html}{title}</div>
        <div style="color: #E0E0E0;">{content}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_data_cluster():
    """Render a dynamic data point cluster animation"""
    
    st.markdown("""
    <style>
    .data-cluster {
        position: relative;
        height: 220px;
        background: rgba(10, 10, 10, 0.5);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 215, 0, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .data-point {
        position: absolute;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 215, 0, 0.8);
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    .connection {
        position: absolute;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.5), rgba(166, 124, 0, 0.5));
        height: 1px;
        transform-origin: left center;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0); }
        50% { transform: translate(var(--tx), var(--ty)); }
        100% { transform: translate(0, 0); }
    }
    </style>
    
    <div class="data-cluster" id="dataCluster">
        <div class="data-point" style="top: 50%; left: 50%; --tx: 10px; --ty: -15px; animation: float 8s infinite;"></div>
        <div class="data-point" style="top: 30%; left: 20%; --tx: -5px; --ty: 10px; animation: float 10s infinite;"></div>
        <div class="data-point" style="top: 70%; left: 30%; --tx: 15px; --ty: 5px; animation: float 12s infinite;"></div>
        <div class="data-point" style="top: 20%; left: 80%; --tx: -10px; --ty: -10px; animation: float 9s infinite;"></div>
        <div class="data-point" style="top: 80%; left: 70%; --tx: 5px; --ty: -15px; animation: float 11s infinite;"></div>
        <div class="data-point" style="top: 40%; left: 60%; --tx: -15px; --ty: 5px; animation: float 13s infinite;"></div>
        <div class="data-point" style="top: 60%; left: 40%; --tx: 10px; --ty: 10px; animation: float 14s infinite;"></div>
        <div class="data-point" style="top: 35%; left: 90%; --tx: -5px; --ty: -5px; animation: float 9s infinite;"></div>
        <div class="data-point" style="top: 85%; left: 15%; --tx: 10px; --ty: -10px; animation: float 12s infinite;"></div>
        <div class="data-point" style="top: 25%; left: 40%; --tx: -8px; --ty: 12px; animation: float 10s infinite;"></div>
        <!-- Pre-rendered connections -->
        <div class="connection" style="top: 50%; left: 50%; width: 30%; transform: rotate(45deg);"></div>
        <div class="connection" style="top: 30%; left: 20%; width: 40%; transform: rotate(15deg);"></div>
        <div class="connection" style="top: 70%; left: 30%; width: 45%; transform: rotate(-15deg);"></div>
        <div class="connection" style="top: 40%; left: 60%; width: 25%; transform: rotate(-30deg);"></div>
        <div class="connection" style="top: 60%; left: 40%; width: 35%; transform: rotate(30deg);"></div>
    </div>
    """, unsafe_allow_html=True)

def render_ai_token_visualization():
    """Render a dynamic visualization of AI tokens"""
    
    st.markdown("""
    <style>
    .token-cosmos {
        position: relative;
        height: 300px;
        background: linear-gradient(180deg, rgba(10, 10, 10, 1) 0%, rgba(26, 26, 26, 0.5) 100%);
        border-radius: 10px;
        overflow: hidden;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .token {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,215,0,0.4) 70%, transparent 100%);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }
    
    .token-center {
        position: absolute;
        top: 50%;
        left: 50%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,215,0,0.6) 70%, transparent 100%);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        animation: pulse-size 4s infinite ease-in-out;
        z-index: 10;
        transform: translate(-50%, -50%);
        width: 40px;
        height: 40px;
    }
    
    .token-orbit {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 20px;
        height: 20px;
        margin-top: -10px;
        margin-left: -10px;
        animation-duration: 20s;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }
    
    .orbit-1 { animation-name: orbit1; }
    .orbit-2 { animation-name: orbit2; animation-duration: 25s; width: 24px; height: 24px; margin-top: -12px; margin-left: -12px; animation-direction: reverse; }
    .orbit-3 { animation-name: orbit3; animation-duration: 30s; width: 16px; height: 16px; margin-top: -8px; margin-left: -8px; }
    .orbit-4 { animation-name: orbit4; animation-duration: 15s; width: 18px; height: 18px; margin-top: -9px; margin-left: -9px; animation-direction: reverse; }
    .orbit-5 { animation-name: orbit5; animation-duration: 22s; width: 14px; height: 14px; margin-top: -7px; margin-left: -7px; }
    .orbit-6 { animation-name: orbit6; animation-duration: 27s; width: 22px; height: 22px; margin-top: -11px; margin-left: -11px; animation-direction: reverse; }
    
    @keyframes orbit1 {
        0% { transform: rotate(0deg) translateX(80px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(80px) rotate(-360deg); }
    }
    
    @keyframes orbit2 {
        0% { transform: rotate(0deg) translateX(110px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(110px) rotate(-360deg); }
    }
    
    @keyframes orbit3 {
        0% { transform: rotate(0deg) translateX(140px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(140px) rotate(-360deg); }
    }
    
    @keyframes orbit4 {
        0% { transform: rotate(0deg) translateX(60px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(60px) rotate(-360deg); }
    }
    
    @keyframes orbit5 {
        0% { transform: rotate(0deg) translateX(100px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(100px) rotate(-360deg); }
    }
    
    @keyframes orbit6 {
        0% { transform: rotate(0deg) translateX(120px) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(120px) rotate(-360deg); }
    }
    
    @keyframes pulse-size {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.8; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
    
    .token-name {
        position: absolute;
        color: #FFD700;
        font-size: 10px;
        white-space: nowrap;
        pointer-events: none;
        text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
    }
    </style>
    
    <div class="token-cosmos">
        <!-- Central node - represents the AI sector -->
        <div class="token-center"></div>
        <div class="token-name" style="top: calc(50% + 25px); left: 50%; transform: translateX(-50%);">AI Sector</div>
        
        <!-- Orbiting tokens - different sizes, speeds and distances -->
        <div class="token token-orbit orbit-1"></div>
        <div class="token-name" style="top: calc(50% - 90px); left: 50%; transform: translateX(-50%);">Neural</div>
        
        <div class="token token-orbit orbit-2"></div>
        <div class="token-name" style="top: calc(50% + 120px); left: 50%; transform: translateX(-50%);">DeepAI</div>
        
        <div class="token token-orbit orbit-3"></div>
        <div class="token-name" style="top: calc(50%); left: calc(50% - 150px);">Synapse</div>
        
        <div class="token token-orbit orbit-4"></div>
        <div class="token-name" style="top: calc(50%); left: calc(50% + 70px);">Cortex</div>
        
        <div class="token token-orbit orbit-5"></div>
        <div class="token-name" style="top: calc(50% - 60px); left: calc(50% + 100px);">BrainDAO</div>
        
        <div class="token token-orbit orbit-6"></div>
        <div class="token-name" style="top: calc(50% + 70px); left: calc(50% - 120px);">GPT Chain</div>
    </div>
    """, unsafe_allow_html=True)