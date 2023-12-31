import Recommenders as Recommenders 
import pandas as pd
import streamlit as st
def app(session_state):
    
    st.header("Your History")
    user_data = pd.read_csv(r"D:\Website\Book1.csv")
    df = pd.read_csv(r"D:/Project 1/Hindi songs dataset/SingerAndSongs.csv")
    user_name = session_state.user_name
    ir = Recommenders.item_similarity_recommender_py()
    ir.create(user_data, 'name', 'song_name')
    user_items = ir.get_user_items(user_name)
    for user_item in user_items:
       print(user_item)
       st.write(user_item)


