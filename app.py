import flask
import os
import pickle
import pandas as pd
from skimage import io
from skimage import transform
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from scipy.sparse import csr_matrix
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
app = flask.Flask(__name__, template_folder='templates')

path_to_collaborative_filtering_rec = 'models/collaborative_filtering_rec.pkl'
path_to_anime_ratingCount= 'models/anime_ratingCount.pkl'
path_to_df_anime= 'models/df_anime.pkl'
path_to_anime_full_data= 'models/anime_full_data.pkl'

N_RECOMMENDATIONS  = 6  # Recommending 5 only (1st will be itself)



with open(path_to_anime_ratingCount, 'rb') as f:
    anime_ratingCount = pickle.load(f)

with open(path_to_df_anime, 'rb') as f:
    df_anime = pickle.load(f)

with open(path_to_anime_full_data, 'rb') as f:
    anime_full_data = pickle.load(f)

with open(path_to_collaborative_filtering_rec, 'rb') as f:
    collaborative_filtering_rec = pickle.load(f)


def text_cleaning(text):
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    return text

@app.route('/', methods=['GET', 'POST'])
def main():
    
    imgs =[]
    title =[]
    rating = []
    synopsis =[]
    if flask.request.method == 'GET':
        top5_animerating=anime_ratingCount[['anime_uid','title', 'score_review','img_url']].sort_values(by = 'score_review',ascending = False).head(5)
        
        for idd in top5_animerating['anime_uid']:
            imgs.append((anime_ratingCount[anime_ratingCount['anime_uid']==idd]['img_url']).values[0])
            synopsis.append((anime_full_data[anime_full_data['anime_uid']==idd]['synopsis']).values[0])
            title.append((anime_full_data[anime_full_data['anime_uid']==idd]['title']).values[0])
            rating.append((anime_full_data[anime_full_data['anime_uid']==idd]['score']).values[0])

        return flask.render_template('index.html',
            images = imgs, 
            ratings = rating, 
            synopsis = synopsis,
            titles= title )


    if flask.request.method == 'POST':
        top5_animerating=anime_ratingCount[['anime_uid','title', 'score_review','img_url']].sort_values(by = 'score_review',ascending = False).head(5)
        
        for idd in top5_animerating['anime_uid']:
            imgs.append((anime_ratingCount[anime_ratingCount['anime_uid']==idd]['img_url']).values[0])
            synopsis.append((anime_full_data[anime_full_data['anime_uid']==idd]['synopsis']).values[0])
            title.append((anime_full_data[anime_full_data['anime_uid']==idd]['title']).values[0])
            rating.append((anime_full_data[anime_full_data['anime_uid']==idd]['score']).values[0])

        results =[]
        user_input_text = flask.request.form['user_input_text']
        
        collaborative_img_url=[]
        for anime_title in collaborative_filtering_rec[user_input_text][0]:
            results.append(anime_title)
            img_url = (df_anime[df_anime['title']==anime_title]['img_url'].values[0])
            collaborative_img_url.append(img_url)

        ## ------------------------- Content-Based Filtering -------------------------------------
        # df_anime['title'] = df_anime['title'].apply(text_cleaning)
        # tfv = TfidfVectorizer(min_df=3,  max_features=None, 
        #             strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
        #             ngram_range=(1, 3),
        #             stop_words = 'english')

        # # Filling NaNs with empty string
        # df_anime['genre'] = df_anime['genre'].fillna('')
        # genres_str = df_anime['genre'].str.split(',').astype(str)
        # tfv_matrix = tfv.fit_transform(genres_str)

        # sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

        # #getting the indices of anime title
        # indices = pd.Series(df_anime.index, index=df_anime['title']).drop_duplicates()


        # idx = indices[user_input_text]

        # idx = idx[0]
        
        
        # #Get the pairwsie similarity scores 
        # sig_scores = list(enumerate(sig[idx]))
        
        # # Sort the movies 
        # sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # # Scores of the 10 most similar movies
        # sig_scores = sig_scores[1:11]

        # recommended_anime_img = []
        # # Movie indices
        # anime_indices = [i[0] for i in sig_scores]
        # for title in df_anime['title'].iloc[anime_indices].values:
        #     results.append(title)
        #     img_url = (df_anime[df_anime['title']==title]['img_url'].values[0])
        #     if img_url not in recommended_anime_img:
        #         recommended_anime_img.append(img_url)
        return flask.render_template('index.html', 
            input_text=user_input_text,
            result=results,
            images = imgs, 
            ratings = rating, 
            synopsis = synopsis,
            titles= title,
            collaborative_img_url = collaborative_img_url
            # recommended_anime_img  = recommended_anime_img
           )
           




if __name__ == '__main__':
    app.run(debug=True)