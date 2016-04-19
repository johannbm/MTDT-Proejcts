import os
from random import shuffle

def load_training_data(type="training"):
	path = "/Users/Johannes/Dropbox/MTDT/Host 2015/AI_PROG/Module_6/data_human/" + type + "/"
	features = []
	labels = []
	
	
	for file in os.listdir(path):
		data = [line.strip() for line in open(path + file, 'r')]
		#shuffle(data)
		for line in data:
			l = line.split(" ")
			temp_features = []
			for i in range(len(l)):
				if i < 16:
					temp_features.append(eval(l[i]))
				else:
					labels.append(eval(l[i])-1)
			features.append(temp_features)
		
	return features, labels
	