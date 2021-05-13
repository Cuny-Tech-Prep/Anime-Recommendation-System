import flask
import os
import pickle
import pandas as pd
from skimage import io
from skimage import transform
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D

app = flask.Flask(__name__, template_folder='templates')

path_to_collaborative_filtering_rec = 'models/collaborative_filtering_rec.pkl'
path_to_anime_ratingCount= 'models/anime_ratingCount.pkl'
path_to_df_anime= 'models/df_anime.pkl'
path_to_anime_full_data= 'models/anime_data.pkl'
path_to_content_based_rec = 'models/content_based_rec.pkl'



with open(path_to_anime_ratingCount, 'rb') as f:
    anime_ratingCount = pickle.load(f)

with open(path_to_df_anime, 'rb') as f:
    df_anime = pickle.load(f)

with open(path_to_anime_full_data, 'rb') as f:
    anime_full_data = pickle.load(f)

with open(path_to_collaborative_filtering_rec, 'rb') as f:
    collaborative_filtering_rec = pickle.load(f)

with open(path_to_content_based_rec, 'rb') as f:
    content_based_rec = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def main():
    
    imgs =[]
    title =[]
    rating = []
    synopsis =[]
    if flask.request.method == 'GET':
        top5_animerating=anime_ratingCount[['anime_uid','title', 'score_review','img_url']].sort_values(by = 'score_review',ascending = False).head(10)
        
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
        err = "" 

        top5_animerating=anime_ratingCount[['anime_uid','title', 'score_review','img_url']].sort_values(by = 'score_review',ascending = False).head(5)
        
        for idd in top5_animerating['anime_uid']:
            imgs.append((anime_ratingCount[anime_ratingCount['anime_uid']==idd]['img_url']).values[0])
            synopsis.append((anime_full_data[anime_full_data['anime_uid']==idd]['synopsis']).values[0])
            title.append((anime_full_data[anime_full_data['anime_uid']==idd]['title']).values[0])
            rating.append((anime_full_data[anime_full_data['anime_uid']==idd]['score']).values[0])

        collaborative_recommended_anime_title =[]
        user_input_text = flask.request.form['user_input_text']
        collaborative_img_url=[]
        try:
            for index in range(len(collaborative_filtering_rec[user_input_text][0])):
                if index <N_RECOMMENDATIONS:
                    anime_title = collaborative_filtering_rec[user_input_text][0][index]
                    collaborative_recommended_anime_title.append(anime_title)
                    img_url = (df_anime[df_anime['title']==anime_title]['img_url'].values[0])
                    collaborative_img_url.append(img_url)
        except KeyError: 
            err = "Title not found"

        content_recommended_anime_title =[]
        content_img_url=[]
        try:
            for index in range(len(content_based_rec[user_input_text])):
                if index <N_RECOMMENDATIONS:
                    anime_title = content_based_rec[user_input_text][index]
                    content_recommended_anime_title.append(anime_title)
                    img_url = (df_anime[df_anime['title']==anime_title]['img_url'].values[0])
                    content_img_url.append(img_url)
        except KeyError: 
            err = "Title not found" 

        return flask.render_template('index.html', 
            input_text=user_input_text,
            collaborative_recommended_anime_title=collaborative_recommended_anime_title,
            images = imgs, 
            ratings = rating, 
            synopsis = synopsis,
            titles= title,
            collaborative_img_url = collaborative_img_url,
            content_recommended_anime_title= content_recommended_anime_title,
            content_img_url=content_img_url,
            error = err
           )
           




if __name__ == '__main__':
    app.run(debug=True)