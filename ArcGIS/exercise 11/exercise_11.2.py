# Modify this file to be used with arcpy.GetParametersAsText(0) and arcpy.AddMessage()

import arcpy, sys,time

arcpy.env.overwriteOutput = True
# parameters
in_fc = arcpy.GetParameterAsText(0)
evaluate_fc = arcpy.GetParameterAsText(1)
name_field = arcpy.GetParameterAsText(2)
name_value = arcpy.GetParameterAsText(3)

# adding the progressor
arcpy.SetProgressor(type='step',message='Progress in my Script',min_range=0, max_range=3,step_value=1)
time.sleep(0.5)
# checking that parameters are correct
arcpy.SetProgressorLabel("Checking the inputs")
arcpy.SetProgressorPosition(0)
time.sleep(2)
arcpy.AddMessage(f"Input Path {in_fc}")
arcpy.AddMessage(f"Name field {evaluate_fc}")
arcpy.AddMessage(f"Name value {name_field}")
arcpy.AddMessage(f"Output Path {name_value}")

# run work

# Build a layer with the name field & field value
arcpy.SetProgressorLabel("Building SQL")
arcpy.SetProgressorPosition(1)
time.sleep(2)
# Build a layer with the name field & field value
sql = f"{name_field}='{name_value}'"
arcpy.MakeFeatureLayer_management(in_features=evaluate_fc,out_layer='distance',where_clause=sql)

arcpy.SetProgressorLabel("Runnning the Near Tool")
arcpy.SetProgressorPosition(2)
time.sleep(2)
# near - save the distances in the attribute table
near = arcpy.analysis.Near(in_fc,"distance",distance_unit="Meters")
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
arcpy.AddMessage(f"Name Haltestelle: {name_value} und {near_id}")    
arcpy.AddMessage(f"Entfernung: {dist}m")

print('Work Done')