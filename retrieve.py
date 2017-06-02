import sys
import datetime
from calendar import monthrange
# Calculates the day and month to retrieve from
# return: %d-%m
def get_day_of_month(retrieve_date):

        today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
        retrieve = datetime.datetime.strptime(str(retrieve_date), "%Y-%m-%d")
        days_ago = (today - retrieve).days
        if days_ago < 0:
                days_ago = 0

        months = [monthrange(datetime.date.today().year, datetime.date.today().month)[1],
        monthrange(datetime.date.today().year, datetime.date.today().month -1)[1],
        monthrange(datetime.date.today().year, datetime.date.today().month -2)[1],
        monthrange(datetime.date.today().year, datetime.date.today().month -3)[1]]

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



print(get_day_of_month(sys.argv[1]))
