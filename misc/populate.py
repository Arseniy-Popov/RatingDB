import os
import datetime as dt

import requests

from dotenv import load_dotenv


load_dotenv()
URL_RDB = "http://127.0.0.1:8080/api/v1"
URL_TMDB = "https://api.themoviedb.org/3"
RDB_ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
RDB_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
AUTH_RDB = (RDB_ADMIN_LOGIN, RDB_ADMIN_PASSWORD)
AUTH_TMDB = {"api_key": os.getenv("TMDB_API"), "language":"en"}


def _slugify(input):
    return "".join([x.lower() if x != " " else "_" for x in input])


def _get_genre_slugs(ids):
    response = requests.get(URL_TMDB + "/genre/movie/list", params=AUTH_TMDB)
    slugs = []
    for id in ids:
        for genre in response.json()["genres"]:
            if genre["id"] == id:
                slugs.append(_slugify(genre["name"]))
    return slugs


def _check_duplicate_title(name, year):
    response = requests.get(
        URL_RDB + "/titles/", params={"name": name, "year": year}
    ).json()
    if response["count"] > 0:
        return True
    return False


def populate_categories():
    categories = ("Movie", "Series", "Book")
    for category in categories:
        requests.post(
            URL_RDB + "/categories/", data={"name": category, "slug": category.lower()}, auth=AUTH_RDB
        )


def populate_genres():
    response = requests.get(URL_TMDB + "/genre/movie/list", params=AUTH_TMDB)
    for genre in response.json()["genres"]:
        data = {"slug": _slugify(genre["name"]), "name": genre["name"]}
        requests.post(URL_RDB + "/genres/", data=data, auth=AUTH_RDB)


def populate_movies(pages=10):
    for page in range(1, pages+1):
        params = {**AUTH_TMDB, "page": page}
        response = requests.get(URL_TMDB + "/movie/top_rated", params=params)
        for movie in response.json()["results"]:
            name, description, category = (
                movie["original_title"],
                movie["overview"],
                "movie",
            )
            year = dt.date.fromisoformat(movie["release_date"]).year
            genres = _get_genre_slugs(movie["genre_ids"])
            if _check_duplicate_title(name, year) or movie["adult"]:
                continue
            data = {
                "name": name,
                "year": year,
                "description": description,
                "genre": genres,
                "category": category,
            }
            requests.post(URL_RDB + "/titles/", data=data, auth=AUTH_RDB)


def populate_reviews(movie_id, title_id, pages=10):
    for page in range(1, pages+1):
        params = {**AUTH_TMDB, "page": page}
        response = requests.get(URL_TMDB + f"/movie/{movie_id}/reviews", params=params)
        for review in response.json()["results"]:
            author, text, score = review["author"], review["content"], review["author_details"]["rating"]
            data = {"text": text, "score": score}
            auth = ("author", os.getenv("USER_PASSWORD"))
            response = requests.post(URL_RDB + f"/titles/{title_id}/reviews/", data=data, auth=AUTH_RDB)


if __name__ == "__main__":
    populate_categories()
    populate_genres()
    populate_movies()
