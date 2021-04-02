# Helper functions to prepare data
import pandas as pd

def read_in(datapath, districtname):
    """[Convert data files to data frame]

    Args:
        datapath ([type]): [path of raw data file in .csv format]
        districtname ([type]): [district for which raw data are provided]

    Returns:
        [type]: [DataFrame containing data with columns district, meant temp in 0.1, Q_TG]
    """    
    df_raw = pd.read_csv(datapath, parse_dates=True, index_col=1, sep = ';')
    df_raw.rename(columns = {' SOUID':'district', '   TG':'daily mean temp', ' Q_TG':'Q_TG'}, inplace=True)
    df_raw['district'] = districtname
    df_raw['daily mean temp'] = df_raw['daily mean temp'] * 0.1
    df_raw = addmonth(df_raw)
    df_raw = addyear(df_raw)
    return df_raw
  
def addmonth(df1):
    """[Include month column in daily temperature data]

    Args:
        df1 ([type]): [DataFrame including info from raw data]

    Returns:
        [type]: [DataFrame with month for each data point added]
    """    
    df1_temp = df1
    df1_temp['month'] = df1.index.month
    df1 = df1_temp
    return df1

def addyear(df2):
    """[Include year column in daily temperature data]

    Args:
        df2 ([type]): [DataFrame including info from raw data]

    Returns:
        [type]: [DataFrame with year for each data point added]
    """  
    df2_temp = df2
    df2_temp['year'] = df2.index.year
    df2 = df2_temp
    return df2

def addmonthlymean(df3):
    complete = pd.DataFrame()
    for y_n in df3.index.year.unique():  
        for m_n in range(11):
            y = df3.loc[(df3['year'] == y_n) & (df3['month'] == m_n)]
            mean = y['daily mean temp'].mean()
            df_temp = y.copy()
            df_temp['monthly mean temp'] = mean
            y = df_temp
            complete = complete.append(y)
    return complete
