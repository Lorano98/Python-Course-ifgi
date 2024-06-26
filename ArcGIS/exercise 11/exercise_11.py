# Modify this file to be used with arcpy.GetParametersAsText(0) and arcpy.AddMessage()

import arcpy, sys,  time

arcpy.env.overwriteOutput = True
# parameters
in_fc = arcpy.GetParameterAsText(0)
in_bus = arcpy.GetParameterAsText(1)
name_field = arcpy.GetParameterAsText(2)
name_value = arcpy.GetParameterAsText(3)

# adding the progressor
arcpy.SetProgressor(type='step',message='Progress in my Script',min_range=0, max_range=3,step_value=1)
time.sleep(0.5)

# Build a layer with the name field & field value
arcpy.SetProgressorLabel("Building a new layer")
arcpy.SetProgressorPosition(0)
sql = f"{name_field}='{name_value}'"
arcpy.AddMessage(f"SQL Clause {sql}")
arcpy.MakeFeatureLayer_management(in_features=in_bus,out_layer='near_features',where_clause=sql)
time.sleep(2)

# run work
# near - save the distances in the attribute table
arcpy.SetProgressorLabel("Calculating the Near tool")
arcpy.SetProgressorPosition(1)
near = arcpy.analysis.Near(in_fc,"near_features",distance_unit="Meters")
time.sleep(2)

# create the search cursor
arcpy.SetProgressorLabel("Getting the name and the distance")
arcpy.SetProgressorPosition(2)
scur = arcpy.da.SearchCursor(in_fc, ["NEAR_FID","NEAR_DIST"])
near_id = 0
dist = 0
# save the id of and the distance to the next busstop
for row in scur:
    near_id = row[0]
    dist = round(row[1],2)
# build sql
sql = f"OBJECTID={near_id}"
# Search for the next busstop to save the name
scur = arcpy.da.SearchCursor(in_table="near_features",field_names=['name'],where_clause=sql)
for row in scur:
    arcpy.AddMessage(f"Name of busstop: {row[0]}")    
arcpy.AddMessage(f"Distance: {dist}m")
time.sleep(2)

arcpy.SetProgressorPosition(3)

print('Work Done')