import streamlit as st
import pandas as pd
import Recommenders as Recommenders 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import psycopg2

CLIENT_ID = "3516208d547447ac914cd09194e6720c"
CLIENT_SECRET = "2ec51de26fec46069bf8e76207bfa2f3"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"
def app(session_state):

    conn_params = {
        'host': 'localhost',
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '12345',
        'port': 5432,
    }

    conn = psycopg2.connect(**conn_params)
    df = pd.read_csv(r"D:/Project 1/Hindi songs dataset/SingerAndSongs.csv")
    user_data = pd.read_csv(r"D:\Website\Book1.csv")
    user_name = session_state.user_name
    pr = Recommenders.popularity_recommender_py()
    pr.create(user_data,'id','song_name')
    t = pr.recommend(user_data['id'] == user_name)
    
    t['Rank'] = t['Rank'].astype(int)
    print(t)
    

    
    #Display the song ranking based on play counts
    st.header('Top Trending Songs')
    st.table(t)



   