import numpy

import theano
from theano import pp
import theano.tensor as T

class HiddenLayer(object):
    def __init__(self, num_weight_in,
                 num_hidden_units, layer_weights=None, bias_weights=None,
                 activation=T.tanh):

        print("Creating layers: #input: ",num_weight_in," #units: ",num_hidden_units)
        
        self.activation = activation
        self.activation_function = self.init_activation(activation)
        self.propagate_function = self.init_propagate_function()
        self.output_delta_function = self.init_output_delta_function()
        self.update_weights_function = self.init_update_weights()
        self.hidden_error_function = self.init_backpropagation_error()


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
                    size = (num_hidden_units, num_weight_in)
                ),
                dtype=theano.config.floatX
            )
        #Similary it suggests that the random weights if
        #the activation function is a sigmoid should be
        #4 * the value of the tanh activation
        if self.activation == theano.tensor.nnet.sigmoid:
            weight_values *= 4

        return weight_values

    def init_update_weights(self):
        x = T.dmatrix('weights')
        y = T.dvector('outputs')
        d = T.dvector('delta_error')
        l = T.dscalar('learning rate')
        z = T.outer(d.T, y)*l + x
        f = theano.function([x, y, d, l], z, on_unused_input='ignore')
        return f

    def init_propagate_function(self):
        x = T.dvector('input')
        y = T.dmatrix('weights')
        b = T.dvector('bias')
        z = T.dot(y, x) + b
        f = theano.function([x,y,b], z)
        return f

    def init_activation(self, activation):
        x = T.dvector()
        z = activation(x)
        f = theano.function([x], z)
        return f

    def init_output_delta_function(self):
        y = T.dvector('example_value')
        a = T.dvector('actual_value')
        s = T.sum(self.activation(a))
        dg = T.grad(s, a)
        delta = dg * (y - a)
        f = theano.function([a, y], delta)
        return f

    def init_backpropagation_error(self):
        o = T.dvector('node_value')
        w = T.dmatrix('weights')
        prev_d = T.dvector('previous deltas')
        s = T.sum(self.activation(o))
        dg = T.grad(s,o)
        delta = dg * T.dot(prev_d, w)
        f = theano.function([o, w, prev_d], delta)
        return f

    def calculate_hidden_error(self, prev_error, o):
        return self.hidden_error_function(o, self.layer_weights, prev_error)
        #print("PREV ERROR: ",prev_error)
        #print("OUTPUT: ",o)
        #print("WEIGHTS: ",self.layer_weights)
        #print("TRANSPOSED: ", numpy.transpose(self.layer_weights))
        #for i in range(len(o)):
         #   errors.append(
          #      self.hidden_error_function(o[i],
           #                                 numpy.transpose(self.layer_weights)[i],
            #                                prev_error)
              #  )
        #print("NEW ERROR: ", errors)
        #return errors
        

    def update_weights(self, error, next_output, learning_rate=0.01):
        #print(self.layer_weights)
        #print(error)
        #print(next_output)
        self.layer_weights = self.update_weights_function(self.layer_weights, next_output, error, learning_rate)
        #print(self.layer_weights)
        #print("---")

    def propagate(self, input_values):
        #lin_output = T.dot(input_values, self.layer_weights) + self.bias_weights
        #print(self.layer_weights)
        #print(self.bias_weights)
        lin_output = self.propagate_function(input_values, self.layer_weights, self.bias_weights)
        #self.output = self.activation_function(lin_output)
        self.output = (
            lin_output if self.activation is None
            else self.activation_function(lin_output)
        )

#hl = HiddenLayer(2,2,[[0.1,0.2],[0.3,0.4]])
#hl.update_weights([-0.0897, 0.1033], [1,2])
#hl.output = [0.6043, 0.7615]
#res = hl.calculate_hidden_error([-0.1187, -0.1489])
#print(res)
        

    
