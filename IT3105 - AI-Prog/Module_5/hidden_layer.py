import numpy

import theano
from theano import pp
import theano.tensor as T

class HiddenLayer(object):
    def __init__(self, num_weight_in,
                 num_hidden_units, layer_weights=None, bias_weights=None,
                 activation=T.tanh):

        #self.input = input
        print("Creatingh layers: #input: ",num_weight_in," #units: ",num_hidden_units)
        self.activation = activation
        self.activation_function = self.init_activation(activation)
        self.propagate_function = self.init_propagate_function()
        self.output_delta_function = self.init_output_delta_function()


        if layer_weights is None:
            layer_weights = self.init_weights(num_weight_in, num_hidden_units)

        if bias_weights is None:
            bias_weights = numpy.zeros((num_hidden_units,), dtype=theano.config.floatX)

        self.layer_weights = layer_weights
        self.bias_weights = bias_weights

        self.output = 0
        

    def init_weights(self, num_weight_in, num_hidden_units):
        #The tutorial in ANN in Theano suggests that the
        #initial random weights should be uniformly distributed
        #in the range of sqrt(6. / (#units in ith layer + #units in i-th layer))
        sum_fan_units = num_weight_in + num_hidden_units
        weight_values = numpy.asarray(
                numpy.random.uniform(
                    low = - numpy.sqrt(6. / (sum_fan_units)),
                    high = numpy.sqrt(6. / (sum_fan_units)),
                    size = (num_weight_in, num_hidden_units)
                ),
                dtype=theano.config.floatX
            )
        #Similary it suggests that the random weights if
        #the activation function is a sigmoid should be
        #4 * the value of the tanh activation
        if self.activation == theano.tensor.nnet.sigmoid:
            weight_values *= 4

        return weight_values

    def init_propagate_function(self):
        x = T.dvector()
        y = T.dmatrix()
        b = T.dvector()
        z = T.dot(x, y) + b
        f = theano.function([x,y,b], z)
        return f

    def init_activation(self, activation):
        x = T.dvector()
        z = activation(x)
        f = theano.function([x], z)
        return f

    def init_output_delta_function(self):
        y = T.dscalar('example_value')
        a = T.dscalar('actual_value')
        dg = T.grad(self.activation)
        delta = dg(a) * (y - a)
        f = theano.function([a,y], delta)
        return f
        

    def propagate(self, input_values):
        print("prop")
        #lin_output = T.dot(input_values, self.layer_weights) + self.bias_weights
        lin_output = self.propagate_function(input_values, self.layer_weights, self.bias_weights)
        self.output = self.activation_function(lin_output)
        self.output = (
            lin_output if self.activation is None
            else self.activation_function(lin_output)
        )
        


        

    
        
#hl = HiddenLayer([3,2], 2, 2)
#h2 = HiddenLayer([3,2], 2, 2)
#print("output: ", hl.output)
    
