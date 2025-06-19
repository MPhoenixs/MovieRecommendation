                                              https://movierecommendation-4swn.onrender.com
This project implements a simple movie recommendation system using content-based filtering. It recommends movies to users based on the similarity of movie 
attributes (e.g., genres, keywords, cast, crew) to a selected movie.
Movie Selection: Users can select a movie from a dropdown list.
Top 5 Recommendations: The system provides a list of the top 5 most similar movies.
Movie Posters: Displays movie posters fetched from The Movie Database (TMDB) API for visual context.
Efficient Data Handling: Utilizes Streamlit's caching mechanisms to efficiently load large data files and prevent redundant API calls.
Python: The core programming language.
Streamlit: For creating the interactive web application.
Pandas: For data manipulation and analysis.
NumPy: For numerical operations, especially with the similarity matrix.
Scikit-learn (implied): Likely used for calculating movie similarities (e.g., using TfidfVectorizer and cosine_similarity in the data preparation phase).
Requests: For making HTTP requests to download the similarity data and fetch movie posters from TMDB.
Hugging Face Hub: Used to host the large similarity.pkl file for reliable download by the deployed Streamlit app.
The Movie Database (TMDB) API: For fetching movie poster 
