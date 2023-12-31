import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import psycopg2
import uuid

def generate_user_id():
    # Generate a random UUID (version 4)
    user_id = str(uuid.uuid4())
    return user_id
def app(session_state):
    CLIENT_ID = "3516208d547447ac914cd09194e6720c"
    CLIENT_SECRET = "2ec51de26fec46069bf8e76207bfa2f3"
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    user_name = session_state.user_name

    if user_name:
        
        
        conn_params = {
            'host': 'localhost',
            'dbname': 'postgres',
            'user': 'postgres',
            'password': '12345',
            'port': 5432,
        }

        conn = psycopg2.connect(**conn_params)
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

        df = pd.read_csv(r"D:/Project 1/Hindi songs dataset/SingerAndSongs.csv")
        print(df.head())
        df = df.drop_duplicates(subset=['Song name'])
        df = df.reset_index(drop=True)
        print(df.shape)

        st.header('Music Recommender System')
        music_list = df['Song name'].values

        selected_music = st.selectbox(
            "Type or select a song from the dropdown",
            music_list
        )
        session_state.selected_value = selected_music


        reference_song_id = selected_music
        reference_song_features = df[df['Song name'] == reference_song_id][['acousticness', 'danceability', 'energy', 'loudness', 'speechiness', 'tempo', 'valence']].values

        df['similarity'] = df[['acousticness', 'danceability', 'energy', 'loudness', 'speechiness', 'tempo', 'valence']].apply(
            lambda x: cosine_similarity((reference_song_features), [x]), axis=1
        )

        # Recommend top N similar songs to the user
        recommended_songs = df.sort_values(by='similarity', ascending=False)[['Singer', 'Song name', 'similarity']].head(6)
        recommended_songs_final = recommended_songs.drop(['similarity'], axis=1)
        print(recommended_songs_final)

        recommended_music_poster = []
        singer_list = recommended_songs_final['Singer'].tolist()
        song_list = recommended_songs_final['Song name'].tolist()
        cur = conn.cursor()
        songname1 = session_state.selected_value
        value = df.loc[df['Song name'] == songname1, 'Singer'].values[0]
        t = generate_user_id()
        sql_query = """INSERT INTO user_songs_complete(id, name, song_name,artist,image)
                VALUES (%s, %s, %s, %s, %s);"""
        update_query = "UPDATE user_songs SET song_name = %s  WHERE name = %s;"
        cur.execute(sql_query, (t, user_name, session_state.selected_value,value,get_song_album_cover_url(songname1,value)))
        copy_query = """COPY user_songs_complete TO 'D:\\Website\\Book1.csv' WITH CSV HEADER"""
        cur.execute(copy_query)
        conn.commit()

        for i in range(len(singer_list)):
            poster_url = get_song_album_cover_url(song_list[i], singer_list[i])
            recommended_music_poster.append(poster_url)
        

        if st.button('Show Recommendation'):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(song_list[0])
                st.image(recommended_music_poster[1]) 
            with col2:
                st.text(song_list[1])
                st.image(recommended_music_poster[2])
            with col3:
                st.text(song_list[2])
                st.image(recommended_music_poster[3])
            with col4:
                st.text(song_list[3])
                st.image(recommended_music_poster[4])
            with col5:
                st.text(song_list[4])
                st.image(recommended_music_poster[5])
        selected_song_data = df[df['Song name'] == selected_music]
        selected_song_data.to_csv(r"D:/Project 1/Hindi songs dataset/SelectedSongs.csv", mode='a', header=False, index=False)
    else:
        st.warning("Please log in first.")


# Uncomment and replace the following lines with the actual data if needed.
# app()
