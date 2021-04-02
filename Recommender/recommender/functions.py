import pandas as pd
from sklearn.impute import KNNImputer
import cProfile, pstats, io


def profile(fnc):
    
    """A decorator that uses cProfile to profile a function. 
       Starts the profile before executing a function, then exeuctes the function,
       then stops the profile, then prints out a diagnostics report.
       
       Lots of boilerplate code from the Python 3 documentation:
       https://docs.python.org/3/library/profile.html#profile.Profile
       """
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable() ### start the profiler
        
        retval = fnc(*args, **kwargs) ### then actually execute the function
        
        pr.disable() ### then we stop the profiler
        
        ###then print the results to the standard output
        s = io.StringIO()
        sortby = 'cumtime'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        
        ### then return the actual return value of the inner function we executed
        return retval

    ### execute the inner function
    return inner

def get_ratings():
    path = 'data/ml-latest-small/ratings.csv'
    df_rating = pd.read_csv(path, sep=',')
    return df_rating

def get_movies():
    path1 = 'data/ml-latest-small/movies.csv'
    df_movies = pd.read_csv(path1, sep=',')
    return df_movies

def make_df(ratings, movies):
        # movie, ratings by users - prepare for merge
    df = ratings.set_index(['movieId', 'userId'])['rating'].unstack(0)
        # make R.column labels movie titles (year)
    df_movieIds = pd.DataFrame(df.columns)
    titles = df_movieIds.merge(movies, on='movieId')
    df.columns = titles['title']
    return df

def impute(df):
    imputer = KNNImputer()
    df_imputed = pd.DataFrame(imputer.fit_transform(df), index=df.index, columns=df.columns)
    return df_imputed

