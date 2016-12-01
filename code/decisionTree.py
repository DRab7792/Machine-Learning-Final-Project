import csv
from student import Student

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
		print cur


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

trainingData = parseData("training")
set1,set2 = divideSet(trainingData, "uns", 0.5)
print entropy(set2)
