import os
import requests
from flask import Flask, jsonify
import pickle
import gdown
app = Flask(__name__)
url = "https://drive.google.com/uc?export=download&id=1sauUXQvSGzzANz_ElxC0jkvHQIi4avRK"
output = "similarity.pkl"
gdown.download(url, output, quiet=False)


if not os.path.exists("similarity.pkl"):
    download_file(url, "similarity.pkl")


movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


@app.route('/movies/<string:movie>')
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    result = {}
    counter = 1
    for i in movies_list:
        movie_counter = str(counter)
        movie_counter = "movie"+movie_counter
        counter += 1
        value = movies.iloc[i[0]].title
        result[movie_counter] = value
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
