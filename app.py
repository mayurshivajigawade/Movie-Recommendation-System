import streamlit as st
import pickle
import requests
import os

from dotenv import load_dotenv


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------
# Load Recommendation Model
# -----------------------------

movies = pickle.load(
    open("model/movies.pkl", "rb")
)

similarity = pickle.load(
    open("model/similarity.pkl", "rb")
)


# -----------------------------
# Recommendation Function
# -----------------------------

def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movie_list:

        recommendations.append(
            movies.iloc[i[0]].title
        )

    return recommendations


# -----------------------------
# TMDB Poster Function
# -----------------------------

def fetch_poster(movie_title):

    if not TMDB_API_KEY:
        return None

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("results"):

            poster_path = data["results"][0].get(
                "poster_path"
            )

            if poster_path:

                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

    except requests.RequestException:

        return None

    return None


# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">'
    '🎬 Movie Recommendation System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover movies similar to your favorites'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Movie Selection
# -----------------------------

selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies["title"].values
)


# -----------------------------
# Recommendation Button
# -----------------------------

if st.button(
    "🎯 Recommend Movies",
    use_container_width=True
):

    recommendations = recommend(
        selected_movie
    )

    st.subheader(
        f"🍿 Movies similar to {selected_movie}"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [
        col1,
        col2,
        col3,
        col4,
        col5
    ]

    for column, movie in zip(
        columns,
        recommendations
    ):

        with column:

            poster = fetch_poster(movie)

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster unavailable"
                )

            st.markdown(
                f"### 🎬 {movie}"
            )