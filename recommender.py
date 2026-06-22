import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

merged = movies.merge(ratings, on="movieId")

movie_ratings = merged.pivot_table(
    index="title",
    columns="userId",
    values="rating"
).fillna(0)

similarity = cosine_similarity(movie_ratings)


def recommend(movie_name):
    if movie_name not in movie_ratings.index:
        return []

    movie_index = movie_ratings.index.get_loc(movie_name)

    distances = list(enumerate(similarity[movie_index]))

    movie_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    return [movie_ratings.index[i[0]] for i in movie_list]