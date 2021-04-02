from random import choice
import pickle
from for_model import get_scores
from recommender_cosim import get_scores2
import pandas as pd
from functions import profile

@profile
def get_movie_recommendation(name1, name2, name3, rating1, rating2, rating3):
    print('***Do some ML magic***') #will be printed in the shell where web server runs
    print('Name1 :', name1)
    print('Rating1: ', rating1)
    print('Name2 :', name2)
    print('Rating2: ', rating2)
    print('Name3 :', name3)
    print('Rating3: ', rating3)
    df = get_scores(name1, name2, name3, rating1, rating2, rating3)
    return df #goes to the browser

def get_movie_recommendation2(name1, name2, name3, rating1, rating2, rating3):
    print('***Do some ML magic***') #will be printed in the shell where web server runs
    print('Name1 :', name1)
    print('Rating1: ', rating1)
    print('Name2 :', name2)
    print('Rating2: ', rating2)
    print('Name3 :', name3)
    print('Rating3: ', rating3)
    df2 = get_scores2(name1, name2, name3, rating1, rating2, rating3)
    return df2 #goes to the browser

if __name__ == '__main__':
    print(get_movie_recommendation("No Game No Life: Zero (2017)", "Father of the Bride Part II (1995)", "Grumpier Old Men (1995)", 2.4, 5, 4.0))
    print(get_movie_recommendation2("No Game No Life: Zero (2017)", "Father of the Bride Part II (1995)", "Grumpier Old Men (1995)", 2.4, 5, 4.0))
    #run when recommender.py is run in terminal
    #but not when importing
