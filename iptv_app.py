import streamlit as st
import requests
from streamlit_player import st_player
import time
from datetime import datetime
import random

# Set up the page configuration with a theme
st.set_page_config(
    page_title="🌟 Premium IPTV Player",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with animations and modern design
custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Poppins', sans-serif;
        }
        
        .main-title {
            font-size: 3em;
            font-weight: 700;
            background: linear-gradient(45deg, #FF416C, #FF4B2B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 20px;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from {
                text-shadow: 0 0 10px #FF416C40;
            }
            to {
                text-shadow: 0 0 20px #FF4B2B40;
            }
        }
        
        .channel-stats {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .channel-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .channel-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, rgba(255,65,108,0.1), rgba(255,75,43,0.1));
        }
        
        .channel-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            transition: 0.5s;
        }
        
        .channel-card:hover::before {
            left: 100%;
        }
        
        .favorite-btn {
            position: absolute;
            right: 10px;
            top: 10px;
            color: #FF416C;
            cursor: pointer;
        }
        
        .player-wrapper {
            background: #0f0f0f;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 1064.44px; /* 1024.44 + 40px padding */
            margin-left: auto;
            margin-right: auto;
        }
        
        .player-container {
            position: relative;
            width: 1024.44px;
            height: 583.55px;
            background: #000000;
            border-radius: 8px;
            overflow: hidden;
            margin: 0 auto;
        }
        
        .player-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 1024.44px;
            height: 583.55px;
            border: none;
        }
        
        @media (max-width: 1124px) {  /* 1064.44px + 60px margin */
            .player-container, .player-container iframe {
                width: 100%;
                height: calc((100vw - 40px) * 0.57);
                max-width: 1024.44px;
                max-height: 583.55px;
            }
        }
        
        .video-info {
            padding: 20px;
        }
        
        .category-header {
            font-size: 1.5em;
            font-weight: 600;
            color: #FF416C;
            margin: 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,65,108,0.3);
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #FF416C, #FF4B2B);
            border-radius: 4px;
        }
        
        .video-title {
            color: #ffffff;
            font-size: 1.5em;
            font-weight: 600;
            margin: 15px 0;
            padding: 0 10px;
        }
        
        .video-stats {
            display: flex;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 15px;
        }
        
        .video-actions {
            background: #272727;
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
            display: flex;
            gap: 10px;
        }
        
        .action-button {
            background: #383838;
            border: none;
            border-radius: 18px;
            padding: 8px 16px;
            color: #ffffff;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.3s;
        }
        
        .action-button:hover {
            background: #4d4d4d;
        }
        
        .channel-info {
            display: flex;
            align-items: center;
            padding: 15px 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .channel-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #383838;
            margin-right: 12px;
        }
        
        .channel-details {
            flex-grow: 1;
        }
        
        .channel-name {
            color: #ffffff;
            font-weight: 500;
            margin-bottom: 4px;
        }
        
        .channel-stats {
            color: #aaaaaa;
            font-size: 0.9em;
        }
        
        /* Custom scrollbar for the player section */
        .player-wrapper::-webkit-scrollbar {
            width: 8px;
        }
        
        .player-wrapper::-webkit-scrollbar-track {
            background: #0f0f0f;
        }
        
        .player-wrapper::-webkit-scrollbar-thumb {
            background: #383838;
            border-radius: 4px;
        }
        
        .player-wrapper::-webkit-scrollbar-thumb:hover {
            background: #4d4d4d;
        }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()

# Initialize session state for watch history
if 'watch_history' not in st.session_state:
    st.session_state.watch_history = []

# Initialize session state for user preferences
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {
        'quality': 'Auto',
        'autoplay': True,
        'notifications': True
    }

# Sidebar enhancements
with st.sidebar:
    st.markdown("### 🎮 Player Controls")
    
    # Enhanced search with filters
    search_query = st.text_input("🔍 Search Channels")
    category_filter = st.multiselect("📺 Categories", 
                                   ["Sports", "News", "Entertainment", "Movies", "Music"])
    
    # Advanced playback controls
    st.markdown("### ⚙️ Playback Settings")
    volume = st.slider("🔊 Volume", 0, 100, 50)
    playback_speed = st.select_slider("⚡ Speed", 
                                    options=[0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0],
                                    value=1.0)
    
    # Quality selection
    quality = st.selectbox("🎥 Quality", ["Auto", "1080p", "720p", "480p", "360p"])
    
    # User preferences
    st.markdown("### 🛠️ Preferences")
    st.session_state.user_preferences['autoplay'] = st.checkbox("▶️ Autoplay", 
                                                              value=st.session_state.user_preferences['autoplay'])
    st.session_state.user_preferences['notifications'] = st.checkbox("🔔 Notifications", 
                                                                   value=st.session_state.user_preferences['notifications'])

# Main content area
st.markdown("<h1 class='main-title'>🌟 Premium IPTV Player</h1>", unsafe_allow_html=True)

# URLs for main, live, and additional stream playlists
MAIN_M3U_URL = "https://raw.githubusercontent.com/Arghayadasdev/World-IPTV-Channels/refs/heads/main/bloginstall-iptv.m3u"
LIVE_M3U_URL = "https://raw.githubusercontent.com/FunctionError/PiratesTv/main/combined_playlist.m3u"
STREAM_M3U_URL = "https://raw.githubusercontent.com/imdhiru/bloginstall-iptv/main/bloginstall-bangla.m3u"

# Load channels from M3U playlist with caching
@st.cache_data
def load_channels(url):
    channels = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                name = lines[i].split(",")[-1].strip()
                url = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if url.startswith("http"):
                    channels.append({"name": name, "url": url})
    except Exception as e:
        st.error(f"Error fetching channels from {url}: {e}")
    return channels

# Load all channel lists
main_channels = load_channels(MAIN_M3U_URL)
live_channels = load_channels(LIVE_M3U_URL)
stream_channels = load_channels(STREAM_M3U_URL)

# Channel Statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        "<div class='channel-stats'>"
        "<h3>📊 Total Channels</h3>"
        f"<h2>{len(main_channels) + len(live_channels) + len(stream_channels)}</h2>"
        "</div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='channel-stats'>"
        "<h3>⭐ Favorites</h3>"
        f"<h2>{len(st.session_state.favorites)}</h2>"
        "</div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        "<div class='channel-stats'>"
        "<h3>📺 Live Now</h3>"
        f"<h2>{random.randint(50, 200)}</h2>"
        "</div>",
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        "<div class='channel-stats'>"
        "<h3>👥 Active Users</h3>"
        f"<h2>{random.randint(100, 1000)}</h2>"
        "</div>",
        unsafe_allow_html=True
    )

# Filtering function
def filter_channels(channels, search_query):
    return [ch for ch in channels if search_query.lower() in ch["name"].lower()]

# Filtered channel lists based on search
filtered_main_channels = filter_channels(main_channels, search_query)
filtered_live_channels = filter_channels(live_channels, search_query)
filtered_stream_channels = filter_channels(stream_channels, search_query)

# Initialize session state for selected channel and visible channel counts
if 'selected_channel' not in st.session_state:
    st.session_state.selected_channel = None
    st.session_state.selected_channel_index = 0

# Initialize session state for displayed channels if not already set
if 'main_channel_display_limit' not in st.session_state:
    st.session_state.main_channel_display_limit = 10
if 'live_channel_display_limit' not in st.session_state:
    st.session_state.live_channel_display_limit = 10
if 'stream_channel_display_limit' not in st.session_state:
    st.session_state.stream_channel_display_limit = 10

# Modified display_channel_list function with enhanced features
def display_channel_list(channels, section_key, display_limit_key):
    display_limit = st.session_state[display_limit_key]
    
    if channels:
        # Changed from 3 columns to 4 for better laptop screen utilization
        cols = st.columns(4)  
        
        for i, channel in enumerate(channels[:display_limit]):
            with cols[i % 4]:  # Adjusted to match new column count
                channel_id = f"{section_key}_{i}_{channel['name'].replace(' ', '_')}"
                is_favorite = channel_id in st.session_state.favorites
                
                # Adjusted card styling for better laptop display
                st.markdown(
                    f"""
                    <div class='channel-card' id='{channel_id}' style='
                        min-height: 120px;
                        padding: 12px;
                        margin: 6px 0;
                    '>
                        <div class='favorite-btn'>{'❤️' if is_favorite else '🤍'}</div>
                        <h3 style='
                            margin-bottom: 8px;
                            font-size: 0.9em;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                        '>{channel['name']}</h3>
                        <div style='
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            font-size: 0.8em;
                        '>
                            <span>{'🔴 Live' if random.random() > 0.5 else '⚫ Offline'}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Compact button style for laptop view
                button_key = f"btn_{section_key}_{i}_{channel['name'].replace(' ', '_')}"
                if st.button("Play", key=button_key, help="Play channel", 
                            use_container_width=True,
                            type="primary"):
                    st.session_state.selected_channel = channel
                    st.session_state.selected_channel_index = i
                    
                    new_entry = {
                        'channel': channel['name'],
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.watch_history = [
                        entry for entry in st.session_state.watch_history 
                        if entry['channel'] != channel['name']
                    ]
                    
                    st.session_state.watch_history.append(new_entry)
                    st.session_state.watch_history = st.session_state.watch_history[-50:]
                    st.rerun()
        
        # Load more button with adjusted styling
        if len(channels) > display_limit:
            st.markdown("<br>", unsafe_allow_html=True)
            load_more_key = f"load_more_{section_key}_{display_limit}"
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Load More", key=load_more_key, use_container_width=True):
                    st.session_state[display_limit_key] += 16  # Increased to match 4-column layout
    else:
        st.warning("No channels available in this category.")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📺 All Channels", "⭐ Favorites", "📝 Watch History", "ℹ️ Info"])

with tab1:
    if st.session_state.selected_channel:
        st.markdown("""
            <div class='player-wrapper'>
        """, unsafe_allow_html=True)
        
        with st.spinner("Buffering..."):
            st_player(
                st.session_state.selected_channel['url'],
                playing=st.session_state.user_preferences['autoplay'],
                volume=volume / 100.0,
                playback_rate=playback_speed,
                key="main_player",
                height=1024.55
            )
        
        st.markdown("""
                <div class='video-info'>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
                    <h1 class='video-title'>🎥 {st.session_state.selected_channel['name']}</h1>
                    <div class='video-stats'>
                        <span>🔴 Live</span> • 
                        <span>{random.randint(100, 10000)} watching</span>
                    </div>
                    <div class='video-actions'>
                        <button class='action-button'>
                            👍 Like
                        </button>
                        <button class='action-button'>
                            ⭐ Add to Favorites
                        </button>
                        <button class='action-button'>
                            ↗️ Share
                        </button>
                    </div>
                    <div class='channel-info'>
                        <div class='channel-avatar'></div>
                        <div class='channel-details'>
                            <div class='channel-name'>{st.session_state.selected_channel['name']}</div>
                            <div class='channel-stats'>{random.randint(1000, 100000)} subscribers</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Select a channel to start watching")

    # Channel listings
    st.markdown("<h2 class='category-header'>📺 Main Channels</h2>", unsafe_allow_html=True)
    display_channel_list(filtered_main_channels, "main", "main_channel_display_limit")

    st.markdown("<h2 class='category-header'>🔴 Live Channels</h2>", unsafe_allow_html=True)
    display_channel_list(filtered_live_channels, "live", "live_channel_display_limit")

    st.markdown("<h2 class='category-header'>🌐 Stream Channels</h2>", unsafe_allow_html=True)
    display_channel_list(filtered_stream_channels, "stream", "stream_channel_display_limit")

with tab2:
    st.markdown("<h2 class='category-header'>⭐ Favorite Channels</h2>", unsafe_allow_html=True)
    favorite_channels = [ch for ch in main_channels + live_channels + stream_channels 
                        if f"{ch['name']}" in st.session_state.favorites]
    if favorite_channels:
        display_channel_list(favorite_channels, "favorites", "main_channel_display_limit")
    else:
        st.info("No favorite channels yet. Click the heart icon on any channel to add it to favorites!")

with tab3:
    st.markdown("<h2 class='category-header'>📝 Watch History</h2>", unsafe_allow_html=True)
    if st.session_state.watch_history:
        for entry in reversed(st.session_state.watch_history[-10:]):
            st.markdown(
                f"""
                <div class='channel-card'>
                    <h3>{entry['channel']}</h3>
                    <p>Watched on: {entry['timestamp']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Your watch history will appear here once you start watching channels.")

with tab4:
    st.markdown("<h2 class='category-header'>ℹ️ About</h2>", unsafe_allow_html=True)
    st.markdown("""
    Welcome to Premium IPTV Player! This application provides:
    - 🌟 High-quality streaming
    - 🔄 Regular updates
    - 📱 Mobile compatibility
    - ⚡ Fast loading times
    - 🎯 Smart recommendations
    
    For support, contact: support@iptvplayer.com
    """)

# Footer
st.markdown("""
<div style='text-align: center; margin-top: 50px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px;'>
    <p>© 2024 Premium IPTV Player | Made with ❤️ by Your Name</p>
</div>
""", unsafe_allow_html=True)
