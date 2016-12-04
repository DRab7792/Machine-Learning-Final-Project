from __future__ import print_function
import csv
import math
import random
from class_student import Student

# Parse the data from one of the csv files
def parseData(fileName):
	# Read the training data from the file
	data = []
	file = open('../data/' + fileName + '.csv', 'rb')
	reader = csv.reader(file)

	# Save the data
	header = True
	for row in reader:
		if not header:
			newStudent = Student()
			newStudent.parse(row)
			data.append(newStudent)
		else:
			header = False

	return data

# Print out the test students
def printArr(arr):
	for cur in arr:
		print (cur)


# Divide an array of student objects by a property and value
def divideSet(arr, prop, value):
	splitFunction = None
	if (isinstance(value, int) or isinstance(value, float)):
		splitFunction = lambda cur:getattr(cur,  prop) >= value
	else: 
		splitFunction = lambda cur:getattr(cur,  prop) == value

	set1 = [cur for cur in arr if splitFunction(cur)]
	set2 = [cur for cur in arr if not splitFunction(cur)]
	return (set1, set2)

# Get unique counts of performance of user for goal objects in array
def uniqueCounts(arr):
	res = {}

	for cur in arr:
		curScore = getattr(cur,  "goalScore")
		if curScore not in res: res[curScore] = 0
		res[curScore] += 1

	return res

# Calculate the entropy
def entropy(arr):
	from math import log
	log2  = lambda x: log(x)/log(2)
	res = uniqueCounts(arr)

	# Calculate the entropy
	ent = 0.0
	for r in res.keys():
		p = float(res[r]) / len(arr)
		ent = ent - p * log2(p)

	return ent

def formStatistics(matrix, roc):
	stats = {
		"accuracy": 0,
		"fpr": 0,
		"tpr": 0
	}

	stats["accuracy"] = float(matrix["tp"] + matrix["tn"]) / (matrix["tp"] + matrix["tn"] + matrix["fp"] + matrix["fn"])

	stats["accuracy"] *= 100

	stats["tpr"] = float(matrix["tp"]) / (matrix["tp"] + matrix["fn"])

	stats["fpr"] = float(matrix["fp"]) / (matrix["fp"] + matrix["tn"])

	# Calculate the area under the curve
	if len(roc) == 1:
		# No false positives occurred, default to a ROC curve area of 0.5?
		stats["rocArea"] = 0.5
	else:
		area = 0.0
		lastY = 0.0
		lastX = 0.0
		for cur in roc:
			if cur[1] == lastY:
				area += (cur[0] - lastX) * lastY
			lastX = cur[0]
			lastY = cur[1]
		stats["rocArea"] = area

	return stats

# Find the mean of an array
def calcMean(arr):
	return sum(arr) / float(len(arr))

# Find the standard deviation of an array
def calcStdDev(arr):
	avg = calcMean(arr)
	variance = sum([pow(x - avg, 2) for x in arr]) / float(len(arr) - 1)
	return math.sqrt(variance)

# Split data into test data and training data
def splitData(arr, ratio):
	trainSize = int(len(arr) * ratio)
	trainSet = []
	copy = list(arr)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return trainSet, copy

# Display statistics with labels
def printStats(stats):
	statsMap = {
		"tn": "True Negatives",
		"fp": "False Positives",
		"fn": "False Negatives",
		"tp": "True Positives",
		"tpr": "True Positive Rate",
		"fpr": "False Positive Rate",
		"rocArea": "Area Under ROC Curve",
		"accuracy": "Accuracy"
	}

	for cur in stats.keys():
		end = ""
		val = stats[cur]
		if isinstance(val, float):
			val = round(val, 5)
		if (cur == "accuracy"):
			end = "%"
		print (statsMap[cur] + ": " + str(val) + end)