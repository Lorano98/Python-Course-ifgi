# Create a map canvas object
mc = iface.mapCanvas()

# Get House_Numbers.shp layer in the TOC
layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

# Getting all fields of the layer
fields = layer.fields()

# Getting access to the layers data provider
provider = layer.dataProvider()

# Getting access to the layers capabilities
capabilities = provider.capabilitiesString()
print(capabilities)

# Checking if the capabilty is part of the layer
if "Change Attribute Values" in capabilities:
    print("Features of this layer can be modified...")
    
    # If modifying is possible, get all features of the layer 
    # and loop through them.
    for feature in layer.getFeatures():
        
        # Get the id of the current feature
        feature_id = feature.id()
        
        # If the value of the current feature in the column "Status" has
        # the value "T" change it to "t"
        if feature["Type"] == "H":
            
            # Create a dictionary with column and value to change
            attributesH = {fields.indexOf("Type"):"Hallenbad"}
            
            # Use the changeAttributeValues methode from the provider to 
            # process the attribute change for the specific feature id
            provider.changeAttributeValues({feature_id:attributesH})
            
        elif feature["Type"] == "F":
            
            # Create a dictionary with column and value to change
            attributesF = {fields.indexOf("Type"):"Freibad"}
            
            # Use the changeAttributeValues methode from the provider to 
            # process the attribute change for the specific feature id
            provider.changeAttributeValues({feature_id:attributesF})
        else:
            pass
    
    print("All relevant features are modified...")
    
else:
    print("Features of this layer cannot be modified...")
    
# define layer provider

provider = layer.dataProvider()

#create new field
fld = QgsField('district', QVariant.String, len = 50)
# add new field to layer
provider.addAttributes([fld])
# update layer
layer.updateFields()

# Get House_Numbers.shp layer in the TOC
layerDistricts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# check for every swimming pool in which district it is
for feature in layer.getFeatures():
    for district in layerDistricts.getFeatures():
        if district.geometry().contains(feature.geometry()):
            # Create a dictionary with column and value to change
            attributes = {fields.indexOf("district"):district["Name"]}
            # Use the changeAttributeValues methode from the provider to 
            # process the attribute change for the specific feature id
            provider.changeAttributeValues({feature.id(): attributes})
        