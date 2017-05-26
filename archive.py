import datetime
import xdelta3
import lzma
import tarfile

# returns a binary string of the delta

def get_days(days_location):
	days_data = []
	for day_location in days_location:
		with open(day_location, 'rb') as day_file:
		#	days_data.append(lzma.decompress(day_file.read()))

	return days_data

# Calculate n + 1 and stomp on n
def rotate_day(backup_root , backup_folders):
	day = datetime.datetime.today().weekday()
	days = ['mon','tues','wed','thurs','fri','sat','sun']
	day_folders = map(lambda day: backup_root + "/day/" + day, days)
	
	# Get each day's data as a string, rotate about 'day'
	days_data = get_days(days_folders)
	days_data = days_data[day:] + days_data[:day]
	
	# Tar backup_folders togeather
	day_file = backup_root + "/temp.tar" 
	day_data = ""
	for folder in backup_folders:
		with tarfile.open(day_file, 'w') as tar:
			tar.add(folder)
	with open(day_file, "rb") as binary:
		day_data = binary.read()

	# Write changes to disk
	with open(day_folders[day]) as new_root:
		days_data[0] = xdelta3.decode(days_data[-1], days_data[0])
                # lzma.compress(days_data[0])
		new_root.write(days_data[0])

	last_day = reduce(xdelta3.decode, days_data[:-1])
	with open(day_folders[(day - 1) % len(day_folders)], "w") as new_tail:
                days_data[-1] = xdelta3.encode(last_day, day_data)
                # lzma.compress(days_data[-1])
		new_tail.write(days_data[-1])
		



#backup_folders = a list of folders locations to back up
#backup_location = the directory you'd like to backup to
def rotate_archive(backup_root, backup_folders): 
	
	
	month = datetime.datetime.today().month % 4
	months = ['month1','month2','month3','month4']
	months_folders= map(lambda month: backup_root + month, months)
	
	week = datetime.datetime.now().day // 7 % 4
	weeks = ['week1','week2','week3','week4']
	week_folders = map(lambda week: month_folders[month] + week, weeks)
	
	day = datetime.datetime.now().day	
	days = ['mon.tar','tues.tar','wed.tar','thurs.tar','fri.tar','sat.tar','sun.tar']
	day_folders = map(lambda day: backup_root + "/day/" + day, days)
	
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
	backup_folders = ['/home/administrator/Downloads/test_dir']
	rotate_archive('/mnt/nas_backup', folder)


main()
