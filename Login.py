import streamlit as st
import psycopg2
def app(session_state):

    
    st.header('Login')
    name = st.text_input("Enter Your name: ")
    session_state.user_name = name
  
# Create a cursor object
   

# Sample data to insert
   

# SQL query to insert data
    sql_query = """INSERT INTO user_songs(id, name, song_name)
                VALUES (%s, %s, %s);"""

# Execute the query

