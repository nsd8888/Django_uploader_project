
#first we import ResNet ml_model for with imagenet dataset
#we know that this dataset is not required for us

import os
import numpy as np
import tensorflow.keras
from keras.layers import GlobalMaxPooling2D
from numpy.linalg import norm
import pickle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
import boto3
import io
from PIL import Image



def training_model(lst,img_search):
    img_size = 224
    model = ResNet50(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
    model = tensorflow.keras.Sequential([
        model,
        GlobalMaxPooling2D()
    ])

    img_list =[]
    img_list.append(img_search)

    print('img_list',img_list)

    s3 = boto3.resource(service_name='s3', region_name='ap-south-1', aws_access_key_id='_',
                        aws_secret_access_key='_')
    for bucket in s3.buckets.all():
        my_bucket = s3.Bucket(bucket.name)
        c = []
        for file in my_bucket.objects.all():
            c.append(file.key)
        print(c)
        print(set(c))

        d=set(c).intersection(set(lst))
        t=set(c).intersection((set(img_list)))
        print(d)
        dilenames=list(d)
        print(dilenames)
        print(t)
    filenames=[]
    for i in dilenames:
        bucket = s3.Bucket('cosmosimages88')
        object = bucket.Object(i)
        file = io.BytesIO()
        object.download_fileobj(file)
        img = Image.open(io.BytesIO(object.get()['Body'].read()))
        img = img.convert('RGB')
        img = img.resize((224, 224), Image.NEAREST)
        filenames.append(img)

    def extract_features(img, model):
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preproccessed_img = preprocess_input(expanded_img_array)
        result = model.predict(preproccessed_img).flatten()
        norm_result = result / (norm(result))
        return norm_result

    feature_list = []
    for file in filenames:
        feature_list.append(extract_features(file, model))
    print("this is from feature_list",feature_list)

    #pickle.dump(feature_list, open('embeddings.pkl', 'wb'))
    #pickle.dump(dilenames, open('filenames.pkl', 'wb'))

##def tets started
    #feature_list = pickle.load(open('embeddings.pkl', 'rb'))
    #filenames = pickle.load(open('filenames.pkl', 'rb'))

    for i in (list(t)):
        bucket = s3.Bucket('cosmosimages88')
        object = bucket.Object(i)
        file = io.BytesIO()
        object.download_fileobj(file)
        img = Image.open(io.BytesIO(object.get()['Body'].read()))
        img = img.convert('RGB')
        img = img.resize((224, 224), Image.NEAREST)
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preproccessed_img = preprocess_input(expanded_img_array)
        result = model.predict(preproccessed_img).flatten()
        norm_result = result / (norm(result))

        neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
        neighbors.fit(feature_list)

        print("this is norm _result of search img",norm_result)

        dist, indices = neighbors.kneighbors(([norm_result]))
    # print(indices)
        output = []
        for file in indices[0]:
            output.append(dilenames[file])
        print("this is output of result",output)
        return output
