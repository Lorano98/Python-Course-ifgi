import arcpy
import os

# list all feature classes that are points in a fgdb 
arcpy.env.workspace = r'D:\Dokumente\Studium\8 FS\Python in QGIS and ArcGIS\Übungen\Introduction to scripting in ArcGIS Pro\exercise_arcpy_1.gdb'
fc_list = arcpy.ListFeatureClasses(feature_type='Point')

# Loop through all layer
for pt_fc in fc_list:
    # Don't look in the layer "active_assets"
    if pt_fc == "active_assets":
        break
    # reference fc and fields
    fc_path = os.path.join(arcpy.env.workspace,pt_fc)
        
    # build sql
    sql = "status='active'"
    attributes = []
    # Search for every feature where the status is active. Then append it to a list.
    with arcpy.da.SearchCursor(in_table=fc_path,field_names=['*'],where_clause=sql) as cursor:
        for row in cursor:
            attributes.append(row)

    # Insert the filtered features in the fc "active_assets"
    with arcpy.da.InsertCursor("active_assets",["*"]) as cursor:
        for row in attributes:
            cursor.insertRow(row)
            
    print(f"Insertion finished for layer {pt_fc}")