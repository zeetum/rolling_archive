# sudo pip3 install py2exe xdelta3

from functools import reduce
import os
import tarfile
import xdelta3

class Archive:

	backup_location = ""
	creation_date = ""

	def __init__(self, backup_location):
		self.backup_location = backup_location
		
		if not os.path.exists(backup_location):
			os.makedirs(backup_location)
			with open(backup_location + "/creation_date", "w") as time_file:
				self.creation_date = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y")
				time_file.write(self.creation_date)
		else:
			with open(backup_location + "/creation_date") as time_file:
				self.creation_date = datetime.datetime.strptime(time_file.read(), "%d-%m-%Y")


	# Returns an array of data from creation_date to retrieve_date
	def __get_data(self, retrieve_date):
                backup_data = []

                for day in range(0, (retrieve_date - creation_day).days):
                        day_file = self.backup_location + "/" + day
                        if os.path.isfile(day_file):
                                with open(day_file, 'rb') as f:
                                        self.backup_data.append(f.read())
                        else:
                                self.backup_data.append(b'')
                
                return backup_data
	
	
        # Writes the file associated with backup_date to restore_file_location
	def retrieve_day(self, restore_location, retrieve_date):
                retrieve_date = datetime.datetime.strptime(str(retrieve_date), "%d-%m-%Y")
		
		if (retrieve_date < creation_date):
			retrieve_date = creation_date
		
		backup_data = __get_data(retrieve_date)
		day_data = reduce(xdelta3.decode, backup_data)
		
		# Write the days data to a temp file
		temp_file = self.backup_location + "/temp.tar.xz"
		with open(temp_file, "wb") as f:
                	f.write(day_data)

		# Then uncompress it to restore_location
		with tarfile.open(temp_file, "r:xz") as tar:
			tar.extractall(path=restore_location)
		os.remove(temp_file)
		
		
	# Writes the backup_folders to the current day
	def archive_day(self, backup_folders):
		today = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y")
                		  
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
		archive_day = (self.creation_date - today).days
                day_file = backup_location + "/" + str(archive_day)
                if self.creation_date == today:
                	with open(day_file, "wb") as f:
                		f.write(day_data)
                else:
                        backup_data = __get_data(today)
                        last_day = reduce(xdelta3.decode, backup_data)
                        with open(day_file, "wb") as f:
                                f.write(xdelta3.encode(last_day, day_data))

archive = Archive("/home/dunadmin/test_backup")
archive.archive_day(["/home/dunadmin/Downloads"])
archive.retrieve_day("/home/dunadmin/test_restore", "01-02-2017")
