import streamlit as st
from streamlit_option_menu import option_menu
import Home, Login, Trending,History,Special_Songs,Similar

st.set_page_config(
    page_title="Music Recommender",
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Music Recommender',
                options=['Home', 'Trending', 'Login','History','Special','Similar'],
                icons=['house-fill', 'trophy-fill', 'info-circle-fill','globe_with_meridians'],
                menu_icon='chat-text-fill',
                default_index=2,  # Set default index to 'Login'
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if 'user_name' not in st.session_state:
            st.session_state.user_name = None

        if app == "Home":
            Home.app(st.session_state)
        elif app == "Trending":
            Trending.app(st.session_state)
        elif app == 'Login':
            Login.app(st.session_state)
        elif app == 'History':
            History.app(st.session_state)
        elif app == 'Special':
            Special_Songs.app(st.session_state)
        elif app == 'Similar':
            Similar.app(st.session_state)

# Create an instance of MultiApp
app_manager = MultiApp()

# Add apps to the MultiApp
app_manager.add_app("Home", Home.app)
app_manager.add_app("Trending", Trending.app)
app_manager.add_app("Login", Login.app)
app_manager.add_app("History", History.app)
app_manager.add_app("Special", Special_Songs.app)
app_manager.add_app("Similar", Similar.app)

# Run the MultiApp
app_manager.run()
