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
# missing values
mydata.isnull().any()
a = mydata[mydata['description'].isnull()]
a.head()
a.info()

# duplicates
mydata.duplicated().sum()
print(mydata[mydata.duplicated()].head())
mydata[mydata['video_id'] == 'jzLlsbdrwQk'].sort_values(by=['likes'])
# keep first occurance of duplicated rows
mydata.drop_duplicates(keep='first', inplace=True)

# fix datetime columns
mydata['trending_date'] = pd.to_datetime(mydata['trending_date'], errors='coerce', format="%y.%d.%m")
mydata['publish_time'] = pd.to_datetime(mydata['publish_time'], errors='coerce', format="%Y-%m-%dT%H:%M:%S.%fZ")

mydata.insert(5,column='publish_date',value=mydata['publish_time'].dt.date)
mydata['publish_time'] = mydata['publish_time'].dt.time

## EDA ##
# How popular each category in different countries
fig, ax = plt.subplots(3,1, figsize=(20,15))
sns.countplot(x='category', data=mydata[mydata['country'] == 'US'],
              order=mydata[mydata['country'] == 'US']['category'].value_counts().index, ax=ax[0])
sns.countplot(x='category', data=mydata[mydata['country'] == 'GB'],
              order=mydata[mydata['country'] == 'GB']['category'].value_counts().index, ax=ax[1])
sns.countplot(x='category', data=mydata[mydata['country'] == 'CA'],
              order=mydata[mydata['country'] == 'CA']['category'].value_counts().index, ax=ax[2])
ax[0].title.set_text('US')
ax[1].title.set_text('GB')
ax[2].title.set_text('CA')
#plt.show()
plt.savefig('results/graphs/categories_by_country.png')

# views, likes, trending across time
# check that trending date always comes after publish_date
mydata[mydata['trending_date'].dt.date < pd.to_datetime(mydata['publish_date'], format="%Y-%m-%d").dt.date]

mydata.groupby(['country','video_id']).size().sort_values(ascending=False).reset_index()

# todo: I want to stack for each country for each count number of appearances the number of videos I have, and then plot this on a line
#  graph.





