import streamlit as st
import pickle
import requests  # <--- Make sure this is imported
import os

# import gdown # <--- This line MUST be commented out or removed

# --- Configuration ---
# Your Hugging Face direct download URL for similarity.pkl
# >>> IMPORTANT: REPLACE THIS WITH YOUR ACTUAL HUGGING FACE DIRECT DOWNLOAD LINK <<<
# Example format: "https://huggingface.co/your_username/your_repo_name/resolve/main/similarity.pkl"
SIMILARITY_FILE_URL = "https://huggingface.co/MPhoenix/MovieRecommendation/resolve/main/similarity.pkl"  # YOU MUST UPDATE THIS MANUALLY
SIMILARITY_FILE_LOCAL_PATH = "similarity.pkl"

# TMDB API Key
TMDB_API_KEY = "af2c3525fb6d4799d8ae9cb1160d8590"  # Consider using st.secrets for production


# --- Functions for Loading Data (with Caching) ---

@st.cache_resource  # Use st.cache_resource for large models/objects loaded once across all sessions
def load_similarity_model(file_path, url):
    """Downloads the similarity matrix from the specified URL and loads it."""
    if not os.path.exists(file_path):
        with st.spinner(f"Downloading {os.path.basename(file_path)}... This might take a moment."):
            try:
                # Use requests for direct HTTP download from Hugging Face
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

                # Write the content to the local file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                st.success(f"{os.path.basename(file_path)} downloaded successfully!")
            except requests.exceptions.RequestException as e:
                st.error(
                    f"Failed to download {os.path.basename(file_path)}. Please check the URL and sharing permissions. Error: {e}")
                st.stop()  # Stop the app if download fails

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except (pickle.UnpicklingError, EOFError) as e:  # Catch specific unpickling errors
        st.error(
            f"Error loading {os.path.basename(file_path)}. It might be corrupted or not a valid pickle file. Error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {os.path.basename(file_path)}: {e}")
        st.stop()


@st.cache_data  # Use st.cache_data for smaller dataframes or objects loaded once
def load_movies_data(file_path='movies.pkl'):
    """Loads the movies dataframe."""
    if not os.path.exists(file_path):
        st.error(f"Error: {file_path} not found. Please ensure it's committed to your GitHub repository.")
        st.stop()
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    except (pickle.UnpicklingError, EOFError) as e:
        st.error(f"Error loading {file_path}. It might be corrupted or not a valid pickle file. Error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {file_path}: {e}")
        st.stop()


# --- Function to fetch poster from TMDB ---
@st.cache_data  # Cache poster fetching to avoid repeated API calls
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}')
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Placeholder if no poster
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"


# --- Recommendation logic ---
def recommend(movie, movies_df, similarity_matrix):
    try:
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        movies_list = sorted(list(enumerate(similarity_matrix[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []
        for i in movies_list:
            movie_title = movies_df.iloc[i[0]].title
            movie_id = movies_df.iloc[i[0]].movie_id  # Assuming 'movie_id' column exists

            recommended_movies.append(movie_title)
            recommended_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_posters
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset for recommendation. Please select another movie.")
        return [], []
    except Exception as e:
        st.error(f"An unexpected error occurred during recommendation: {e}")
        return [], []


# --- Load data (these lines run when the app starts up) ---
# Load similarity matrix (will download from Hugging Face if not present)
similarity = load_similarity_model(SIMILARITY_FILE_LOCAL_PATH, SIMILARITY_FILE_URL)

# Load movies dataframe (assumes movies.pkl is in your GitHub repo)
movies = load_movies_data('movies.pkl')

# --- Streamlit UI ---
st.title('Movie Recommendation System')

# Only display UI elements if data loaded successfully
if movies is not None and not movies.empty and similarity is not None:
    selected_movie_name = st.selectbox('What movie do you want us to recommend?', movies['title'].values)

    if st.button('Recommend'):
        if selected_movie_name:  # Ensure a movie is selected
            names, posters = recommend(selected_movie_name, movies, similarity)
            if names:  # Only display if recommendations were found
                cols = st.columns(5)
                for i in range(5):
                    with cols[i]:
                        st.text(names[i])
                        st.image(posters[i])
else:
    st.info("Initializing application... Please wait.")