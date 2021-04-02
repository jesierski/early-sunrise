import re
import pandas as pd
import numpy as np
import pickle

from sklearn.impute import KNNImputer

from functions import get_ratings, get_movies, make_df, impute


FILENAME = 'data/recommender_model_n-comp-20_max-iter-10000_KNN-imputer.sav'


def get_scores(nameinput1, nameinput2, nameinput3, ratinginput1, ratinginput2, ratinginput3):
    # df_rating = get_ratings()
    # df_movies = get_movies()

    # create dataframe with movies, ratings by users
    # R = make_df(df_rating, df_movies)
    #Use fixed matrix R_imputed pickled beforehand to speedup recommender
    R = pd.read_pickle('data/R_imputed.pkl')

    ##make R.column labels movie titles
    #R_movieIds = pd.DataFrame(R.columns)
    #titles = R_movieIds.merge(df_movies, on='movieId')
    #R.columns = titles['title only']

    #Model preparations, define Q
    loaded_model = pickle.load(open(FILENAME, 'rb'))
    Q = loaded_model.components_
    # Make a data frame
    pd.DataFrame(Q, columns=R.columns)

    # Create a dictionary for a new user
    new_user_input = {nameinput1:ratinginput1, nameinput2:ratinginput2, nameinput3:ratinginput3} # user input used to calculate recommendations
    if type(new_user_input) != dict:
        raise TypeError('Please give the input as a dictionary')
    new_user = pd.DataFrame(new_user_input, columns=R.columns, index=[len(R.index)+1])
    # Convert it to a pd.DataFrame
    new_user = pd.DataFrame(new_user_input, columns=R.columns, index=[len(R.index)+1])
    #Fill missing data
    average_movie_rating = R.mean().mean() 
    new_user = new_user.fillna(average_movie_rating)

    #Use model
    #Prediction step 1 - generate user_P 
    user_P = loaded_model.transform(new_user)
    #new user R - reconstruct R but for this new user only
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=R.columns)
    # We want to get rid of movies we have already watchend
    recommendation = user_R.drop(columns=new_user_input.keys())
    # Sort recommendations
    recommendation.sort_values(by=len(R.index)+1, axis=1, ascending=False, inplace=True)
    top = round(recommendation.iloc[:,0:3], 2)

    return top