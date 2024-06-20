# exercise 2.1
import arcpy
import os

# set the workspace
arcpy.env.workspace = r'C:\Users\Anne\Documents\Studium\8.Semester\PiQArGIS\arcgis02\arcpy_2.gdb'

# save the path to the busstops
busStops = os.path.join(arcpy.env.workspace,"stops_ms_mitte")
# save path to input
poi = os.path.join(arcpy.env.workspace,"input")

# near - save the distances in the attribute table
near = arcpy.analysis.Near("input","stops_ms_mitte",distance_unit="Meters")

# create the search cursor
scur = arcpy.da.SearchCursor(poi, ["NEAR_FID","NEAR_DIST"])
near_id = 0
dist = 0
# save the id of and the distance to the next busstop
for row in scur:
    near_id = row[0]
    dist = round(row[1],2)

# build sql
sql = f"OBJECTID={near_id}"
# Search for the next busstop to save the name
scur = arcpy.da.SearchCursor(in_table=busStops,field_names=['name'],where_clause=sql)
for row in scur:
    print(f"Name Haltestelle: {row[0]}")    
print(f"Entfernung: {dist}m")
