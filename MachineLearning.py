import random
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout,TimeDistributed
from keras.layers import LSTM, BatchNormalization, GRU
from keras.models import load_model
from keras.optimizers import RMSprop
import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
random.seed(10)

class DecisionNetwork(object):

    def __init__(self,numInputs,numOutputs,inputs,outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.numInputs = numInputs
        self.numOutputs = numOutputs

    def build(self, step,length):
        self.length = length
        self.step = step
        self.rotChanges = self.inputs
        self.motorPower = self.outputs

        print(np.array(self.rotChanges).shape)
        print(np.array(self.motorPower).shape)

        self.model = Sequential()
        self.model.add(LSTM(50, input_dim =3, activation='relu', return_sequences=True))
        self.model.add(LSTM(100, return_sequences=False))
        self.model.add(Dense(1, activation='linear'))
        print(self.model.input_shape)
        self.model.summary()
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

    def run(self, iterations,X_train,X_test,y_train,y_test,useModel=False):
        self.iterations = iterations
        if useModel == False:
            for i in range(self.iterations):
                self.model.fit(X_train,y_train,batch_size=100,epochs=1)
                #self.model.save('n.h5')
            score = self.model.evaluate(X_test, y_test, verbose=0)
            print('Test score:', score[0])
            print('Test accuracy:', score[1])
        else:
            self.model = load_model('n.h5')
            for i in range(self.iterations):
                self.model.fit(X_train,y_train,batch_size=100,epochs=1,validation_data=(X_test,y_test),validation_split=0.1)
                self.model.save('n.h5')
            score = self.model.evaluate(X_test, y_test, verbose=0)
            print('Test score:', score[0])
            print('Test accuracy:', score[1])

    def sample(self,predictions, temp=1.0, useModel=False):
        if useModel == True:
            self.model = load_model('n.h5')
            print(self.model.predict(predictions))

def train_test_split(X,Y, test_size=0.15):
    #    This just splits data to training and testing parts
    X = np.array(X)
    Y = np.array(Y)
    ntrn = round(X.shape[0] * (1 - test_size))
    perms = np.random.permutation(X.shape[0])
    X_train, Y_train = X.take(perms[0:ntrn],axis=0), Y.take(perms[0:ntrn],axis=0)
    X_test, Y_test = X.take(perms[ntrn:],axis=0),Y.take(perms[ntrn:],axis=0)
    return X_train, X_test, Y_train, Y_test

if __name__ == "__main__":
    #Generate structured data with noise
    # [motorPower1, motorPower2]
    X = []

    # [rotation, distance(cm), acceleration]
    y = []

    for i in range(-255, 256, 1):
        for j in range(-255, 256, 1):
            rot = 0
            X.append([i, j])

            # Go through rotations
            if abs(i) == abs(j):
                rot = 0
            elif i == 0 and j < 0:
                rot = j
            elif i == 0 and j > 0:
                rot = -j
            elif i > 0 and j == 0:
                rot = i
            elif i < 0 and j == 0:
                rot = -i
            elif i > 0 and j < 0:
                if abs(i) < abs(j):
                    rot = j + i
                else:
                    rot = i + j
            elif i > 0 and j > 0:
                if abs(i) < abs(j):
                    rot = j - i
                else:
                    rot = i - j
            elif i < 0 and j < 0:
                if abs(i) < abs(j):
                    rot = j - i
                else:
                    rot = i - j

            elif i < 0 and j > 0:
                if abs(i) < abs(j):
                    rot = j + i
                else:
                    rot = i + j
            if rot == 0:
                y.append([rot,0,rot**2])
            else:
                y.append([rot, rot//3, rot//2])
    X = [i for i in range(511**2)]
    nn = DecisionNetwork(1,2,y,X)
    nn.build(1, 100)
    X_train, X_test, y_train, y_test = train_test_split(np.array(nn.rotChanges).reshape(len(nn.rotChanges),1,3),nn.motorPower,test_size=0.8)
    nn.run(10000,X_train,X_test,y_train,y_test)
    nn.sample(X_test[:10])
