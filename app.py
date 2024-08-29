from flask import Flask, jsonify
import pickle
app = Flask(__name__)
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
