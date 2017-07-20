"""Decision Network for BrushBot"""

from keras.models import load_model, Sequential
from keras.layers import Dropout, LSTM, Activation, Dense
from keras.optimizers import RMSprop


class DataProcessor(object):
    """A data processing class that allows for the loading of data and preprocessing for neural network"""

    def __init__(self, relative_position_file, position_file, accel_file, gyro_file):
        self.relative_position_file = relative_position_file
        self.position_file = position_file
        self.gyro_file = gyro_file
        self.accel_file = accel_file
        self.accuracy = 3
        self.relative_pos = []
        self.delta_pos = []
        self.delta_gyro = []
        self.delta_accel = []
        self.times = []
        self.data = []
        self.sequences = []
        self.next_sequences = []

    def load_data(self, accuracy, return_values=True):
        """Load data from textfile rounding it to desired decimal place. Returns a list of times, relative positions,
        changes in position, changes in acceleration, and changes in rotation."""
        self.accuracy = accuracy
        for line in open(self.relative_position_file, "r"):
            time, value = line.split(',')
            self.relative_pos.append(round(float(value), self.accuracy))
        for line in open(self.position_file, "r"):
            time, value = line.split(',')
            self.times.append(round(float(time), self.accuracy))
            self.delta_pos.append(round(float(value), self.accuracy))
        for line in open(self.accel_file, "r"):
            time, value = line.split(',')
            self.delta_accel.append(round(float(value), self.accuracy))
        for line in open(self.gyro_file, "r"):
            time, value = line.split(',')
            self.delta_gyro.append(round(float(value), self.accuracy))
        if return_values:
            return self.times, self.relative_pos, self.delta_pos, self.delta_accel, self.delta_gyro

    def preprocess(self, sequence_length, step):
        """Preprocess the data into sequences. Returns chunks of sequences and a list of next sequences"""
        for r, p, a, g in zip(self.relative_pos, self.delta_pos, self.delta_accel, self.delta_gyro):
            self.data.append([r, p, a, g])
        for i in range(0, len(self.data) - sequence_length, step):
            self.sequences.append(self.data[i:i + sequence_length])
            self.next_sequences.append(self.data[i + sequence_length])
        return self.sequences, self.next_sequences


class DecisionNetwork(object):
    """Decision Network that guides BrushBot's actions."""

    def __init__(self, savefile):
        self.savefile = savefile
        self.model = None
        self.optimizer = None

    def create_model(self, inputs, outputs, epochs, load=False):
        if load:
            self.load_model()
        else:
            self.inputs = inputs
            self.outputs = outputs
            self.epochs = epochs
            self.model = Sequential()
            self.model.add(LSTM(100, input_shape=(None, len(self.inputs[0][0])), return_sequences=True))
            self.model.add(Dropout(0.2))
            self.model.add(LSTM(100, return_sequences=False))
            self.model.add(Dropout(0.2))
            self.model.add(Dense(len(self.outputs[0])))
            self.model.add(Activation('linear'))
            print(self.model.input_shape)
            self.model.summary()
            self.optimizer = RMSprop(lr=0.01)
            self.model.compile(loss='mse', optimizer=self.optimizer, metrics=['accuracy'])

    def load_model(self):
        self.model = load_model(self.savefile)

    def save_model(self):
        self.model.save(self.savefile)

    def train_model(self, validate=False):
        for i in range(self.epochs):
            if validate:
                pass
            else:
                self.model.fit(self.inputs, self.outputs, batch_size=100, epochs=1)
                self.save_model()

    def predict(self, to_predict):
        return self.model.predict(to_predict)
