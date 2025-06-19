import streamlit as st
import pickle
import requests
import os

# Download similarity.pkl from Google Drive
file_id = "1wUDruHgeI6TYWXdgFdwMQ5AwxzSTrpoO"
url = f"https://drive.google.com/uc?id={file_id}"
output = "similarity.pkl"

if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=af2c3525fb6d4799d8ae9cb1160d8590')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"  + data['poster_path']

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommendations_movies = []
    recommendations_movies_poster = []
    for i in movies_list:
        recommendations_movies.append(movies.iloc[i[0]].title)
        recommendations_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommendations_movies, recommendations_movies_poster

# Load pickles
with open('movies.pkl', 'rb') as file:
    movies = pickle.load(file)
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

# Streamlit UI
st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('What movie do you want us to recommend?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
