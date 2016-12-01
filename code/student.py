class Student:
	stg = 0.0
	scg = 0.0
	stro = 0.0
	lpr = 0.0
	peg = 0.0
	# Convert the user knowledge level from string to float 0-1
	uns = 0 
	# Exam performance of user for goal objects in letter grade
	goalScore = "F"

	def __init__(self):
		return 

	# Parse from the csv files
	def parse(self, row):
		# Check the row length
		if len(row) != 6:
			return

		# Assign the numbers
		self.stg = float(row[0])
		self.scg = float(row[1])
		self.stro = float(row[2])
		self.lpr = float(row[3])
		self.peg = float(row[4])

		# Handle the UNS conversion
		if row[5].lower() == "very_low":
			self.uns = 0
		elif row[5].lower() == "low":
			self.uns = 0.33
		elif row[5].lower() == "middle":
			self.uns = 0.66
		elif row[5].lower() == "high":
			self.uns = 1

		# Handle goal score
		if self.peg < 0.66:
			self.goalScore = "F"
		elif self.peg < 0.7:
			self.goalScore = "D"
		elif self.peg < 0.8:
			self.goalScore = "C"
		elif self.peg < 0.9:
			self.goalScore = "B"
		else:
			self.goalScore = "A"

		return

	# String representation
	def __str__(self):
		string = "STG: " + str(self.stg) + ", "
		string += "SCG: " + str(self.scg) + ", "
		string += "STR: " + str(self.stro) + ", "
		string += "LPR: " + str(self.lpr) + ", "
		string += "PEG: " + str(self.peg) + ", "
		string += "UNS: " + str(self.uns)

		return string
		
		