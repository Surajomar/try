from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__, template_folder="templates")

# Load the data from the pickle file
with open('movie_dict.pkl', 'rb') as f:
    model_data = pickle.load(f)
    movies = pd.DataFrame(model_data)

@app.route('/')
def index():
    return render_template('index.html', model_data=movies['title'])

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

def predict(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names


@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form.get('item')
    if movie:
        recommended_movies = predict(movie)
        return render_template('index.html', model_data=movies['title'], recommended_movies=recommended_movies, selected_movie=movie)
    return render_template('index.html', model_data=movies['title'],recommended_movies=["please select one of the above"])


if __name__ == '__main__':
    app.run(debug=True)
