# -*- coding: utf-8 -*-
"""ProteinSolventAccessibilityCNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15VbqY-wxQhtJz8PUCcRpG3_xLFV2q09H
"""

#Import libraries
import numpy as np
from keras.utils import to_categorical
from keras import backend as K
import tensorflow as tf
from keras import losses 
from keras.callbacks import Callback
from keras.models import Model
from keras.layers.core import Dense, Dropout, Activation
from keras import layers,optimizers
from keras import regularizers
from keras.optimizers import Adam
from keras import metrics
import time
import tensorflow as tf
from random import randint
import matplotlib.pyplot as plt

# Dataset from Cull pdb for ICML2014
#dataset = gzip.open('cullpdb+profile_6133_filtered.npy.gz', 'rb')
dataset = np.load('data/cullpdb+profile_6133_filtered.npy')
print("Before: ",dataset.shape)
dataset = np.reshape(dataset, (dataset.shape[0], 700, 57))
print("After: ",dataset.shape)

print('Preparing dataset...dataset shape ',dataset.shape )
dataindex = range(30) # secondary structure => input
t_end_idx=int(dataset.shape[0]*0.8)#4800
v_idx = t_end_idx+ int(dataset.shape[0]*0.1)#5000

#np.random.seed(1234)
idx_arr = np.arange(dataset.shape[0])
np.random.shuffle(idx_arr)
traindataset = dataset[idx_arr,:,:]

print("traindataset.. ",traindataset.shape)
#print("traindataset unique ",np.unique(idx_arr).shape)
traindata = traindataset[:t_end_idx,:,dataindex]
trainlabel = traindataset[:t_end_idx,:,34:35] #considero solo la relative (33) 
valdata = traindataset[t_end_idx:v_idx,:,dataindex]
vallabel = traindataset[t_end_idx:v_idx,:,34:35]

traindata = np.concatenate((traindata, valdata), axis=0)
trainlabel = np.concatenate((trainlabel, vallabel), axis=0)

testdata = traindataset[v_idx:,:,dataindex]
testlabel = traindataset[v_idx:,:,34:35]

print("\n********Before:********\ntraindata.shape: ",traindata.shape,"\nvaldata.shape: ",valdata.shape,"\ntestdata.shape: ",testdata.shape,"\ntrainlabel.shape: ",trainlabel.shape,"\nvallabel.shape: ",vallabel.shape,"\ntestlabel.shape: ",testlabel.shape)

max_num_amino = 700

trainmask = dataset[:t_end_idx,:,30]* -1 + 1
valmask = dataset[t_end_idx:v_idx,:,30]* -1 + 1
testmask = dataset[v_idx:,:,30]* -1 + 1

trainvalmask = np.concatenate((trainmask, valmask), axis=0)


trainlabel = to_categorical(trainlabel,2)
testlabel = to_categorical(testlabel,2)
vallabel = to_categorical(vallabel,2)

#print(trainlabel[2,:,:])

train_tmp = []
train_lab_tmp = []
val_tmp = []
val_lab_tmp = []
test_tmp = []
test_lab_tmp = []

min_ratio = 0.05
max_ratio = 0.95
do_ratio = True

for i in range(valdata.shape[0]):
  p = valdata[i,:max_num_amino,:]
  pl = vallabel[i,:max_num_amino,:]
  num_amino = int(sum(valmask[i]))
  if(num_amino<=max_num_amino):
    ratio_first = (np.sum(pl[:num_amino,0])/num_amino)
    if do_ratio:
      if( min_ratio < ratio_first and ratio_first < max_ratio ):    
        val_tmp.append(p)
        pl[num_amino:,:]=[0,0]
        val_lab_tmp.append(pl)
    else:
      val_tmp.append(p)
      pl[num_amino:,:]=[0,0]
      val_lab_tmp.append(pl)

    
print('traindata.shape[0]' ,traindata.shape[0])
for i in range(traindata.shape[0]):
  p = traindata[i,:max_num_amino,:]
  pl = trainlabel[i,:max_num_amino,:]
  num_amino = int(sum(trainvalmask[i]))
  if(num_amino<=max_num_amino):
    ratio_first = (np.sum(pl[:num_amino,0])/num_amino)
    #print(i," - ",np.sum(pl[:num_amino,0]),' su ',num_amino,' => ',ratio_first)
    if do_ratio:
      if( min_ratio < ratio_first and ratio_first < max_ratio ):      
        train_tmp.append(p)
        pl[num_amino:,:]=[0,0]
        train_lab_tmp.append(pl)
    else:      
      train_tmp.append(p)
      pl[num_amino:,:]=[0,0]
      train_lab_tmp.append(pl)

for i in range(testdata.shape[0]):
  p = testdata[i,:max_num_amino,:]
  pl = testlabel[i,:max_num_amino,:]
  num_amino = int(sum(testmask[i]))
  if(num_amino<=max_num_amino):
    ratio_first = (np.sum(pl[:num_amino,0])/num_amino)
    if do_ratio:
      if( min_ratio < ratio_first and ratio_first < max_ratio ):    
        test_tmp.append(p)
        pl[num_amino:,:]=[0,0]
        test_lab_tmp.append(pl)
    else:    
      test_tmp.append(p)
      pl[num_amino:,:]=[0,0]
      test_lab_tmp.append(pl)

traindata = np.array(train_tmp).astype(float)
valdata = np.array(val_tmp).astype(float)
testdata = np.array(test_tmp).astype(float)
trainlabel = np.array(train_lab_tmp).astype(float)
vallabel = np.array(val_lab_tmp).astype(float)
testlabel = np.array(test_lab_tmp).astype(float)

#print(trainlabel[2,:,:])

print("\n********After:********\ntraindata.shape: ",traindata.shape,"\nvaldata.shape: ",valdata.shape,"\ntestdata.shape: ",testdata.shape,
      "\ntrainlabel.shape: ",trainlabel.shape,"\nvallabel.shape: ",vallabel.shape,"\ntestlabel.shape: ",testlabel.shape)


def proteinCategoricalCrossentropy(y_true,y_pred):
      
      loss = y_true * K.log(y_pred)      
      loss = -K.sum(loss, -1) #/ 2 # diviso il numero di classi => + una media 
      #print('loss ',loss)
      
      return loss
      #return losses.categorical_crossentropy(y_true, y_pred)


def weighted_accuracy(y_true, y_pred):
    #print(y_pred)
    
    #y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
    
    #print(y_pred)
    #print('input_layer->',input_layer)
    acc = K.sum(K.cast( K.equal(
                        K.argmax(y_true, axis=-1),
                        K.argmax((y_pred), axis=-1)
                    ),"float32") * K.sum(y_true, axis=-1)
                ) / K.sum(y_true)
    return acc
    
    #return tf.reduce_sum(tf.equal(tf.argmax(y_true,-1),tf.argmax(tf.cast(y_pred,"float32"),-1)) * tf.reduce_sum(y_true,-1)) / tf.reduce_sum(y_true)

train_accs = []
val_accs = []

class ProteinCallback(Callback):
  def __init__(self, eval_data):
      self.eval_data = eval_data
      
  def on_epoch_end(self, epoch, logs={}):
        x, y = self.eval_data
        #loss, acc = self.model.evaluate(x, y, verbose=0)
        #print('Testing loss: {}, weighted_accuracy: {}'.format(loss, acc))

num_epoche = 42
conv = 32
drop = 0
activation = 'tanh'
poolSize = 5
batchSize=32
validationSplit=0.1
#adam = Adam(lr=1e-3)
#sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
optimizer = 'adam'

input_layer = layers.Input(shape=(max_num_amino,len(dataindex)), name='input')

net = layers.Conv1D(conv,5, padding='same')(input_layer)

net = layers.Activation(activation)(net)

#act1 = layers.MaxPooling1D(pool_size=poolSize,strides=1,padding='same')(act1)

net = layers.Dropout(drop)(net)

net = layers.Conv1D(conv, 5, padding='same')(net)

net = layers.Activation(activation)(net)

net = layers.MaxPooling1D(pool_size=poolSize,strides=1,padding='same')(net)

net = layers.Dropout(drop)(net)

net = layers.Conv1D(conv, 5, padding='same')(net)

net = layers.Activation(activation)(net)

net = layers.MaxPooling1D(pool_size=poolSize,strides=1,padding='same')(net)

#pool3 = layers.Conv1D(128, 5, activation='relu', padding='same')(pool3)

net = layers.Dropout(drop)(net)

net = layers.Dense(conv)(net)
net = layers.Activation(activation)(net)
net = layers.Dropout(drop)(net)

output_layer = layers.Dense(2, activation="softmax", name='output')(net) 

model = Model(inputs=input_layer, outputs=output_layer)


model.compile(optimizer=optimizer,#rmsprop,adam,SGD,adamax
              #loss='categorical_crossentropy',
              loss=proteinCategoricalCrossentropy,
              metrics=[weighted_accuracy])

model.summary()
model_summary= (str(model.to_json()))
# Fit the model

time_start = time.time()

history = model.fit(traindata,trainlabel,epochs=num_epoche,verbose=2,batch_size=batchSize,#validation_split=validationSplit)
                    #callbacks=[ProteinCallback((testdata,testlabel))])
                    validation_data=(testdata,testlabel))
time_execution = time.time() - time_start
print("Fit time: ",time_execution)