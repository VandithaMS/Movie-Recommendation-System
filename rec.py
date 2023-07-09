import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import re

mdf = pd.read_csv('https://raw.githubusercontent.com/krishnaik06/Recommendation_complete_tutorial/master/KNN%20Movie%20Recommendation/movies.csv',
                usecols=['movieId', 'title'], dtype={'movieId':'int32','title':'str'})
rdf = pd.read_csv('https://raw.githubusercontent.com/krishnaik06/Recommendation_complete_tutorial/master/KNN%20Movie%20Recommendation/ratings.csv',
                 usecols=['userId', 'movieId', 'rating'], dtype={'userId':'int32', 'movieId':'int32', 'rating':'float32'})

df = pd.merge(mdf,rdf, on='movieId')
df.head()

cmr = df.dropna(axis=0, subset=['title'])
movieRatingCount = (cmr.groupby(by=['title'])['rating'].count().reset_index().rename(columns={'rating':'totalRatingCount'})
                    [['title','totalRatingCount']])
movieRatingCount.head()

rating_with_totalRatingCount = cmr.merge(movieRatingCount, left_on = 'title', right_on = 'title', how = 'left')
rating_with_totalRatingCount.head()
pd.set_option('display.float_format', lambda x :'%.3f' % x)
# print(movieRatingCount['totalRatingCount'].describe())

popThres = 50
pop_mov = rating_with_totalRatingCount.query('totalRatingCount >= @popThres')
pop_mov.head()

movie_features_df = pop_mov.pivot_table(index='title',columns='userId',values='rating').fillna(0)
movie_features_df.head()
titleList=list(movie_features_df.index)

from scipy.sparse import csr_matrix

df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(df_matrix)
df_matrix.shape

# pickle.dump(model_knn, open('model.pkl', 'wb'))
# pickle.dump(movie_features_df, open('data.pkl','wb'))

# n = np.random.choice(df_matrix.shape[0])
def recommend(name):
    n=retName(name)
    print(n)
    dis,idx = model_knn.kneighbors(movie_features_df.iloc[n,:].values.reshape(1,-1), n_neighbors=8)
    l=[]
    print('Recommendations for '+ movie_features_df.index[n])
    for i in range(1,len(dis.flatten())):
        new_str = re.sub('[!?.,:-]',"",movie_features_df.index[idx.flatten()[i]][:-6])
        l.append(new_str)
        print('{0} : {1} with distance of {2}'.format(i, movie_features_df.index[idx.flatten()[i]], dis.flatten()[i]))
    return l

def retName(name):
    n=titleList.index(name)
    return n