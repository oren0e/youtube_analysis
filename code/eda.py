import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
pd.set_option('expand_frame_repr', False)  # To view all the variables in the console

# Read data #
def dataReader(country):
    '''
    Description: Reads csv and json file for country code (US, GB, etc.), merges the category variable from the json
    Parameters:
        country: String. Country code.
    Returns:
        a pandas Dataframe.
    '''
    videos_df = pd.read_csv(str(f"data/{country}videos.csv"))
    with open(str(f"data/{country}_category_id.json"), 'r') as f:
        json_vec = json.load(f)

    categories = {}
    for cat in json_vec['items']:
        categories[cat['id']] = cat['snippet']['title']
    temp_df = pd.DataFrame(list(categories.items()), columns=['category_id', 'category'])
    temp_df['category_id'] = temp_df['category_id'].astype(int)
    videos_df = pd.merge(left=videos_df, right=temp_df, on='category_id')

    return videos_df

videos_us = dataReader("US")
videos_gb = dataReader("GB")
videos_ca = dataReader("CA")

# merge 3 dataframes together
videos_us["country"] = "US"
videos_gb["country"] = "GB"
videos_ca["country"] = "CA"
mydata = pd.concat([videos_us,videos_ca,videos_gb],axis=0)
mydata.tail()

# Duplicates, missing values, date-time
