import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.metrics.pairwise import cosine_similarity

from functions import get_ratings, get_movies, make_df, impute


def get_scores2(nameinput1, nameinput2, nameinput3, ratinginput1, ratinginput2, ratinginput3):

    df_rating = get_ratings()
    df_movies = get_movies()

    # get rid of duplicate movies (year) in the movie ids data frame
    df_movies = df_movies.drop_duplicates(subset='title', keep='first')
    # keep only ratings of movies with the unique movie ids from cleand df_movies
    df_rating = df_rating.merge(df_movies['movieId'], on='movieId')

    R = make_df(df_rating,df_movies)

    # Create a dictionary for a new user
    new_user_input = {nameinput1:ratinginput1, nameinput2:ratinginput2, nameinput3:ratinginput3} # user input used to calculate recommendations
    if type(new_user_input) != dict:
        raise TypeError('Please give the input as a dictionary. Type is: '+type(new_user_input))
    # Convert it to a pd.DataFrame
    new_user = pd.DataFrame(new_user_input, columns=R.columns, index=[len(R.index)+1])
    if new_user.shape != (1, 9719):
        raise TypeError(f'new_user not correct shape. Shape is ' + str(new_user.shape))

    R1 = R.append(new_user)
    if R1.shape != (611, 9719):
        raise TypeError(f'R1 has wrong shape for Cosim recommender. Shape is: ' + str(R1.shape))

    unseen_movies = R1.columns[R1.loc[611].isna()]
    if unseen_movies.shape != (9716,):
        raise TypeError(f'unseen_movies wrong shape. Shape is ' + str(unseen_movies.shape))
    
    R1_imputed = impute(R1)
    cs = pd.DataFrame(cosine_similarity(R1_imputed), index=R1.index, columns=R1_imputed.index)

    pred_ratings = [] ########CHANGED
    for movie in unseen_movies: 
        other_users = R1.index[-R1[movie].isna()]
        # put in logic to select most similar users: threshold, closest three,... 
        # prediction of rating: weighted average of rating of closest neighbours
        # sum(similarity*rating)/sum(similarity)  OR  sum(ratings)/no.users
        nominator = 0
        denominator = 0
        for u in other_users:
            rating = R1.loc[u, movie]# What is the rating of the other user?
            sim = cs.loc[611, u] # What is the similarity between active and other user
            nominator += (sim*rating)
            denominator += sim
        pred_rating = nominator/denominator
        pred_ratings.append((movie, pred_rating)) ######CHANGED 
    if len(pred_ratings) == 0:
        raise TypeError(f'pred_ratings not created properly. Length is '+str(len(pred_ratings)))
    preds = pd.DataFrame(pred_ratings, columns = ['movie', 'rating'])

    preds_sorted = preds.sort_values('rating', ascending=False)
    top2 = round(preds_sorted.iloc[0:3], 2)
    return top2