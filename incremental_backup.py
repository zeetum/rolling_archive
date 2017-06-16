from functools import reduce
import datetime
import time
import os
import tarfile
import xdelta3

class Archive:

	backup_location = ""
	creation_date = ""

	def __init__(self, backup_location):
		self.backup_location = backup_location
		if os.path.exists(self.backup_location + "/temp"):
			os.remove(self.backup_location + "/temp")
		
		if not os.path.exists(backup_location):
			os.makedirs(backup_location)
		
		if os.path.exists(backup_location + "/creation_date"):
			with open(backup_location + "/creation_date") as time_file:
				self.creation_date = datetime.datetime.strptime(time_file.read(), "%Y-%m-%d")
		else:
			with open(backup_location + "/creation_date", "w") as time_file:
				self.creation_date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
				time_file.write(self.creation_date)



	# Returns an array of data from creation_date to retrieve_date
	def __get_data(self, retrieval_date):
		backup_data = []
		
		# Set floor and ceiling
		today = datetime.datetime.fromtimestamp(time.time())
		if retrieval_date > today:
			exit("Error: Date entered is after Today")
		if retrieval_date < self.creation_date:
			exit("Error: Date entered is before Creation Date")

		# Read data from disk 
		day_index = (retrieval_date - self.creation_date).days
		for day in range(0, day_index + 1):
			day_file = self.backup_location + "/" + str(day)
			if os.path.isfile(day_file):
				with open(day_file, 'rb') as f:
					backup_data.append(f.read())
		
		return backup_data
	
	
	# Writes the file associated with backup_date to restore_file_location
	def retrieve_day(self, restore_location, retrieval_date):
		retrieval_date = datetime.datetime.strptime(str(retrieval_date), "%d-%m-%Y")
		backup_data = self.__get_data(retrieval_date)
		day_data = reduce(xdelta3.decode, backup_data)
		
		# Write the days data to a temp file
		temp_file = self.backup_location + "/temp"
		with open(temp_file, "wb") as f:
			f.write(day_data)

		# Then uncompress it to restore_location
		with tarfile.open(temp_file, "r:xz") as tar:
			tar.extractall(path=restore_location)
		os.remove(temp_file)
		
		
	# Writes the backup_folders to the current day
	def archive_day(self, backup_folders):
		today = datetime.datetime.fromtimestamp(time.time())
		yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
		archive_day = today.day - self.creation_date.day

		# Tar backup_folders togeather
		temp_file = self.backup_location + "/temp"
		day_data = b""
		with tarfile.open(temp_file, "x:xz") as tar:
			for folder in backup_folders:
				tar.add(folder)
		with open(temp_file, "rb") as binary:
			day_data = binary.read()
		os.remove(temp_file)

		# Write to disk
		day_file = self.backup_location + "/" + str(archive_day)
		if archive_day == 0:
			with open(day_file, "wb") as f:
				f.write(day_data)
		else:
			backup_data = self.__get_data(yesterday)
			last_day = reduce(xdelta3.decode, backup_data)
			with open(day_file, "wb") as f:
				f.write(xdelta3.encode(last_day, day_data))

archive = Archive("/home/administrator/test_backup")
archive.archive_day(["/home/administrator/Downloads"])
archive.retrieve_day("/home/administrator/test_restore", "16-06-2017")
