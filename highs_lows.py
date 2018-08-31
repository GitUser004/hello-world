import csv
from matplotlib import pyplot
from datetime import datetime

filename = "sitka_weather_2014.csv"
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates,highs,lows = [],[],[]
    for row in reader:
        dates.append(datetime.strptime(row[0], "%Y-%m-%d"))
        highs.append(int(row[1]))
        lows.append(int(row[3]))

for index, column_header in enumerate(header_row):
    print(index, column_header)

fig = pyplot.figure(dpi = 128, figsize = (10, 6))
pyplot.plot(dates, highs, c = "red",linewidth = 1,alpha = 0.5)
pyplot.plot(dates, lows, c = "blue",linewidth = 1,alpha = 0.5)
pyplot.fill_between(dates,highs,lows,facecolor='blue',alpha=0.1)

pyplot.title("Daily high temperatures, 2014", fontsize=10)
pyplot.xlabel('', fontsize=10)
fig.autofmt_xdate()
pyplot.ylabel("Temperature (F)", fontsize=10)
pyplot.tick_params(axis='both', which='major', labelsize=10)

pyplot.show()
