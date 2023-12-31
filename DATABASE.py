import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="12345", port=5432)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_songs(
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        song_name VARCHAR(255)
    );
""")


conn.commit()
cur.close()
conn.close()