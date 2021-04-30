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


app = flask.Flask(__name__, template_folder='templates')

# path_to_anime_matrix = 'models/anime_matrix.pkl'
# path_to_anime_pivot = 'models/anime_pivot.pkl'
# path_to_knnmodel= 'models/knnmodel.pkl'
# path_to_df_anime = 'models/df_anime.pkl'

N_RECOMMENDATIONS  = 6  # Recommending 5 only (1st will be itself)



# with open(path_to_anime_matrix, 'rb') as f:
#     anime_matrix = pickle.load(f)

# with open(path_to_anime_pivot, 'rb') as f:
#     anime_pivot = pickle.load(f)

# with open(path_to_knnmodel, 'rb') as f:
#     knnmodel = pickle.load(f)

# with open(path_to_df_anime, 'rb') as f:
#     df_anime = pickle.load(f)

arr = []
for i in range(len(anime_pivot)):
    arr.append(df_anime['title'][int(i)])

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))


    # if flask.request.method == 'POST':
    #     results =[]
    #     user_input_text = flask.request.form['user_input_text']
        
    #     idx = arr.index(user_input_text)
    #     results.append(["Anime Selected: "])
        
    #     distances, indices = knnmodel.kneighbors(anime_matrix[idx], n_neighbors = N_RECOMMENDATIONS)
    #     for i in indices:
    #         results.append([df_anime['title'][i]])

        
    #     return flask.render_template('index.html', 
    #         input_text=user_input_text,
    #         result=results)
           




# @app.route('/images/')
# def images():
#     return flask.render_template('images.html')


# @app.route('/bootstrap/')
# def bootstrap():
#     return flask.render_template('bootstrap.html')


# @app.route('/classify_image/', methods=['GET', 'POST'])
# def classify_image():
#     if flask.request.method == 'GET':
#         # Just render the initial form, to get input
#         return(flask.render_template('classify_image.html'))

#     if flask.request.method == 'POST':
#         # Get file object from user input.
#         file = flask.request.files['file']

#         if file:
#             # Read the image using skimage
#             img = io.imread(file)

#             # Resize the image to match the input the model will accept
#             img = transform.resize(img, (28, 28))

#             # Flatten the pixels from 28x28 to 784x0
#             img = img.flatten()

#             # Get prediction of image from classifier
#             predictions = image_classifier.predict([img])

#             # Get the value of the prediction
#             prediction = predictions[0]

#             return flask.render_template('classify_image.html', prediction=str(prediction))

#     return(flask.render_template('classify_image.html'))




if __name__ == '__main__':
    app.run(debug=True)