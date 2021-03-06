# -*- coding: utf-8 -*-
"""「feature_nowwin.ipynb」的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vHa-IsVU5IGOrd3LCw8gP-1qHnoCS5BP
"""

# for garbage collection
import gc

# for warnings
import warnings
warnings.filterwarnings("ignore")

# utility libraries
import os
import numpy as np 
import pandas as pd 
import cv2
import tqdm
import tensorflow as tf

# keras libraries
import keras
from tensorflow.keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.layers import BatchNormalization, Dense, GlobalAveragePooling2D, Lambda, Dropout, InputLayer, Input
from keras import backend as K
from keras.callbacks import EarlyStopping
from sklearn.model_selection import StratifiedKFold
from keras import optimizers

data_dir = os.path.abspath(os.getcwd())
print("The directory of the executable file is "+data_dir)

train_txt = '/training_labels.txt'
test_txt = '/testing_img_order.txt'

def set_labeldf():
  header_list = ["img", "breed"]
  labels_df  = pd.read_csv(data_dir+train_txt, sep = " ",names = header_list)  # all the testing images
  train_dir = 'training_images/'
  bird_breeds = sorted(list(set(labels_df['breed'])))
  n_classes = len(bird_breeds)

  class_dict = dict(zip(bird_breeds, range(n_classes)))
  labels_df['file_path'] = labels_df['img'].apply(lambda x:train_dir+f"{x}")
  labels_df['breed'] = labels_df.breed.map(class_dict)
  return labels_df, class_dict
labels_dataframe, class_to_num = set_labeldf()

# set image size here
img_size = 500
bath_size = 64


# TEST IMAGES

# print(image_path)
with open(data_dir+test_txt) as f:
      test_images = [x.strip() for x in f.readlines()]  # all the testing images
def read_testimg():
  test_dir = 'testing_images/'
  f.close()
  X_tsls = [] 
  for image in tqdm.tqdm(np.array(test_images)):
    image_path = data_dir+'/'+test_dir+image
    orig_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    res_image = cv2.resize(orig_image,(img_size, img_size))
    X_tsls.append(res_image)
  return X_tsls

X_test = read_testimg()
Xtesarr = np.array(X_test)

del(X_test)
gc.collect()
print(Xtesarr.shape)

# FEATURE EXTRACTION OF VALIDAION AND TESTING ARRAYS
def get_valfeatures(model_name, data_preprocessor, data):
    '''
    Same as above except not image augmentations applied.
    Used for feature extraction of validation and testing.
    '''
    dataset = tf.data.Dataset.from_tensor_slices(data)

    ds = dataset.batch(bath_size)

    input_size = data.shape[1:]

    # Prepare pipeline.
    input_layer = Input(input_size)

    preprocessor = Lambda(data_preprocessor)(input_layer)

    base_model = model_name(weights = 'imagenet', include_top = False,
                input_shape = input_size)(preprocessor)
                
    avg = GlobalAveragePooling2D()(base_model)
    feature_extractor = Model(inputs = input_layer, outputs = avg)

    # Extract feature.
    feature_maps = feature_extractor.predict(ds, verbose=1)
    print('Feature maps shape: ', feature_maps.shape)
    return feature_maps

# RETURNING CONCATENATED FEATURES USING MODELS AND PREPROCESSORS
def get_concat_features(feat_func, models, preprocs, array):

    print(f"Beggining extraction with {feat_func.__name__}\n")
    feats_list = []

    for i in range(len(models)):
        
        print(f"\nStarting feature extraction with {models[i].__name__} using {preprocs[i].__name__}\n")
        # applying the above function and storing in list
        feats_list.append(feat_func(models[i], preprocs[i], array))

    # features concatenating
    final_feats = np.concatenate(feats_list, axis=-1)
    # memory saving
    del(feats_list, array)
    gc.collect()

    return final_feats

# DEFINING models and preprocessors imports 

from keras.applications.xception import Xception, preprocess_input #0.57
xception_preprocessor = preprocess_input

from keras.applications.resnet_v2 import ResNet152V2, preprocess_input 
resnext_preprocessor = preprocess_input


models = [ResNet152V2, Xception]    # InceptionV3, , InceptionResNetV2
preprocs = [resnext_preprocessor, xception_preprocessor] # , inception_preprocessor, , inc_resnet_preprocessor

'''
# save five train models 
def model_save():   
    for i in range (len(trained_models)):
        trained_models[i].save(data_dir+"/my_model"+str(i))
model_save()
'''

# load five models
trained_models = []

def model_load():
    for i in range (5):
        path = data_dir+"/models/my_model"+str(i)
        print('\nmodel path：'+path)
        trained_models.append(keras.models.load_model(path))
        print('Load model'+str(i)+' fin.')
model_load()

test_features = get_concat_features(get_valfeatures, models, preprocs, Xtesarr)

del(Xtesarr)
gc.collect()
print('Final feature maps shape', test_features.shape)

def predict(models, test_fea):
  y_pred_norm = models[0].predict(test_fea, batch_size = bath_size)/3
  for dnn in models[1:]:
      y_pred_norm += dnn.predict(test_fea, batch_size = bath_size)/3
  
  dict2 = {value:key for key, value in class_to_num.items()}
  pred_codes = np.argmax(y_pred_norm, axis = 1)
  result = pd.Series(pred_codes).map(dict2)
  return result

answer = predict(trained_models, test_features)
print(answer)

submission = np.array(pd.concat([pd.Series(test_images), answer], axis=1))
np.savetxt(data_dir+'/answer.txt', submission, fmt='%s')



