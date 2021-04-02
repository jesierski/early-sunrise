import pandas as pd
from functions import get_ratings, get_movies, make_df, impute
from for_model import get_scores
from recommender_cosim import get_scores2

def test_rating_in():
    df = get_ratings()
    assert isinstance(df, pd.DataFrame)

def test_movies_in():
    df = get_movies()
    assert isinstance(df, pd.DataFrame)

def test_recommender_nmf():
    result = get_scores('Silver Spoon (2014)', 'Flint (2017)', 'Jumanji (1995)', 1, 4.9, 5.0)
    assert isinstance(result, pd.DataFrame)

def test_recommender_cosim():
    result2 = get_scores2('Silver Spoon (2014)', 'Flint (2017)', 'Jumanji (1995)', 1, 4.9, 5.0)
    assert isinstance(result2, pd.DataFrame)