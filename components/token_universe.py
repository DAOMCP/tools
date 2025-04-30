import streamlit as st

def render_token_universe():
    """
    Renders the AI Token Universe visualization with animated orbiting tokens.
    This component can be imported and used in the main app.py.
    """
    st.markdown('<h2 style="color: #00E4FF; font-weight: 600; letter-spacing: 1px; border-bottom: 1px solid rgba(0, 228, 255, 0.2); padding-bottom: 10px; margin-bottom: 20px;">AI Token Universe</h2>', unsafe_allow_html=True)
    
    # Enhanced AI Token Visualization with explanation text
    st.markdown("""
    <div style="background-color: rgba(0, 228, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <p style="margin-bottom: 10px;">The AI Token Universe represents the evolving ecosystem of AI-related cryptocurrency tokens. 
        The visualization illustrates relationships, relative market sizes, and positioning within the broader AI technology landscape.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rendered with custom styling to ensure it appears properly
    st.markdown("""
    <style>
    .token-cosmos {
        position: relative;
        height: 300px;
        background: linear-gradient(180deg, rgba(10, 17, 40, 1) 0%, rgba(26, 33, 81, 0.5) 100%);
        border-radius: 10px;
        overflow: hidden;
        margin: 20px 0;
        border: 1px solid rgba(0, 228, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .token {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(0,228,255,0.4) 70%, transparent 100%);
        transform-origin: center center;
        box-shadow: 0 0 15px rgba(0, 228, 255, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #0A1128;
        font-size: 0.7rem;
    }
    
    .token-lg {
        background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(0,228,255,0.6) 70%, transparent 100%);
        box-shadow: 0 0 20px rgba(0, 228, 255, 0.8);
        animation: pulse-size 4s infinite ease-in-out;
        z-index: 10;
    }
    
    .token-sm {
        z-index: 5;
    }
    
    @keyframes orbit {
        0% { transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg); }
        100% { transform: rotate(360deg) translateX(var(--orbit-radius)) rotate(-360deg); }
    }
    
    @keyframes orbit-reverse {
        0% { transform: rotate(0deg) translateX(var(--orbit-radius)) rotate(0deg); }
        100% { transform: rotate(-360deg) translateX(var(--orbit-radius)) rotate(360deg); }
    }
    
    @keyframes pulse-size {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .orbit-line {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 1px dashed rgba(0, 228, 255, 0.2);
        border-radius: 50%;
    }
    
    .token-name {
        position: absolute;
        color: #00E4FF;
        font-size: 0.7rem;
        white-space: nowrap;
        text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
    }
    </style>
    
    <div class="token-cosmos">
        <!-- Orbit circles -->
        <div class="orbit-line" style="width: 120px; height: 120px;"></div>
        <div class="orbit-line" style="width: 200px; height: 200px;"></div>
        <div class="orbit-line" style="width: 280px; height: 280px;"></div>
        
        <!-- Central node - represents the AI sector -->
        <div class="token token-lg" style="top: 50%; left: 50%; width: 50px; height: 50px; margin-top: -25px; margin-left: -25px;">AI</div>
        
        <!-- Orbiting tokens - major market cap tokens -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 30px; height: 30px; margin-top: -15px; margin-left: -15px; 
                     --orbit-radius: 60px; animation: orbit 20s infinite linear;">FET</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 34px; height: 34px; margin-top: -17px; margin-left: -17px; 
                     --orbit-radius: 100px; animation: orbit-reverse 25s infinite linear;">AGIX</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 24px; height: 24px; margin-top: -12px; margin-left: -12px; 
                     --orbit-radius: 140px; animation: orbit 30s infinite linear;">RNDR</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 22px; height: 22px; margin-top: -11px; margin-left: -11px; 
                     --orbit-radius: 80px; animation: orbit-reverse 18s infinite linear;">OCEAN</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 26px; height: 26px; margin-top: -13px; margin-left: -13px; 
                     --orbit-radius: 120px; animation: orbit 22s infinite linear;">GRT</div>
        
        <div class="token token-sm" style="top: 50%; left: 50%; width: 20px; height: 20px; margin-top: -10px; margin-left: -10px; 
                     --orbit-radius: 90px; animation: orbit-reverse 27s infinite linear;">NMR</div>
        
        <!-- Second ring -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 18px; height: 18px; margin-top: -9px; margin-left: -9px; 
                     --orbit-radius: 130px; animation: orbit 24s infinite linear;">ICP</div>
                     
        <div class="token token-sm" style="top: 50%; left: 50%; width: 16px; height: 16px; margin-top: -8px; margin-left: -8px; 
                     --orbit-radius: 120px; animation: orbit-reverse 28s infinite linear;">CHR</div>
                     
        <!-- Outer ring - smaller tokens -->
        <div class="token token-sm" style="top: 50%; left: 50%; width: 14px; height: 14px; margin-top: -7px; margin-left: -7px; 
                     --orbit-radius: 140px; animation: orbit 32s infinite linear;">ALI</div>
                     
        <div class="token token-sm" style="top: 50%; left: 50%; width: 16px; height: 16px; margin-top: -8px; margin-left: -8px; 
                     --orbit-radius: 110px; animation: orbit-reverse 29s infinite linear;">CQT</div>
    </div>
    """, unsafe_allow_html=True)
