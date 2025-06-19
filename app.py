import streamlit as st
import pickle
import requests
import os
import requests
def download_file(url, filename):
    if not os.path.exists(filename):
        print("Downloading model file...")
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)

# Google Drive Direct Download Link (example)
download_file("https://drive.google.com/uc?export=download&id=1wUDruHgeI6TYWXdgFdwMQ5AwxzSTrpoO", "similarity.pkl")
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=af2c3525fb6d4799d8ae9cb1160d8590')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"  + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommendations_movies = []
    recommendations_movies_poster = []
    for i in movies_list:
        recommendations_movies.append(movies.iloc[i[0]].title)
        recommendations_movies_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommendations_movies, recommendations_movies_poster
with open('movies.pkl', 'rb') as file:
    movies = pickle.load(file)
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)
st.title('Movie Recommendation system')
selected_movie_name = st.selectbox('what movie do you want us to recommend',movies['title'].values )

if st.button('recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])