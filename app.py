import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    layout="wide",
    page_title="Workfix Leak Detector",
    initial_sidebar_state="expanded"
)

# CSS for dark theme and alarming aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stSidebar {
        background-color: #161b22;
        color: #c9d1d9;
    }
    .metric-card {
        background-color: #161b22;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #30363d;
    }
    .red-text {
        color: #f85149;
        font-weight: bold;
    }
    .green-text {
        color: #56d364;
        font-weight: bold;
    }
    .yellow-text {
        color: #d29922;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .header-title {
        font-size: 2.5rem;
        color: #f85149;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-value {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #f85149;
    }
    .metric-label {
        text-align: center;
        color: #8b949e;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def generate_mock_comment_data():
    """Generate realistic mock comment data"""
    intents = [
        "price?", "how do I join?", "interested", "sent a DM", "tell me more",
        "how much?", "sign me up", "what's the cost?", "I want this", 
        "can you help me?", "ready to buy", "how does it work?",
        "pricing details", "where do I start?", "need this now",
        "sounds good", "what's included?", "best price?", "ready to invest"
    ]
    
    users = [
        "mike_s", "sarah_b", "john_doe", "emma_w", "alex_r", "lisa_k",
        "david_m", "jessica_p", "ryan_t", "amy_c", "chris_l", "karen_h",
        "matt_j", "rachel_g", "kevin_b", "susan_f", "tom_w", "linda_v"
    ]
    
    comments = []
    for _ in range(random.randint(25, 40)):
        comment = {
            'user': random.choice(users),
            'comment': random.choice(intents),
            'time_ignored': f"{random.randint(1, 7)} Days ago",
            'potential_value': st.session_state.offer_price
        }
        comments.append(comment)
    
    return pd.DataFrame(comments)

def generate_mock_chart_data():
    """Generate mock data for the chart"""
    dates = [(datetime.now() - timedelta(days=x)).strftime('%m/%d') for x in range(7)]
    dates.reverse()
    
    # Generate comment volume (high) and replies (low)
    comment_volume = [random.randint(45, 85) for _ in range(7)]
    replies = [random.randint(2, 8) for _ in range(7)]
    
    return pd.DataFrame({
        'date': dates,
        'comments': comment_volume,
        'replies': replies
    })

def calculate_metrics():
    """Calculate audit metrics"""
    # Simulate missed leads count
    missed_leads = random.randint(15, 35)
    lost_revenue = missed_leads * st.session_state.offer_price
    
    # Calculate metrics
    avg_response_time = f"{random.randint(12, 24)} hours, {random.randint(15, 59)} mins"
    reply_rate = f"{random.randint(25, 35)}%"
    efficiency_score = random.choice(["D-", "D", "D+"])
    
    return {
        'missed_leads': missed_leads,
        'lost_revenue': lost_revenue,
        'avg_response_time': avg_response_time,
        'reply_rate': reply_rate,
        'efficiency_score': efficiency_score
    }

def render_dashboard():
    """Render the main dashboard"""
    if 'handle' not in st.session_state:
        st.error("Please run the audit first!")
        return
    
    metrics = calculate_metrics()
    
    # Header
    st.markdown(f'<div class="header-title">AUDIT RESULTS FOR @{st.session_state.handle}</div>', unsafe_allow_html=True)
    
    # Section A: The "Bleeding Neck" Header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">', unsafe_allow_html=True)
        st.markdown(f'${metrics["lost_revenue"]:,}')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">ESTIMATED LOST REVENUE (Last 30 Days)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">', unsafe_allow_html=True)
        st.markdown(f'{metrics["missed_leads"]}')
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">MISSED HIGH-INTENT LEADS</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section B: The Metrics Row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="red-text metric-value">{metrics["avg_response_time"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">AVERAGE RESPONSE TIME</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="red-text metric-value">{metrics["reply_rate"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">REPLY RATE ON SALES COMMENTS</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="red-text metric-value">{metrics["efficiency_score"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">WORKFIX EFFICIENCY SCORE</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section C: Visual Evidence (The Chart)
    st.markdown('<h3>Comment Volume vs. Brand Replies (Last 7 Days)</h3>', unsafe_allow_html=True)
    
    chart_data = generate_mock_chart_data()
    
    fig = go.Figure(data=[
        go.Bar(name='Comments Received', x=chart_data['date'], y=chart_data['comments'], 
               marker_color='#f85149', opacity=0.7),
        go.Bar(name='Replies Sent', x=chart_data['date'], y=chart_data['replies'], 
               marker_color='#56d364', opacity=0.7)
    ])
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='#0d1117',
        paper_bgcolor='#0d1117',
        font_color='#c9d1d9',
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section D: The "Wall of Shame"
    st.markdown('<h3>Recent Unanswered High-Intent Comments</h3>', unsafe_allow_html=True)
    
    comments_df = generate_mock_comment_data()
    comments_df = comments_df.head(10)  # Show top 10
    
    # Format the dataframe for display
    st.dataframe(
        comments_df,
        column_config={
            "user": "User",
            "comment": "Comment Snippet",
            "time_ignored": "Time Ignored",
            "potential_value": st.column_config.NumberColumn(
                "Potential Value",
                format="$%d"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

def main():
    # Sidebar
    with st.sidebar:
        st.title("Workfix Leak Detector")
        st.markdown("---")
        
        handle = st.text_input("Target Instagram Handle", value="alexhormozi")
        offer_price = st.number_input(
            "Average High-Ticket Offer Price ($)", 
            min_value=500, 
            max_value=10000, 
            value=3000, 
            step=500
        )
        
        if st.button("🚨 RUN LEAK AUDIT", type="primary", use_container_width=True):
            # Store values in session state
            st.session_state.handle = handle.replace('@', '')
            st.session_state.offer_price = offer_price
            
            # Show loading spinner
            with st.spinner("Scanning last 50 posts... Analyzing comment intent... Calculating lost revenue..."):
                time.sleep(3)  # Simulate processing time
    
    # Main page
    if 'handle' in st.session_state:
        render_dashboard()
    else:
        st.markdown('<div class="sub-header">Enter Instagram handle and offer price, then click "RUN LEAK AUDIT" to begin analysis</div>', unsafe_allow_html=True)
        
        # Show example metrics to demonstrate the tool
        st.markdown('<h3>Example Audit Results</h3>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value" style="color: #f85149;">$75,000</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">ESTIMATED LOST REVENUE (Last 30 Days)</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value" style="color: #f85149;">25</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">MISSED HIGH-INTENT LEADS</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
