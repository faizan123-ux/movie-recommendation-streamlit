
import streamlit as st
import pandas as pd
import requests
from recommender import recommend



movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Average ratings
movie_avg_ratings = (
    ratings.groupby("movieId")["rating"]
    .mean()
    .reset_index()
)

movies = movies.merge(
    movie_avg_ratings,
    on="movieId",
    how="left"
)



@st.cache_data
def fetch_poster(movie_title):

    api_key = "ff1d1b7cf097b3a3b8af73af8bc55404"

    # Remove year from title
    movie_title = movie_title.split("(")[0].strip()

    search_url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": movie_title
    }

    try:
        response = requests.get(
            search_url,
            params=params
        )

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

    except:
        pass

    return None



st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

st.subheader("🔍 Search Movie")

search_movie = st.text_input(
    "Type a movie name"
)

<<<<<<< HEAD
movie_list = []

if search_movie:

    movie_list = [
        movie for movie in movies["title"].values
        if search_movie.lower() in movie.lower()
    ]

else:

    movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Search and select a movie",
    sorted(movie_list)
)



=======
>>>>>>> 835dbeaa7e16d81f15802d7721a705f914fb1c52


if st.button("Recommend"):

    with st.spinner(
        "Finding recommendations..."
    ):

        recommendations = recommend(
            selected_movie
        )

    st.subheader(
        "Recommended Movies"
    )

    if recommendations:

        cols = st.columns(5)

        for i, movie in enumerate(
            recommendations
        ):

            poster = fetch_poster(movie)

            movie_info = movies[
                movies["title"] == movie
            ]

            with cols[i % 5]:

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.image(
                        "https://via.placeholder.com/300x450?text=No+Poster",
                        use_container_width=True
                    )

                st.markdown(
                    f"**{movie}**"
                )

                if not movie_info.empty:

                    rating = (
                        movie_info.iloc[0]
                        ["rating"]
                    )

                    genres = (
                        movie_info.iloc[0]
                        ["genres"]
                    )

                    if pd.notna(rating):

                        st.write(
                            f"⭐ {rating:.1f}"
                        )

                    st.caption(
                        genres.replace(
                            "|",
                            " • "
                        )
                    )

    else:

        st.warning(
            "No recommendations found."
        )




