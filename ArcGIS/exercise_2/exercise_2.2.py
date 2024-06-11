import arcpy

# list all feature classes that are points in a fgdb 
arcpy.env.workspace = r'D:\Dokumente\Studium\8 FS\Python in QGIS and ArcGIS\Übungen\Introduction to scripting in ArcGIS Pro\exercise_arcpy_1.gdb'
# Define a dictonary, where the different buffer distances are stored
types = {"mast":300,"mobile_antenna":50,"building_antenna":100}

# Add a new field for the buffer distances
arcpy.management.AddField("active_assets","buffer_distance","SHORT")
# Iterate through the types
for key in types:
    # First select all features with the specified type
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view="active_assets",
        selection_type="NEW_SELECTION",
        where_clause=f"type = '{key}'",
    )
    # Then calculate the buffer_distance
    arcpy.management.CalculateField("active_assets","buffer_distance",expression=f"{types[key]}")

# Clear Selection
arcpy.management.SelectLayerByAttribute("active_assets", "CLEAR_SELECTION")

# Calculate the buffer based on the different buffer distances
arcpy.analysis.Buffer("active_assets","coverage","buffer_distance")
        
print("Buffer complete!")