import datetime

x = datetime.datetime.now()
print(x)
print(x.year)

y = datetime.datetime(2020, 5, 17)
print(y)

print(x.strftime("%A")) #weekday name
print(x.strftime("%d")) #day of month
print(x.strftime("%B")) #month name
