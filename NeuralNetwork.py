from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout,TimeDistributed
from keras.layers import LSTM, BatchNormalization, GRU
from keras.models import load_model
#from sklearn.cross_validation import train_test_split
from keras.optimizers import RMSprop
import numpy as np
import matplotlib.pyplot as plt
import sys
import random
import math
random.seed(10)

class DecisionNetwork(object):

    def __init__(self,numInputs,numOutputs,inputs):
        self.inputs = inputs
        self.numInputs = numInputs
        self.numOutputs = numOutputs

    def build(self, step,length):
        self.length = length
        self.step = step
        self.movements = []
        self.next_movements = []
        for i in range(0, len(self.inputs)-length, step):
            self.movements.append(self.inputs[i:i+length])
            self.next_movements.append(self.inputs[i+length])
        self.model = Sequential()
        self.model.add(LSTM(100, input_shape=(None,3),return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(100, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(3))
        self.model.add(Activation('linear'))
        print(self.model.input_shape)
        self.model.summary()
        self.optimizer = RMSprop(lr=0.01)
        self.model.compile(loss='mse', optimizer=self.optimizer, metrics=['accuracy'])

    def run(self, iterations,X_train,X_test,y_train,y_test,useModel=False):
        self.iterations = iterations
        if useModel == False:
            for i in range(self.iterations):
                self.model.fit(X_train,y_train,batch_size=100,epochs=1,validation_data=(X_test,y_test),validation_split=0.1)
                self.model.save('m.h5')
            score = self.model.evaluate(X_test, y_test, verbose=0)
            print('Test score:', score[0])
            print('Test accuracy:', score[1])
        else:
            self.model = load_model('m.h5')
            for i in range(self.iterations):
                self.model.fit(X_train,y_train,batch_size=100,epochs=1,validation_data=(X_test,y_test),validation_split=0.1)
                self.model.save('m.h5')
            score = self.model.evaluate(X_test, y_test, verbose=0)
            print('Test score:', score[0])
            print('Test accuracy:', score[1])

    def sample(self,predictions, temp=1.0, useModel=False):
        if useModel == True:
            self.model = load_model('m.h5')
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
    inputs = []
    for i in range(30000):
        gyro = 10*((math.sin(i)**3)-6*(math.cos(i)*(math.sin(i)**2))+math.sin(i))+random.uniform(-2,2)
        pos = (math.cos(i)**2)*math.sin(i)+random.uniform(-1,1)
        accel = (math.cos(i)**3)+math.sin(i)+random.uniform(-0.5,0.5)
        inputs.append([gyro,pos,accel])

    nn = DecisionNetwork(1,2,inputs)
    nn.build(1, 100)
    X_train, X_test, y_train, y_test = train_test_split(nn.movements,nn.next_movements)
    nn.run(100,X_train,X_test,y_train,y_test)
    nn.sample(X_test[:10])