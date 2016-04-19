#from hidden_layer import *
import theano
import theano.tensor as T
import numpy
import data_loader as dl
import time
from ann import *
from preprocessor import *

#Features are in the range [0,255]
def scale_features(features):
    for f in features:
        for i in range(len(f)):
            f[i] *= (1/9)


def generate_example_output(label):
    example_output = [0.1] * 4
    example_output[label] = 0.9
    return example_output

def test(a):
	test_features, test_labels = dl.load_training_data("testing")
	test_features = preprocess(test_features)

	correct_counter = 0
	wrong_counter = 0
	for i in range(len(test_features)):
		res = a.test_case(test_features[i])
		if res == test_labels[i]:
			correct_counter += 1
		else:
			wrong_counter += 1

	return getPercentage(correct_counter, wrong_counter)


def train(a):
    global f
    
    features, labels = dl.load_training_data()
    features = preprocess(features)

    correct = 0
    fail = 0
    iteration = 0
    
    while(True):
        writeLog(["ITERATION: #" , str(iteration) , "\n"])
        print("iteration; ", iteration)
        for i in range(len(labels)):
            if i % 200 == 0:
                print(i)
            a.propagate(features[i], labels[i])
            a.backpropagate(features[i], generate_example_output(labels[i]))
        #print(a.correct)
        writeLog(["TRAINING: " , getPercentage(a.correct, a.fail) , "\n"])
        #print("TRAINING: " , getPercentage(a.correct, a.fail) , "\n")
        res = test(a)
        #print("TESTING: ",res)
        writeLog(["TESTING: " , res , "\n"])
        iteration += 1
        if (iteration > 15):
            break
        else:
            a.correct = 0
            a.fail = 0

def writeLog(l):
    f = open('log', 'a')
    f.write("".join(l))
    f.close()

def getPercentage(s, f):
    tot = s + f
    res = s / tot
    return str(res) + " %" 



#a = Ann([50, 40], 4, learning_rate = 0.025)
#train(a)




















    
