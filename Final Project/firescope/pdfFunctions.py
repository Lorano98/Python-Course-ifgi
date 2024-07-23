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

def createPDF(feuer, output_path, parent, layer_Feuer):
    # Calculate every attribute
    feuerID = feuer["id"]
    typ = feuer["Typ"]
    numGefaeh = feuer["num_Gefaeh"]
    numVerlet = feuer["num_Verlet"]
    Verstaerkung = feuer["Verstaerku"]
    num_Fahrze = feuer["num_Fahrze"]
    datum = feuer["Datum"]
    status = feuer["Status"]

    # Zoom to selected features
    iface.mapCanvas().zoomToSelected(layer_Feuer)
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
    c.drawString(100,750,f"{typ}-Brand (ID={feuerID})")
    c.setFont("Helvetica", 12)
    
    # Draw all parameters
    c.drawString(100,715,f"Brand-ID: {feuerID}")
    c.drawString(100,700,f"Art des Feuers: {typ}")
    c.drawString(100,685,f"Anzahl Gefährdeter Personen: {numGefaeh}")
    c.drawString(100,670,f"Anzahl Verletzter: {numVerlet}")
    if Verstaerkung == "ja":
        c.drawString(100,655,f"Es wurde Verstärkung angefordert.")
    else:
        c.drawString(100,655,f"Es wurde keine Verstärkung angefordert.")
    c.drawString(100,640,f"Anzahl der Einsatzfahrzeuge: {num_Fahrze}")
    c.drawString(100,625,f"Datum des Brandes: {datum}")
    if status == "geloescht":
        c.drawString(100,610,f"Der Brand wurde erkannt und die Gefahr gebannt.")
    else:
        c.drawString(100,610,f"Es brennt noch!")  
    # Draw image of map
    map = ImageReader(picture_path)
    c.drawImage(map, 100, 450, width=300, height=150)

    c.save()
    
    os.remove(picture_path)

    # Show message with info, that is was created successfully
    QMessageBox.information(parent,"Information","ദ്ദി(｡•̀ ,<)~✩‧₊ \nThe pdf was created successfully at the path: " + output_path)