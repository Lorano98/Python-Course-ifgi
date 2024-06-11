# Import der benötigten Bibliotheken
from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsPointXY

# Create a mapCanvas() instance
mc = iface.mapCanvas()
# Create a QgsDistanceArea() instance
da = QgsDistanceArea()

# Get the layers
layer_d = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# Create an input dialog.
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")

if bOK:
    # Get the coordinates
    split = sCoords.split(",")
    lat_WGS = float(split[0])
    lon_WGS = float(split[1])
    
    # Initializing the transformation
    crs_from = QgsCoordinateReferenceSystem(4326)
    crs_to = QgsCoordinateReferenceSystem(layer_d.crs().postgisSrid())
    transformation = QgsCoordinateTransform(crs_from, crs_to, QgsProject.instance())
    
    # Transform
    point_from = QgsPointXY(lon_WGS, lat_WGS)
    point_to = transformation.transform(point_from)
    
    # Check every district wether the point lies within
    erg = NULL
    for f in layer_d.getFeatures():
        if f.geometry().contains(point_to):
            erg = f['Name']
    
    # Check if a district has been found
    if erg == NULL:
        QMessageBox.information(parent, "Geoguesser", "The point lies in no district.")
    else:
        QMessageBox.information(parent, "Geoguesser", f"The point lies in the district {erg}.")
    
else:
    # User cancelled
    QMessageBox.warning(parent, "Geoguesser", "User cancelled")