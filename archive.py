from functools import reduce
import os
import tarfile
import datetime
from calendar import monthrange
import xdelta3

class Archive:
	day = datetime.datetime.today().day
	month = datetime.datetime.today().month % 4

	backup_location = ""
        month_folders = []
	month_data = []


	def __init__(self, backup_location):
		self.backup_location = backup_location
		months = ['month1','month2','month3','month4']
		self.month_folders = list(map(lambda month: backup_location + "/" + month, months))
		__create_folders()
		self.month_data = __load_days()


	def __create_folders(self):
		for month in month_folders:
                	if not os.path.exists(month):
                        	os.makedirs(month)


	def __load_days(self):
		days_data = []
		days_in_month = monthrange(datetime.date.today().year, datetime.date.today().month)[1]
                for day in range(days_in_month):
			day_file = month_folders[month] + "/" + day
                        if os.path.isfile(day_file):
                                with open(day_file, 'rb') as f:
                                        days_data.append(f.read())
                        else:
                                days_data.append(b'')
 
                return days_data


	def __clear_month(self):
		days_in_month = monthrange(datetime.date.today().year, datetime.date.today().month)[1]
                for day in range(days_in_month):

			day_file = month_folders[month] + "/" + str(day)
                        with open(day_file, 'w'):
                       		pass

			self.month_data[day] = b''


	# returns [day, month]
	def __get_day_location(self, backup_date):
	
	        today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
	        retrieve = datetime.datetime.strptime(str(retrieve_date), "%d-%m-%Y")
	        days_ago = (today - retrieve).days
	        if days_ago < 0:
                        days_ago = 0

	        months = [monthrange(datetime.date.today().year, datetime.date.today().month)[1],
	        monthrange(datetime.date.today().year, datetime.date.today().month - 1)[1],
                monthrange(datetime.date.today().year, datetime.date.today().month - 2)[1],
                monthrange(datetime.date.today().year, datetime.date.today().month - 3)[1]]

                month = 0
	        today = today.day
	        if today - days_ago <= 0:
	                month += 1
                        days_ago -= today
	        else:
                        return [today - days_ago, 0]
        
                while days_ago > 0 and month < 3:
                        if days_ago - months[month] < 0:
                                break
 
                        days_ago -= months[month]
                        month += 1
	
		if days_ago > months[3]:
        		return [months[3], 3]
		else:
        		return [months[month] - days_ago, month]


	def archive_day(self, backup_folders):
                # Tar backup_folders togeather
                temp_file = backup_location + "/temp.tar"
                day_data = b""
                for folder in backup_folders:
                        with tarfile.open(temp_file, 'w') as tar:
                                tar.add(folder)
                with open(temp_file, "rb") as binary:
                        day_data = binary.read()
                with open(temp_file, 'w'):
                	pass
		
		
                # Write to disk
		day_file = month_folders[month] + "/" + str(day)
                if day == 0:
			__clear_month()
			self.month_data[day] = day_data
			with open(day_file, "wb") as f:
				f.write(self.month_data[day])
			
                else:
			last_day = reduce(xdelta3.decode, month_data[:day])
			self.month_data[day] = xdelta3.encode(last_day, day_data)
			with open(day_file, "wb") as f:
				f.write(self.month_data[day])
