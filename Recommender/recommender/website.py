# pip install flask 

from flask import Flask, request, session, redirect
from flask.templating import render_template
import recommender
import pandas as pd

app = Flask('Anja\'s web recommender')

@app.route('/movie') # <-- suffix of the URL
def get_movie():
    d = dict(request.args)
    name1 = d['movie1']
    rating1 = d['rating1']
    name2 = d['movie2']
    rating2 = d['rating2']
    name3 = d['movie3']
    rating3 = d['rating3']
    
    movie = recommender.get_movie_recommendation(name1, name2, name3, rating1, rating2, rating3)
    movies = movie.columns.values
    ratings = list(movie.iloc[0,[0,1,2]])
    
    movie2 = recommender.get_movie_recommendation2(name1, name2, name3, rating1, rating2, rating3)
    movies2 = list(movie2['movie'])
    if len(movies2) != 3:
        raise TypeError(f'Cosim movie list is not of correct length. Length is '+str(len(movies2)))
    ratings2 = list(movie2['rating'])
    if len(ratings2) != 3:
        raise TypeError(f'Cosim ratings list is not of correct length. Length is '+str(len(ratings2)))    
    #return movies
    return render_template('result.html', column_names=movies, row_data=ratings, column_names2=movies2, row_data2=ratings2, title='Your recommendation:') 


@app.route('/')
def hello():
    return render_template('main.html')
     #Use double quotes for a href, html understands only double quotes
    # include images with <img src ="/my_image.png"> 

    # these functions need to return strings
    # it's HTTP response sent to browser

if __name__ == '__main__':
    app.run(debug=True, port=5000)