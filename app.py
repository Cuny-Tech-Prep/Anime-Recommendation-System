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

path_to_anime_pivot = 'models/anime_pivot.pkl'
path_to_model_knn= 'models/model_knn.pkl'

N_RECOMMENDATIONS  = 6  # Recommending 5 only (1st will be itself)



with open(path_to_anime_pivot, 'rb') as f:
    anime_pivot = pickle.load(f)

with open(path_to_model_knn, 'rb') as f:
    model_knn = pickle.load(f)

arr = []
for i in range(len(anime_pivot)):
    arr.append(anime_pivot.index[int(i)])

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))


    if flask.request.method == 'POST':
        results =[]
        user_input_text = flask.request.form['user_input_text']
        
        if(isinstance(user_input_text, str)):
            # finds the id from the string.
            idx = arr.index(user_input_text)
        else:
            idx = user_input_text
        
        distances, indices = model_knn.kneighbors(anime_pivot.iloc[idx,:].values.reshape(1, -1), n_neighbors = N_RECOMMENDATIONS)
        for i in range(0, len(distances.flatten())):
            if i == 0:
                results.append(['Recommendations for {0} with id {1}:'.format(anime_pivot.index[idx], idx)])
            else:
                results.append(['{0}: {1}, with distance of {2}:'.format(i, anime_pivot.index[indices.flatten()[i]], round(distances.flatten()[i], 4))])
        
        return flask.render_template('index.html', 
            input_text=user_input_text,
            result=results)
           


@app.route('/anime/')
def anime():
    return flask.render_template('anime.html')



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