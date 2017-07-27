"""Decision Network for BrushBot"""

#from keras.models import load_model, Sequential
#from keras.layers import Dropout, LSTM, Activation, Dense
#from keras.optimizers import RMSprop


class DataProcessor(object):
    """A data processing class that allows for the loading of data and preprocessing for neural network"""

    def __init__(self, gyro_file, accelX_file, accelY_file, joy_file):
        self.gyro_file = gyro_file
        self.accelX_file = accelX_file
        self.accelY_file = accelY_file
        self.joy_file = joy_file
        self.accuracy = 3
        self.relative_pos = []
        self.delta_accelX = []
        self.delta_gyro = []
        self.delta_accelY = []
        self.times = []
        self.data = []
        self.sequences = []
        self.joys = []

    def load_data(self, accuracy, return_values=True):
        """Load data from textfile rounding it to desired decimal place. Returns a list of times, relative positions,
        changes in position, changes in acceleration, and changes in rotation."""
        self.accuracy = accuracy
        for line in open(self.joy_file, "r"):
            time, left, right = line.replace("\n", "").split(',')
            self.joys.append([left, right])
        for line in open(self.gyro_file, "r"):
            time, value = line.split(',')
            self.times.append(round(float(time), self.accuracy))
            self.delta_gyro.append(round(float(value), self.accuracy))
        for line in open(self.accelX_file, "r"):
            time, value = line.split(',')
            self.delta_accelX.append(round(float(value), self.accuracy))
        for line in open(self.accelY_file, "r"):
            time, value = line.split(',')
            self.delta_accelY.append(round(float(value), self.accuracy))
        if return_values:
            return self.times, self.delta_gyro, self.delta_accelX, self.delta_accelY, self.joys

    def preprocess(self):
        """Preprocess the data into sequences. Returns chunks of sequences and a list of next sequences"""
        for g, x, y in zip(self.delta_gyro, self.delta_accelX, self.delta_accelY):
            self.data.append([g, x, y])
        return self.data, self.joys, self.times


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

if __name__ == '__main__':
    dp = DataProcessor("logs/gyro.txt", "logs/accelX.txt", "logs/accelY.txt", "logs/joy.txt")
    times, delta_gyro, delta_accelX, delta_accelY, joys = dp.load_data(3, True)
    print(joys)