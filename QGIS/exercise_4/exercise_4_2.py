import csv

# Get current map and schools shape
mc = iface.mapCanvas()
schools = QgsProject.instance().mapLayersByName("Schools")[0]

# Array to store all the rows. Filled with the Schoolname and the coordinates.
data = []
sf = schools.selectedFeatures()
for f in sf:
    geo = f.geometry().asPoint()
    data.append([f.attributes()[1],geo.x(), geo.y()])

# Csv Writer
with open("D:/SchoolReport.csv","w",newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["Name","X","Y"])
    # Make a new row for each feature
    for i in data:
        writer.writerow(i)