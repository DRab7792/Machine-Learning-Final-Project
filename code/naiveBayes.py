from __future__ import print_function
from class_student import Student
from function_util import *

attrs = ["stg", "scg", "stro", "uns", "lpr"]

# Separate students by goal score (pass/fail)
def separateByClass(arr):
	separated = {}
	for cur in arr:
		curClass = getattr(cur, 'goalScore')
		if (curClass not in separated):
			separated[curClass] = []
		separated[curClass].append(cur)

	return separated

# Get statistics for a set of students
def summarize(arr):
	summaries = {}
	for curAttr in attrs:
		attrVals = []
		for curStudent in arr:
			attrVals.append(getattr(curStudent, curAttr))
		summaries[curAttr] = (calcMean(attrVals), calcStdDev(attrVals))
	return summaries

# Get statistics for each class in the training data
def summarizeByClass(arr):
	classes = separateByClass(arr)
	summaries = {}
	for classVal, instances in classes.iteritems():
		summaries[classVal] = summarize(instances)
	return summaries

# Calculate probability that an attribute value belongs in a class
def calcProbability(val, mean, stdDev):
	exponent = math.exp(-(math.pow(val - mean, 2)/(2 * math.pow(stdDev, 2))))
	return (1 / (math.sqrt(2 * math.pi) * stdDev)) * exponent

# Use the attribute summaries to calculate the probability of a class for a student
def calcClassProbabilities(summaries, student):
	probabilities = {}
	for classVal, classSummaries in summaries.iteritems():
		probabilities[classVal] = 1
		for curAttr in attrs:
			mean, stdDev = classSummaries[curAttr]
			val = getattr(student, curAttr)
			probabilities[classVal] *= calcProbability(val, mean, stdDev)
	return probabilities

# Use the attribute summaries to predict the class of a student
def predictStudentClass(summaries, student):
	probabilities = calcClassProbabilities(summaries, student)
	bestLabel, bestProb = None, -1
	for classVal, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classVal
	return bestLabel

# Run test data through prediction model
def predictStudents(summary, arr):
	# Form confusion matrix
	matrix = {
		"tp": 0,
		"tn": 0,
		"fn": 0,
		"fp": 0
	}
	roc = [[0.0, 0.0]]

	# 
	for cur in arr:
		prediction = predictStudentClass(summary, cur)
		actual = getattr(cur, "goalScore")

		if actual == prediction and prediction == "Pass":
			matrix["tp"] += 1
		elif actual == prediction and prediction == "Fail":
			matrix["tn"] += 1
		elif actual != prediction and prediction == "Pass":
			roc.append([matrix["fp"], matrix["tp"]])
			matrix["fp"] += 1
			roc.append([matrix["fp"], matrix["tp"]])
		elif actual != prediction and prediction == "Fail":
			matrix["fn"] += 1

	# Convert to rates
	for cur in roc:
		if matrix["fp"] != 0:
			cur[0] = float(cur[0]) / matrix["fp"]
		else:
			cur[0] = 0.0

		if matrix["tp"] != 0:
			cur[1] = float(cur[1]) / matrix["tp"]
		else:
			cur[1] = 0.0

	return (matrix, roc)

# Display summaries with labels
def printSummaries(summary):
	for classVal in summary.keys():
		attrs = summary[classVal]
		print (classVal + ":")
		for curAttr in attrs.keys():
			print ("  " + curAttr + ":")
			print ("    Mean: " + str(attrs[curAttr][0]))
			print ("    Std Deviation: " + str(attrs[curAttr][1]))
	return;

def main():
	list1 = parseData("training")
	list2 = parseData("test")
	data = list1 + list2
	splitRatio = 0.67

	trainingData, testData = splitData(data, splitRatio)
	summary = summarizeByClass(trainingData)
	(confusionMatrix, rocCurve) = predictStudents(summary, testData)
	statistics = formStatistics(confusionMatrix, rocCurve)
	
	print ("Summaries By Class")
	print ("------------------")
	printSummaries(summary)
	print ("\n\n")
	print ("Confusion matrix from test data")
	print ("-------------------------------")
	printStats(confusionMatrix)
	print ("\n\n")
	print ("Statistics from test data")
	print ("-------------------------")
	printStats(statistics)

main()