"""Decision Network for BrushBot"""


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

    def __init__(self, inputs, savefile, epochs):
        self.inputs = inputs
        self.savefile = savefile
        self.epochs = epochs

if __name__ == '__main__':
    dp = DataProcessor("relative_pos.txt", "pos.txt", "accel.txt", "gyro.txt")
    dp.load_data(3, False)
    sequences, next_sequences = dp.preprocess(10, 1)
    print(sequences, next_sequences)
