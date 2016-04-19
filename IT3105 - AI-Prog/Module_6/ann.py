#import hidden_layer as hl
from hidden_layer import *
import theano
import theano.tensor as T
import numpy
import time

class Ann(object):

    def __init__(self, hidden_layer_data, num_output_nodes,
                  activation = T.tanh, learning_rate = 0.001):

        self.learning_rate = learning_rate
        #Initialize all the hidden layers given by hidden_layer_data
        #where each element gives #units at layer given by index i
        self.hidden_layers = []
        for i in range(len(hidden_layer_data)):
            num_input = 16 if i == 0 else hidden_layer_data[i-1]
            self.hidden_layers.append(HiddenLayer(num_input,hidden_layer_data[i]))


        #Add output layer
        self.hidden_layers.append(HiddenLayer(hidden_layer_data[-1], num_output_nodes))

        self.correct = 0
        self.fail = 0



    def propagate(self, input_values, label):
        #Propagate forward
        res = self.propagate_forward(input_values)
        if res == label:
            self.correct += 1
        else:
            self.fail += 1
        #Backpropagate
        #self.backpropagate()
        

    def propagate_forward(self, input_values, get_all = False):
        for l in self.hidden_layers:
            l.propagate(input_values)
            input_values = l.output
        #print(input_values)
        if (get_all):
            return input_values
        return numpy.ndarray.argmax(input_values)

    def backpropagate(self, input_values, label_values):
        prev_delta = self.backpropagate_output_layer(label_values)
        #print("out delta: ", prev_delta)
        self.backpropagate_hidden_layers(prev_delta, input_values)
    

    def backpropagate_output_layer(self, example_output):
        #Last layer in hidden_layers is the output layer
        output_layer = self.hidden_layers[-1]
        actual = output_layer.output
        #output_deltas = [output_layer.output_delta_function(actual[i], example_output[i]) for i in range(10)]
        output_deltas = output_layer.output_delta_function(actual, example_output)
        #print("IN: ", actual)
        #print("ACTUAL OUTPUT: ", actual)
        #print("EXAMPLE: ", example_output)
        #update weights
        #output_layer.update_weights(output_deltas)
        return output_deltas

    def backpropagate_hidden_layers(self, previous_delta, input_values):
        #Update outputlayer weights
        #output_layer = self.hidden_layers[-1]
        
        previous_layer = self.hidden_layers[-1]
        previous_layer.delta = previous_delta
        for i in range(len(self.hidden_layers)-2,-1,-1):
            current_layer = self.hidden_layers[i]
            #previous_layer.update_weights(previous_delta, current_layer.output, self.learning_rate)
            
            previous_delta = previous_layer.calculate_hidden_error(previous_delta, current_layer.output)
            current_layer.delta = previous_delta
            previous_layer = current_layer

        #Update first layer
        ai = input_values
        for l in self.hidden_layers:
            l.update_weights(l.delta, ai, self.learning_rate)
            ai = l.output
        #self.hidden_layers[0].update_weights(previous_delta, input_values, self.learning_rate)
            

    def test_case(self, input_values):
        return self.propagate_forward(input_values)
        #return output.index(max( self.hidden_layers[-1].output))
    





