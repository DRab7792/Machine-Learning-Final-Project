from __future__ import print_function
from class_student import Student
from function_util import *

attrs = ["stg", "scg", "stro", "uns", "lpr"]

#Tree node class
class decisionNode:
	def __init__(self, attr = -1, value = None, results = None, tb = None, fb = None):
		self.attr = attr
		self.value = value
		self.results = results
		self.tb = tb
		self.fb = fb

# Build the decision tree
def buildTree(arr, scoref = entropy):
	# Check the length of the array
	if len(arr) == 0:
		return decisionNode()

	currentScore = scoref(arr)

	# Track the best criteria
	bestGain = 0.0
	bestCriteria = None
	bestSets = None

	for curAttr in attrs:
		# Get all values of the current attribute
		attrVals = {}
		for cur in arr:
			val = getattr(cur, curAttr)
			attrVals[val] = 1

		for val in attrVals.keys():
			# Divide set by each value
			(set1,set2) = divideSet(arr, curAttr, val)

			p = float(len(set1)) / len(arr)
			gain = currentScore - p * scoref(set1) - (1 - p) * scoref(set2)

			if (gain > bestGain) and len(set1) > 0 and len(set2) > 0:
				bestGain = gain
				bestCriteria = (curAttr, val)
				bestSets = (set1, set2)

	if bestGain > 0:
		trueBranch = buildTree(bestSets[0])
		falseBranch = buildTree(bestSets[1])
		return decisionNode(attr = bestCriteria[0], value = bestCriteria[1], tb = trueBranch, fb = falseBranch)
	else:
		return decisionNode(results = uniqueCounts(arr))

def printTree(tree, indent = ''):
	if (tree.results != None):
		print (str(tree.results))
	else:
		print (str(tree.attr) + ':' + str(tree.value) + '? ')
		print (indent+'T->', end=" ")
		printTree(tree.tb, indent+'  ')
		print (indent+'F->', end=" ")
		printTree(tree.fb, indent+'  ')

# Recursively search through tree
def execTree(student, tree):
	if (tree.results != None):
		res = tree.results.keys()[0]
		return res
	else:
		val = getattr(student, tree.attr)
		if val > tree.value:
			return execTree(student, tree.tb)
		else:
			return execTree(student, tree.fb)

# Run test data through tree
def testTree(arr, tree):
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
		prediction = execTree(cur, tree)
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


def main():
	# Parse training data and form tree
	trainingData = parseData("training")
	tree = buildTree(trainingData)
	print ("Test Data Tree Formation")
	print ("------------------------")
	printTree(tree)
	print ("\n\n")

	# Parse test data and run it through the tree
	testData = parseData("test")
	(confustionMatrix, rocCurve) = testTree(testData, tree)
	statistics = formStatistics(confustionMatrix, rocCurve)

	print ("Confusion matrix from test data")
	print ("-------------------------------")
	printStats(confustionMatrix)
	print ("\n\n")
	print ("Statistics from test data")
	print ("-------------------------")
	printStats(statistics)

main()
