from datetime import datetime

class Database:
	def __init__(self, path):
		"""Returns the database CSV as an appropriately-formatted dictionary populated with (date, quantity) tuples."""
		self.data = {}
		with open(path, 'r') as f:
			headers = f.readline().strip('\n').split(',')[1:]
			for header in headers:
				self.data[header] = []
			for line in f:		# reader starts on second line
				line = line.strip('\n').split(',')	# format line nicely
				date = datetime.strptime(line[0], '%Y-%m-%d')
				for i, quantity in enumerate(line[1:]):
					try:
						self.data[headers[i]].append((date, int(quantity)))
					except ValueError:		# if there is no quantity entry
						continue
	def __repr__(self):
		"""Print all entries in database."""
		out = ""
		for key in self.data:
			out += key + ':\n'
			for entry in self.data[key]:
				out += entry[0].strftime("%d/%m/%Y") + '\t' + str(entry[1]) + '\n'
			out += '\n'
		return out

	# File management
	def save(self, path, sortDB = True):
		"""Saves database back to CSV format. If the database is already sorted, set sortDB = False."""
		if sortDB:
			self.sort()

		# `out` will be a two-dimensional list for easy positional access
		out = [list(self.data)]
		out[0].insert(0, 'DATE')
		
		# populate first column with dates
		dates = []
		for item in self.data:
			for entry in self.data[item]:
				if entry[0] not in dates:
					dates.append(entry[0])
		dates.sort()
		blankdat = ['' for _ in range(len(self.data.keys()))]
		for date in dates:		# create output template...
			out.append([date.strftime("%Y-%m-%d")] + blankdat)

		# populate data
		for item in self.data:
			# get position in output
			index = out[0].index(item)
			for date, quantity in self.data[item]:
				for i, row in enumerate(out[1:]):
					if row[0] == date.strftime("%Y-%m-%d"):
						out[i + 1][index] = quantity

		# convert list back to string
		for i, row in enumerate(out):
			for j, element in enumerate(out[i]):
				out[i][j] = str(out[i][j])
			out[i] = ','.join(out[i])
		out = '\n'.join(out)

		with open(path, 'w') as f:
			f.write(out)

	# Entry management
	def addEntry(self, item, date, quantity):
		"""Adds an entry to the loaded database. Does not modify actual database. Will throw exception if entry already exists or KeyError if item is not in keys.

		Item should be a string, date should be a datetime object, quantity should be an int."""
		for entry in self.data[item]:	# check if entry already exists
			if entry[0] == date:
				raise Exception("Entry already exists.")
		self.data[item].append((date, quantity))
	def modEntry(self, item, date, quantity):
		"""Modify an entry. Will throw exception if entry does not exist or KeyError if item is not in keys."""
		for i, entry in enumerate(self.data[item]):
			if entry[0] == date:
				self.data[item][i] = (date, quantity)
				return
		raise Exception("Entry does not exist.")
	def delEntry(self, item, date):
		"""Remove an entry. Will throw exception if entry does not exist or KeyError if item is not in keys."""
		for i, entry in enumerate(self.data[item]):
			if entry[0] == date:
				del self.data[item][i]
				return
		raise Exception("Entry does not exist.")
	def sort(self):
		for item in self.data:
			self.data[item].sort()

def avgroc(data):
	"""Calculates average rate of consumption. Excludes all intervals on which rate is positive. Returns -1 if no decreasing intervals found."""
	avg = 0
	n = 0
	for i in range(len(data) - 1):
		if data[i] > data[i + 1]:	# capture decreasing intervals only
			avg += data[i] - data[i + 1]
			n += 1
	try:
		avg /= n
	except ZeroDivisionError:
		return -1
	return avg

## FOR TESTING ONLY
def printFile(path):
	with open(path, 'r') as f:
		print("-- BEGIN --")
		for line in f:
			print(line, end = "")
		print()
		print("-- END --")

def identicalFile(path1, path2):
	with open(path1) as f1:
		d1 = f1.readlines()
	with open(path2) as f2:
		d2 = f2.readlines()
	if d1 == d2:
		return True
	else:
		return False

if __name__ == "__main__":
	database = Database("database.csv")
	print(database)

	try:
		database.addEntry('shirts', datetime(2017, 2, 21), 15)
	except KeyError:
		print("Key does not exist.")
	except Exception:
		print("Entry already exists for that date.")

	print(database)

	try:
		database.modEntry('shirts', datetime(2017, 2, 15), 200)
	except KeyError:
		print("Key does not exist.")
	except Exception:
		print("Entry date does not exist.")

	print(database)

	try:
		database.delEntry('shirts', datetime(2017, 2, 17))
	except KeyError:
		print("Key does not exist.")
	except Exception:
		print("Entry date does not exist.")

	print(database)

	print(database.save("test.csv"))