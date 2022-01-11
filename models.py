import tensorflow as tf
import keras
from keras.layers import Dense
from system_constants import SystemConstants


class ControlBarrierFunction:
    def __init__(self):
        self.system_constants = SystemConstants()
        self.num_neurons = [10, 15, 10]
        self.activation_functions = ['relu', 'relu', 'relu', 'sigmoid']
        self.model = keras.Sequential()
        self.model.add(Dense(12, input_dim=self.system_constants.num_inputs, activation='relu'))
        assert len(self.num_neurons) == len(self.activation_functions), 'Wrong length of neurons and Activation ' \
                                                                        'Functions -> Control Barrier Function'
        for count in range(len(self.num_neurons)):
            self.model.add(Dense(self.num_neurons[count], activation=self.activation_functions[count]))

    def model_fit(self, state, expected_output):
        self.model.fit(state, expected_output, epochs=self.system_constants.num_epochs,
                       batch_size=self.system_constants.batch_size)

    def model_evaluate(self, state, expected_output):
        _, accuracy = self.model.evaluate(state, expected_output, verbose=0)


class NNController:
    def __init(self):
        self.system_constands = SystemConstants()
        self.num_neurons = [10, 20, 50, 30, 15, 17]
        self.activation_functions = ['relu', 'relu', 'relu', 'relu', 'relu', 'relu']
        self.model = keras.Sequential()
        self.model.add(Dense(12, input_dim=self.system_constands.num_inputs, activation='relu'))
        assert len(self.num_neurons) == len(self.activation_functions), 'Wrong length of neurons and Activation ' \
                                                                        'Functions -> NNController'
        for count in range(len(self.num_neurons)):
            self.model.add(Dense(self.num_neurons[count], activation=self.activation_functions[count]))

    def model_fit(self, state, expected_output):
        self.model.fit(state, expected_output, epochs=self.system_constants.num_epochs,
                       batch_size=self.system_constants.batch_size)

    def model_evaluate(self, state, expected_output):
        _, accuracy = self.model.evaluate(state, expected_output, verbose=0)
