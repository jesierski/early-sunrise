#Feature engineering functions for Bike sharing project
import pandas as pd
import numpy as np
import math

from sklearn.preprocessing import MinMaxScaler, StandardScaler, FunctionTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score

# feature engineer training set data
def fe_train(data):
    ''' implement transformer workflow e.g.
    transformer = StandardScaler()
    transformer.fit(Xtrain[['desired_column']])
    transformer.transform(X_train[['desired_column]])
    '''
    # drop correlated columns atemp/temp and season/weather
    data_temp = data.drop(columns = ['season', 'holiday','workingday','humidity', 'weather', 'atemp'])

    # add columns with the hours as sin/cos combination to capture cyclic nature of the hours to include hours in model training
    data_temp['sin_time'] = np.sin(2*np.pi*data.index.hour/24)
    data_temp['cos_time'] = np.cos(2*np.pi*data.index.hour/24)

    c_transformer = ColumnTransformer([
    ('pass', 'passthrough', ['sin_time', 'cos_time']),
    ('scale1', StandardScaler(), [ 'temp']),
    ('scale3', StandardScaler(), [ 'windspeed']),
    ])

    data_fe = pd.DataFrame(c_transformer.fit_transform(data_temp), index = data.index, columns = ['sin_time', 'cos_time', 'temp', 'windspeed'])

    return data_fe

def fe_test(data2):
    # drop correlated columns atemp/temp and season/weather
    data2_temp = data2.drop(columns = ['season', 'holiday','workingday','humidity', 'weather', 'atemp'])

    # add columns with the hours as sin/cos combination to capture cyclic nature of the hours to include hours in model training
    data2_temp['sin_time'] = np.sin(2*np.pi*data2.index.hour/24)
    data2_temp['cos_time'] = np.cos(2*np.pi*data2.index.hour/24)

    c_transformer = ColumnTransformer([
    ('pass', 'passthrough', ['sin_time', 'cos_time']),
    ('scale1', StandardScaler(), [ 'temp']),
    ('scale3', StandardScaler(), [ 'windspeed']),
    ])

    data2_fe = pd.DataFrame(c_transformer.fit_transform(data2_temp), index = data2.index, columns = ['sin_time', 'cos_time', 'temp', 'windspeed'])

    return data2_fe

def prediction_to_csv(testdata, model):
    ytarget_pred = model.predict(testdata)
    submission = pd.DataFrame(ytarget_pred, index=testdata.index, columns=['count'])
    submission.loc[submission["count"] < 0, "count"] = 0

    submission.to_csv('data/bike-sharing-demand/bikeshare_submission.csv')


