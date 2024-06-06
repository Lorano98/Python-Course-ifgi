from qgis.core import QgsProject
from PyQt5.QtWidgets import QMessageBox
from qgis.utils import iface
import time
from reportlab.lib.utils import ImageReader
import os
from reportlab.pdfgen import canvas
from pathlib import Path

# Calculate the size of the selected district
def sizeArea(district):
    return district.geometry().area()

# Calculate the number of households in the selected district
def numberOfHousholds(district):
    layers_h = QgsProject.instance().mapLayersByName("House_Numbers")
    layer_h = layers_h[0]
    counter = 0
    # Check for every house number wether it lies in the selected district
    for feature in layer_h.getFeatures():
        if district.geometry().contains(feature.geometry()):
            counter = counter + 1
    
    return counter

# Calculate the number of parcels in the selected district
def numberOfParcels(district):
    layers_p = QgsProject.instance().mapLayersByName("Muenster_Parcels")
    layer_p = layers_p[0]
    counter = 0
    # Check for every parcel wether it lies in the selected district
    for feature in layer_p.getFeatures():
        if district.geometry().intersects(feature.geometry()):
            counter = counter + 1
    
    return counter
    
# Calculate the number of schools in the selected district
def numberOfSchools(district):        
    layer = QgsProject.instance().mapLayersByName("Schools")[0]
    
    counter = 0
    sop_in_d = [] # list for storing all features which lie in the selected district
    # Check for every school or pool wether it lies in the selected district
    for feature in layer.getFeatures():
        if district.geometry().contains(feature.geometry()):
            counter = counter + 1
            sop_in_d.append(feature["SchoolType"])
    
    return counter

# Calculate the number of pools in the selected district
def numberOfPools(district):        
    layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
    
    counter = 0
    sop_in_d = [] # list for storing all features which lie in the selected district
    # Check for every school or pool wether it lies in the selected district
    for feature in layer.getFeatures():
        if district.geometry().contains(feature.geometry()):
            counter = counter + 1
            sop_in_d.append(feature["Type"])
    
    return counter

def createPDF(district, output_path, parent):
    # Calculate every attribute
    name = district["Name"]
    parent_district = district["P_District"]
    area = sizeArea(district)
    households = numberOfHousholds(district)
    parcels = numberOfParcels(district)
    schools = numberOfSchools(district)
    pools = numberOfPools(district)
    
    # Zoom to selected features
    iface.mapCanvas().zoomToSelected()
    iface.mapCanvas().refresh()
    time.sleep(5)
    
    # Take Screenshot of the map and store it in the same path as the pdf
    folder = Path(output_path).parent
    picture_path = f'{folder}/feature.png'
    iface.mapCanvas().saveAsImage(picture_path)
    
    # Create Canvas for displaying the pdf
    c = canvas.Canvas(output_path)
    
    # Title
    c.setFont("Helvetica", 30)
    c.drawString(100,750,f"City District Profile {name}")
    c.setFont("Helvetica", 12)
    
    # Draw all parameters
    c.drawString(100,715,f"Parent District: {parent_district}")
    c.drawString(100,700,f"Size: {area} m²")
    c.drawString(100,685,f"Number of housholds: {households}")
    c.drawString(100,670,f"Number of parcels: {parcels}")
    c.drawString(100,655,f"Number of schools: {schools}")
    c.drawString(100,640,f"Number of pools: {pools}")
    
    # Draw image of map
    map = ImageReader(picture_path)
    c.drawImage(map, 100, 450, width=300, height=150)

    c.save()
    
    os.remove(picture_path)

    # Show message with info, that is was created successfully
    QMessageBox.information(parent,"Information","ദ്ദി(｡•̀ ,<)~✩‧₊ \nThe pdf was created successfully at the path: " + output_path)