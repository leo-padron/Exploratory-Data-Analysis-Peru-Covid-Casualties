"""
This script extracts only covid-related records from clean data
"""
import os
import src.utilities as utils
import numpy as np
import pandas as pd 
from polyfuzz import PolyFuzz
from polyfuzz.models import RapidFuzz
from rapidfuzz import fuzz
import time

def get_clean_data():
    
    config = utils.read_config()
    
    path =  os.path.join(config['data']['clnFilePath'], 'clean_data.csv')
    df = pd.read_csv(path)
    return df

def sample_data():
    
    # take a random sample (10%) from the data.
    df = get_clean_data()
    df = df.sample(frac=0.1, random_state=1)
    return df   

def select_series():
    
    df = sample_data()
    causes_df = df[df.columns[-6:]]
    causes_df = causes_df.applymap(lambda s:str(s))    
    return causes_df

def extract_matches(series):
    
    #queries = [['covid-19'], ['covid'], ['covid19'],['coronavirus'], ['sars-cov-2'],['covid-19 coronavirus sars-cov-2']]
    queries = [['covid-19'], ['sars-cov-2'],['coronavirus']]
    idx = np.array([], dtype='int64')
    series = series.to_list()
    
    for query in queries:
        matcher = RapidFuzz(n_jobs=1, score_cutoff=0.6, scorer=fuzz.token_set_ratio)
        model = PolyFuzz(matcher)
        model.match(series, query)
        matches = model.get_matches()  
        #lst = matches.loc[matches['Similarity']>= 0.6].index.to_list()
        array = matches.loc[matches['Similarity']>= 0.6].index.to_numpy()
        #indexes.extend(lst)
        idx = np.concatenate([idx, array])
        #list(set(indexes))
        
    idx = np.unique(idx)
    return idx  

def get_indexes():
    
    startTime = time.time()
    
    causes_df = select_series()
    indexes = np.array([],dtype='int64')
    
    for s in causes_df:
        s = causes_df[s]
        idx = extract_matches(s)
        indexes =np.concatenate([indexes, idx])
    
    indexes = np.unique(indexes)
    
    
    print ('Transformation took {0} seconds.'.format(time.time() - startTime))
    
    return indexes
    
def transform_data(df, indexes):
    
    config = utils.read_config()
    df = df.iloc[indexes]
    df.to_csv(os.path.join(config['data']['tsFilePath'], 'ts_data.csv'),index=False)
    
def main():
    print("\nSampling data...done.")
    print("Transforming data...")
    indexes = get_indexes()
    df = sample_data()
    transform_data(df,indexes)
    print("Done.\n")

if __name__ == "__main__":
    # Master function
    main()