import sys
import datetime
from calendar import monthrange

# returns the time from today to retrieve
def days_ago(retrieve_date):
    today = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    retrieve = datetime.datetime.strptime(str(retrieve_date), "%Y-%m-%d")

    return (today - retrieve).days


# Calculates the day and month to retrieve from
# return: %d-%m 
def get_day_in_month():
    months = [monthrange(datetime.date.today().year, datetime.date.today().month)[1],
              monthrange(datetime.date.today().year, datetime.date.today().month -1)[1],
              monthrange(datetime.date.today().year, datetime.date.today().month -2)[1],
              monthrange(datetime.date.today().year, datetime.date.today().month -3)[1]]
    print(months)



print(days_ago(sys.argv[1]))
print(get_day_in_month())
