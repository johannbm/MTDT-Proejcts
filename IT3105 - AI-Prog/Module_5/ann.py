import hidden_layer as hl
import theano
import theano.tensor as T
import numpy
from mnist_basic import * as mb

class Ann(object):

    def __init__(self, hidden_layer_data,
                  activation = T.tanh, learning_rate = 0.001):

        #Initialize all the hidden layers given by hidden_layer_data
        #where each element gives #units at layer given by index i
        self.hidden_layers = []
        for i in range(len(hidden_layer_data)):
            num_input = 5 if i == 0 else hidden_layer_data[i-1]
            self.hidden_layers.append(hl.HiddenLayer(num_input,hidden_layer_data[i]))



    def propagate(self, input_values):
        for l in self.hidden_layers:
            l.propagate(input_values)
            input_values = l.output
        print("final layer values : ", input_values)

l,i = mb.load_mnist()
#a = Ann([20,50, 30])
#a.propagate([3,2,2,1,2])
            
        
        
