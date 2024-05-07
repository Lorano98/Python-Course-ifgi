# Import modules
from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import *
#!/usr/bin/python
import os, sys

project_path ="C:/Users/Anne/Documents/Studium/8.Semester/PiQArGIS/Python in QGIS/meine_zweite_karte.qgz"  # for QGIS version 3+

# Open a file
path = "C:/Users/Anne/Documents/Studium/8.Semester/PiQArGIS/Python in QGIS/Muenster"
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
    # check if its a shapefile
    if(file[-3:] == 'shp'):
        # add file to path and save it
        name = file
        file = "C:/Users/Anne/Documents/Studium/8.Semester/PiQArGIS/Python in QGIS/Muenster/" + file
        print(file)
        # load path as layer
        file = QgsVectorLayer(file, name, "ogr")
        #Check if layer is valid
        if not file.isValid():
            print("Error loading the layer!")
        else:
        # Create QGIS instance and "open" the project
            project = QgsProject.instance()
            project.read(project_path)
            # Add layer to project
            project.addMapLayer(file)

            # Save project
            project.write()

            print("Layer added to project\nProject saved successfully!")