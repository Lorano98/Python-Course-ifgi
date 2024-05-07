# Create a map canvas object
mc = iface.mapCanvas()

# get Muenster_City_Districts.shp layer in the TOC
layers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
layer = layers[0]

# Create QgsFeatureRequest() instance
request = QgsFeatureRequest()

# Define clause
nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)

# Set clause
orderby = QgsFeatureRequest.OrderBy([nameClause])
request.setOrderBy(orderby)

# Save districts in a list ordered by attribute "Name"
districts_names = []
for feature in layer.getFeatures(request):
    districts_names.append(feature["Name"])

# print(districts_names)

# create window for users to choose a district
parent = iface.mainWindow()
# create a dropdown with the districts
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",
districts_names)

# select the feature by the district name choosen by the user
layer.selectByExpression(f"\"Name\" LIKE '{sDistrict}'", QgsVectorLayer.SetSelection)
district = layer.selectedFeatures()
# print(district)
# save the geometry fo the district
districtgeom = district[0].geometry()

# get the school layer by name
schoolslayers = QgsProject.instance().mapLayersByName("Schools")
schools = schoolslayers[0]


schoolsInDistrict = ""
# if the user cancels the window:
if(bOk == False):
    QMessageBox.warning(parent, "(۶ૈ ᵒ̌ Дᵒ̌)۶ૈ=͟͟͞͞ 💣 Schools", "User is not vegan! Isn't allowed to go to school'")
# if the user confirms their selection
else:
    # loop through the schools 
    for feature in schools.getFeatures():
        school = feature.geometry()
        # save the school names and ity type of schools within in the district
        if(districtgeom.contains(school)):
            schoolsInDistrict += f"{feature['Name']}, {feature['SchoolType']}\n"
# If there are no schools in the district:
if (schoolsInDistrict == ""):
    QMessageBox.information(parent,f"Schools in {sDistrict}" ,"No schools in this district. Unfortunately you stay dumb :)" )
# Print the schools and their types in a window
else:
    QMessageBox.information(parent, f"Schools in {sDistrict}",schoolsInDistrict )
