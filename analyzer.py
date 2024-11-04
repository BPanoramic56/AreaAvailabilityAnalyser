import matplotlib.pyplot as plt
import connector
from datetime import datetime

connection = connector.connect_to_main()
all_data   = connector.get_all(connection=connection)
data = dict()
for row in all_data:
    data[row[2]] = (row[0], row[1])
    
keys = data.keys()
keys = sorted(keys) # Ensuring the data is sorted based on date
x = list()
y = list()


for key in data.keys():
    y.append(data[key][1])

for key in keys:
    date = "{0}.{1}".format(
    str(key.strftime('%d')),
    str(key.strftime('%b')))
    x.append(date)


# plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)

plt.scatter(x, y, label= "stars", color= "darkslategray", marker= "|", s=30)
# naming the x axis
plt.xlabel('Date')
# naming the y axis
plt.ylabel('Usage')

# giving a title to my graph
plt.title('Date x Usage')

# function to show the plot
plt.show()