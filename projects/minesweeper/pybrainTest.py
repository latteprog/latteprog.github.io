from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import time

def loadData(filename):
	fp = open(filename, "r")

	str = fp.readline()
	str = str.split()
	nums = [int(x) for x in str]

	dataCnt = nums[0]	
	inpSize = nums[1]
	outSize = nums[2]

	res = SupervisedDataSet(inpSize, outSize)

	for i in range(dataCnt):
		str = fp.readline()
		str = str.split()
		nums = [float(x) for x in str]

		res.addSample(nums[:inpSize], nums[inpSize:])

	return res

def loadNetwork(filename):
	fp = open(filename, "r")
	res = pickle.load(fp)
	fp.close()

	return res

def saveNetwork(network, filename):
	fp = open(filename, "w")
	pickle.dump(network, fp)
	fp.close()

net = loadNetwork("beginner_vector_4x4_30.txt")

trainDs = loadData("beginner_vector_4x4_train.txt")
testDs = loadData("beginner_vector_4x4_test.txt")

trainer = BackpropTrainer(net, trainDs, learningrate = 0.01, momentum = 0.99)

print "start"
correct = 0
incorrect = 0

tic = time.clock()

for i in range(len(testDs)):
	res = net.activate(testDs['input'][i]).tolist()
	if(int(testDs['target'][i][res.index(max(res))]) == 1):
		correct += 1
	else:
		incorrect += 1


print correct, incorrect

toc = time.clock()
