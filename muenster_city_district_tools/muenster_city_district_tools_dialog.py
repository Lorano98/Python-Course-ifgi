# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MuensterCityDistrictToolsDialog
                                 A QGIS plugin
 Gives information about city districts
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-04
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Eva Langstein, Anne Staskiewicz, Felix Disselkamp
        email                : elangste@uni-muenster.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import (QMessageBox,
                             QFileDialog)
from qgis.core import QgsProject
from qgis.utils import iface
import os
import csv

from .dataDialogue import Ui_Dialog as Ui_DataDialog
from .exportDialogue import Ui_Dialog as Ui_ExportDialog
from .pdfFunctions import sizeArea, numberOfHousholds, numberOfParcels, numberOfSchools, numberOfPools, createPDF

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'muenster_city_district_tools_dialog_base.ui'))

# Get the district layer from the map
layer_d = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
parent = iface.mainWindow()

# Class for the data dialog
class DataDialog(QtWidgets.QDialog, Ui_DataDialog):
    def __init__(self, parent=None):
        super(DataDialog, self).__init__(parent)
        self.setupUi(self)
        self.ok_Button.clicked.connect(self.accept)

# Class for the export dialog
class ExportDialog(QtWidgets.QDialog, Ui_ExportDialog):
    def __init__(self, parent=None):
        super(ExportDialog, self).__init__(parent)
        self.setupUi(self)
        self.ok_button.clicked.connect(self.accept)
        # Create funtions for the buttons
        self.pdf_button.clicked.connect(self.pdf)
        self.csv_button.clicked.connect(self.createCSV)  

    # Function to create a pdf
    def pdf(self):
        # Check wether the right amount of districts is selected
        if(len(layer_d.selectedFeatures())==0):
            QMessageBox.warning(parent,"Information","(╯°□°)╯︵ ɹoɹɹƎ \n\n           No district selected!")
        elif(len(layer_d.selectedFeatures())>1):
            QMessageBox.warning(parent,"Information","(╯°□°)╯︵ ɹoɹɹƎ \n\n           More than one district selected!")
        else:
            district = layer_d.selectedFeatures()[0]
            # Open the file dialog
            output_path = QFileDialog.getSaveFileName(None, "📥 Select save destination ","", '*.pdf')

            if not output_path[0]:
                # User has cancelled
                QMessageBox.warning(parent,"Information","🚫😊 The user cancelled the export!")
            else:
                createPDF(district, output_path[0], parent)

    # Function to create a csv
    def createCSV(self):
        # Check wether the right amount of districts is selected
        if(len(layer_d.selectedFeatures())==0):
            QMessageBox.warning(parent,"Information","(╯°□°)╯︵ ɹoɹɹƎ \n\n           No district selected!")
        else:
            # Open the file dialog
            output_path = QFileDialog.getSaveFileName(None, "📥 Select save destination ","", '*.csv')

            if not output_path[0]:
                QMessageBox.warning(parent,"Information","🚫😊 The user cancelled the export!")
            else:
                # List to store all the rows.
                data = []
                districts = layer_d.selectedFeatures()
                for f in districts:
                    # Calculate every attribute
                    name = f["Name"]
                    area = sizeArea(f)
                    parcels = numberOfParcels(f)
                    schools = numberOfSchools(f)
                    # Store it in the list
                    data.append([name,area,parcels,schools])

                # Csv Writer
                with open(output_path[0],"w",newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow(["Name","Size","Parcels","Schools"])
                    # Make a new row for each feature
                    for i in data:
                        writer.writerow(i)

                # Feedback after the writing has finished
                QMessageBox.information(parent,"Information","ദ്ദി(｡•̀ ,<)~✩‧₊ \nThe csv was created successfully at the path: " + output_path[0])

class MuensterCityDistrictToolsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MuensterCityDistrictToolsDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.DataButton.clicked.connect(self.getData)
        self.ExtportButton.clicked.connect(self.openExportDialog)

    def getData(self):
        # Check wether the right amount of districts is selected
        if(len(layer_d.selectedFeatures())==0):
            QMessageBox.warning(parent,"Information","(╯°□°)╯︵ ɹoɹɹƎ \n\n           No district selected!")
        elif(len(layer_d.selectedFeatures())>1):
            QMessageBox.warning(parent,"Information","(╯°□°)╯︵ ɹoɹɹƎ \n\n           More than one district selected!")
        else:
            district = layer_d.selectedFeatures()[0]

            # Calculate every attribute
            name = district["Name"]
            parent_district = district["P_District"]
            area = sizeArea(district)
            households = numberOfHousholds(district)
            parcels = numberOfParcels(district)
            schools = numberOfSchools(district)
            pools = numberOfPools(district)

            # Open the data dialog
            dialog = DataDialog()
            dialog.data_textBox.setHtml(f"Name: {name}<br>" \
                        f"Parent district: {parent_district}<br>" \
                        f"Area: {area} m²<br>" \
                        f"Households: {households}<br>" \
                        f"Parcels: {parcels}<br>" \
                        f"Schools: {schools}<br>" \
                        f"Pools: {pools}")
            dialog.exec_()

    # Open the export dialog
    def openExportDialog(self):
        print("openExportDialog")
        dialog = ExportDialog()
        dialog.exec_()

