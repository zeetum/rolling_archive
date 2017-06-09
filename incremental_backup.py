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
			with open(backup_location + "/creation_date") as time_file:
				self.creation_date = datetime.datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y")
				time_file.write(self.creation_date)
		else:
			with open(backup_location + "/creation_date") as time_file:
				self.creation_date = time_file.read()
                	
	def __get_data(self, days_ago):
                backup_data = []
		
                for day in range(days_ago):
                        day_file = self.backup_location + "/" + day
                        if os.path.isfile(day_file):
                                with open(day_file, 'rb') as f:
                                        self.backup_data.append(f.read())
                        else:
                                self.backup_data.append(b'')
                
                return month_data
	
	
        # Writes the file associated with backup_date to restore_file_location
	def retrieve_day(self, restore_location, retrieve_date):
		today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
                retrieve_date = datetime.datetime.strptime(str(retrieve_date), "%d-%m-%Y")
		days_ago = (today - retrieve).days
		if (days_ago > ):
			days_ago = str(creation_date)
		
		backup_data = __get_data(days_ago)
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
                archive_day =  (today - creation_date).days
                		  
                # Tar backup_folders togeather
                temp_file = self.backup_location + "/temp.tar.xz"
                day_data = b""
		with tarfile.open(temp_file, "x:xz") as tar:
                	for folder in backup_folders:
                                tar.add(folder)
                with open(temp_file, "rb") as binary:
                        day_data = binary.read()
		os.remove(temp_file)
                
                # Write to disk
                day_file = backup_location + "/" + str(archive_day)
                if archive_day == 0:
                	with open(day_file, "wb") as f:
                		f.write(day_data)
                else:
                        backup_data = __get_data(days_ago)
                        last_day = reduce(xdelta3.decode, backup_data)
                        with open(day_file, "wb") as f:
                                f.write(xdelta3.encode(last_day, day_data))

archive = Archive("/home/dunadmin/test_backup", ['month1','month2','month3','month4'])
archive.archive_day(["/home/dunadmin/Downloads"])
archive.retrieve_day("/home/dunadmin/test_restore", "01-02-2017")
