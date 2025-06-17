import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1N2VlNWUzOTk4ZmU4ZTY1ZWY4MTMzZjNkM2JjNDdmZiIsIm5iZiI6MTczNDg0MjkyMy4wNjYsInN1YiI6IjY3Njc5YTJiOGNhNTNjYzZhNzVlMzBhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZCJQaY5AHqdEnMyirMOCzB1_jPAFcWc7yjm4RH_00Ik"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Selected movie not found in the dataset.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie_name)

    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])  # show the poster for the recommended movie
