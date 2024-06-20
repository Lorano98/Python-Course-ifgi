# exercise 2.1
import arcpy
import os

# set the workspace
arcpy.env.workspace = r'C:\Users\Anne\Documents\Studium\8.Semester\PiQArGIS\arcgis02\arcpy_2.gdb'

# save the path to the busstops
busStops = os.path.join(arcpy.env.workspace,"stops_ms_mitte")
# Create Input Featureclass
arcpy.management.CreateFeatureclass(arcpy.env.workspace, "input", "POINT", spatial_reference='PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')

# Add a point to the featureclass
poi = os.path.join(arcpy.env.workspace,"input")
new_feat = arcpy.Point(847834.0696,6793696.0903)
with arcpy.da.InsertCursor(poi, ["SHAPE@"]) as icur:
    icur.insertRow([new_feat])

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
    print(f"Name of busstop: {row[0]}")    
print(f"Distance: {dist}m")
