# Modify this file to be used with arcpy.GetParametersAsText(0) and arcpy.AddMessage()

import arcpy, sys

arcpy.env.overwriteOutput = True
# parameters
in_fc = arcpy.GetParameterAsText(0)

# checking that parameters are correct
print(f"Input Path {in_fc}")

# run work
# near - save the distances in the attribute table
near = arcpy.analysis.Near(in_fc,"stops_ms_mitte",distance_unit="Meters")

# create the search cursor
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
scur = arcpy.da.SearchCursor(in_table="stops_ms_mitte",field_names=['name'],where_clause=sql)
for row in scur:
    arcpy.AddMessage(f"Name of busstop: {row[0]}")    
arcpy.AddMessage(f"Distance: {dist}m")

print('Work Done')