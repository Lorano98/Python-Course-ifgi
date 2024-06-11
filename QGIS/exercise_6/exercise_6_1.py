# Read csv
csv = open("D:/standard_land_value_muenster.csv", "r")
lines = csv.readlines()

# Creating a new feature
feature_new = QgsFeature(layer.fields())

# Define the fields
uri = "multipolygon?crs=EPSG:25832&field=standard_land_value:float&field=type:String&field=district:String&index=yes"
layer = QgsVectorLayer(uri, "temp_standard_land_value_muenster", "memory")

# Initialize the data provider on the new layer
provider = layer.dataProvider()

features = []
# Loop through the cvs file to extract the features
for data in lines[1:]:
    # Creating a new feature
    feature_new = QgsFeature(layer.fields())
    
    # Get the row
    row = data.replace("\n","").split(";")
    
    # Set the attributes
    feature_new.setAttribute("standard_land_value", row[0])
    feature_new.setAttribute("type", row[1])
    feature_new.setAttribute("district", row[2])
    feature_new.setGeometry(QgsGeometry.fromWkt(row[3]))
    features.append(feature_new)
    
# Using the data provider to add the new features to the layer
provider.addFeatures(features)

# Add the layer to the map
QgsProject().instance().addMapLayer(layer)