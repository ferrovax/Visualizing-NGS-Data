import csv
import string
import seaborn as sb
import matplotlib.pyplot as plt

dict, line_count = {}, 0

with open('NGS_data.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')

    for row in csv_reader:
        if line_count > 0:
            if row[2] not in dict.keys():
                # row[2] corresponds to Sample_Well data
                # row[3] corresponds to Well_Total data
                dict[row[2]] = [int(row[3])]
            else:
                dict[row[2]].append(int(row[3]))

        line_count += 1

for key in dict:
    well_average = sum(dict[key]) / ((line_count - 1) / 384)
    dict[key] = well_average

    #print(key, dict[key])

# Printing the dictionary lists well total averages for each of the 384 wells.
# Scrolling through and finding consistently underrepresented wells is easy enough,
# with wells like B18, B24, G10, K04, P23, and even P06 and M06 standing out as underrepresented,
# but we can make the data more clear and interpretable with a heat map.

data = []
# Need to arrange data in a format compatible with Seaborn
# dict -> list of [well ID, well average] pairs
for key in dict:
    data.append([key, dict[key]])

def sortKey(p):
    # sort key function to get wells in order
    return (ord(p[0][:1]) - 97) * 100 + int(p[0][1:])

data.sort(key=sortKey)

# Clean data: keep well averages only
for i in range(384):
    data[i] = data[i][1]

p384, n = [], 24

# p384 -> 384-well plate array (16*24) with our average well values
while n <= 384:
    p384.append(data[n - 24:n])
    n += 24

x_axis = [x if x == 1 or x % 6 == 0 else '' for x in range(1, 25)]
y_axis = string.ascii_uppercase[:16]

heat_map = sb.heatmap(p384, xticklabels=x_axis, yticklabels=y_axis)
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.show()

# Darkest wells, like B18, indicate underrepresented wells.
