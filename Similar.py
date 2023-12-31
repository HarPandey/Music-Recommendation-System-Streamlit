import Recommenders as Recommenders 
import pandas as pd
import streamlit as st
def app(session_state):
       df = pd.read_csv(r"D:/Project 1/Hindi songs dataset/SingerAndSongs.csv")
       user_data = pd.read_csv(r"D:\Website\Book1.csv")
       df = df.drop_duplicates(subset=['Song name'])
       df = df.reset_index(drop=True)
       st.header('Song Based Similarity')
       music_list = df['Song name'].values

       selected_music = st.selectbox(
            "Type or select a song from the dropdown",
            music_list
        )
       ir = Recommenders.item_similarity_recommender_py()
       ir.create(user_data, 'name', 'song_name')
       t = ir.get_similar_items([selected_music])
       st.write(t)
       
