# sudo pip3 install xdelta3 py2exe
# the filename of the backup should be the date it was created

from functools import reduce
import os
import tarfile
import datetime
import xdelta3


# Setup new backup file structure
def new_backup_dir(backup_root):
	month = datetime.datetime.today().month % 4
	months = ['month1','month2','month3','month4']
	month_folders = list(map(lambda month: backup_root + "/" + month, months))
	weeks = ['week1','week2','week3','week4']
	week_folders = []
	for month in month_folders:
		week_folders += list(map(lambda week: month + "/" + week, weeks))
	
	if not os.path.exists(backup_root + "/day"):
		os.makedirs(backup_root + "/day")
	
	for month in month_folders:
		if not os.path.exists(month):
			os.makedirs(month)
	for week in week_folders:
		if not os.path.exists(week):
			os.makedirs(week)
	

# returns a binary string of the delta
def get_days(days_location):
	days_data = []
	for day_location in days_location:
		if os.path.isfile(day_location):
			with open(day_location, 'rb') as day_file:
				days_data.append(day_file.read())
		else:
			days_data.append(b'')

	return days_data


# Tar and compress backup_folders
# [1] = new root to be expanded with the diff of [0]
# [0] = old root to be stomped with the diff the old tail and the new data
def rotate_day(backup_root, backup_folders):
	day = datetime.datetime.today().weekday()
	days = ['mon','tues','wed','thurs','fri','sat','sun']
	days = days[day:] + days[:day]
	days_files = list(map(lambda day: backup_root + "/day/" + day, days))
	days_data = get_days(days_files)
	
	# Tar backup_folders togeather
	day_file = backup_root + "/temp.tar" 
	day_data = b""
	for folder in backup_folders:
		with tarfile.open(day_file, 'w') as tar:
			tar.add(folder)
	with open(day_file, "rb") as binary:
		day_data = binary.read()
		
        # Write the new root file
        with open(days_files[1], "wb") as new_root:
                days_data[1] = xdelta3.decode(days_data[0], days_data[1])
                new_root.write(days_data[1])

        # Write the new tail file
        last_day = reduce(xdelta3.decode, days_data[1:])
        with open(days_files[0], "wb") as new_tail:
                new_tail.write(xdelta3.encode(last_day, day_data))


#backup_folders = a list of folders locations to back up
#backup_location = the directory you'd like to backup to
def rotate_archive(backup_root, backup_folders): 
	
	
	month = datetime.datetime.today().month % 4
	months = ['month1','month2','month3','month4']
	month_folders = list(map(lambda month: backup_root + month, months))
	
	week = datetime.datetime.now().day // 7 % 4
	weeks = ['week1','week2','week3','week4']
	week_folders = list(map(lambda week: month_folders[month] + week, weeks))
	
	day = datetime.datetime.now().day	
	rotate_day(backup_root, backup_folders)
	
	# Rotate weeks at the beginning of each week
	if (day % 7 == 0):
		backup_file = week_folder[week]
		with tarfile.open(backup_file, 'w') as tar:
			for day in day_folders:
				tar.add(day)
	
	# Trim all months other than current to have one week per month
	if (day == 0):
		backup_file = month_folder[month]



def main():
	backup_folders = ['/home/administrator/test_backup']
	backup_dir = '/home/administrator/backup'
	#new_backup_dir(backup_dir)
	rotate_archive(backup_dir, backup_folders)


main()
