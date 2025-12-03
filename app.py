import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import instaloader
from datetime import datetime
import time

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Workfix Live Auditor")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main { background-color: #0E1117; color: #FAFAFA; }
    .metric-card {
        background-color: #262730;
        border: 1px solid #41424C;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .big-number { font-size: 3em; font-weight: bold; color: #FF4B4B; }
    .label { font-size: 1em; color: #A3A8B8; }
    .stButton>button { width: 100%; background-color: #FF4B4B; color: white; border: none; }
</style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---

def analyze_instagram(username, offer_price):
    """
    Connects to Instagram via Instaloader to fetch REAL data.
    Note: This works best locally. Cloud IPs may be blocked.
    """
    L = instaloader.Instaloader()
    
    # Optional: Load session if you have one (uncomment if running locally with login)
    # L.load_session_from_file('your_username') 

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # 1. Basic Profile Info
        data = {
            "username": profile.username,
            "followers": profile.followers,
            "bio": profile.biography,
            "url": profile.external_url,
            "pic": profile.profile_pic_url,
            "is_verified": profile.is_verified
        }

        # 2. Analyze Last 5 Posts
        posts_data = []
        total_comments = 0
        total_likes = 0
        
        # We only grab the last 5 to avoid Rate Limits
        for post in profile.get_posts():
            if len(posts_data) >= 5:
                break
            
            posts_data.append({
                "date": post.date_local,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption[:50] + "..." if post.caption else "No Caption"
            })
            total_comments += post.comments
            total_likes += post.likes
            time.sleep(1) # Sleep to be nice to API

        # 3. Calculate "Leak" Metrics
        # Industry Benchmark: ~20% of comments on coaching pages are "Intent" (Leads)
        estimated_leads = int(total_comments * 0.20)
        potential_revenue = estimated_leads * offer_price

        stats = {
            "total_likes_last_5": total_likes,
            "total_comments_last_5": total_comments,
            "avg_engagement": (total_likes + total_comments) / 5,
            "estimated_leads": estimated_leads,
            "potential_revenue": potential_revenue
        }
        
        return data, posts_data, stats

    except instaloader.ProfileNotExistsException:
        st.error(f"❌ User @{username} not found.")
        return None, None, None
    except instaloader.ConnectionException as e:
        st.error(f"⚠️ Connection Refused by Instagram. Try running this Locally. Error: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
        return None, None, None

# --- MAIN APP LAYOUT ---

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=50)
        st.title("Workfix Audit")
        target_user = st.text_input("Target Username", placeholder="alexhormozi")
        offer_val = st.number_input("High Ticket Offer Value ($)", value=3000, step=500)
        
        run_btn = st.button("RUN LIVE AUDIT")
        st.info("ℹ️ Scans last 5 posts for engagement leaks.")

    # Main Area
    if run_btn and target_user:
        with st.spinner(f"Connecting to Instagram servers... Analyzing @{target_user}..."):
            profile_data, posts, stats = analyze_instagram(target_user, offer_val)

        if profile_data:
            # Header Profile Section
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(profile_data['pic'], width=100)
            with col2:
                st.subheader(f"@{profile_data['username']} {'✅' if profile_data['is_verified'] else ''}")
                st.write(f"**Followers:** {profile_data['followers']:,} | **Bio:** {profile_data['bio']}")
            
            st.divider()

            # The "Leak" Dashboard
            st.markdown("### 🚨 LEAK DETECTION REPORT")
            m1, m2, m3 = st.columns(3)
            
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">MISSED COMMENTS (Last 5 Posts)</div>
                    <div class="big-number">{stats['total_comments_last_5']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">ESTIMATED LEADS IGNORED</div>
                    <div class="big-number">{stats['estimated_leads']}</div>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">POTENTIAL REVENUE LEAK</div>
                    <div class="big-number">${stats['potential_revenue']:,}</div>
                </div>
                """, unsafe_allow_html=True)

            # Visual Evidence
            st.markdown("### 📉 Engagement Breakdown")
            
            # Create Dataframe for Chart
            df = pd.DataFrame(posts)
            
            fig = go.Figure(data=[
                go.Bar(name='Likes', x=df['date'], y=df['likes'], marker_color='#333333'),
                go.Bar(name='Comments (Leads)', x=df['date'], y=df['comments'], marker_color='#FF4B4B')
            ])
            fig.update_layout(barmode='group', plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

            # The Call to Action
            st.success("✅ Audit Complete. Automated System Recommended.")

    else:
        # Empty State
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🕵️‍♂️ Instagram Leak Detector</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Enter a username to scan for missed high-ticket opportunities.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
