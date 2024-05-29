"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureRequest,
                       QgsProject,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFileDestination,
                       QgsVectorLayer)
from qgis import processing
from qgis.utils import iface
import time
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from collections import Counter
import os

class CreateCityDistrictProfile(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    DISTRICTS = 'Districts'
    POI = "Poi"
    PDF_OUTPUT = 'PDF_OUTPUT'
    
    # get Muenster_City_Districts.shp layer in the TOC
    layers_d = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
    layer_d = layers_d[0]

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return CreateCityDistrictProfile()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'createcitydistrictprofile'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Create City District Profile')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'scripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Calculate the size of the district, the number of households and the number of parcels. Also the number of schools or pools is calculated. A map image of the district is printed. Also a barchart about the types of schools/pools is calculated.")
        
    def getDistricts(self):

        # Create QgsFeatureRequest() instance
        request = QgsFeatureRequest()

        # Define clause
        nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)

        # Set clause
        orderby = QgsFeatureRequest.OrderBy([nameClause])
        request.setOrderBy(orderby)

        # Save districts in a list ordered by attribute "Name"
        districts_names = []
        for feature in self.layer_d.getFeatures(request):
            districts_names.append(feature["Name"])
            
        return districts_names

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        districts_names = self.getDistricts()
        
        # Dropdown Menü for choosing the district
        self.addParameter(
            QgsProcessingParameterEnum(
            self.DISTRICTS, 'Choose a district', options=districts_names, defaultValue="Schloss", usesStaticStrings=True
            )
        )
        
        # Choose wether you want to have calculations about the schools or the pools
        self.addParameter(
            QgsProcessingParameterEnum(
            self.POI, 'Choose a POI', options=["Schools", "Pools"], defaultValue="Schools", usesStaticStrings=True
            )
        )

        # Choose a destination to save the pdf
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.PDF_OUTPUT,
                self.tr('Output PDF File'),
                fileFilter="PDF files (*.pdf)"
            )
        )
    
    # Calculate the size of the selected district
    def sizeArea(self, district):
        return district.geometry().area()
       
    # Calculate the number of households in the selected district
    def numberOfHousholds(self, district):
        layers_h = QgsProject.instance().mapLayersByName("House_Numbers")
        layer_h = layers_h[0]
        counter = 0
        # Check for every house number wether it lies in the selected district
        for feature in layer_h.getFeatures():
            if district.geometry().contains(feature.geometry()):
                counter = counter + 1
        
        return counter
    
    # Calculate the number of parcels in the selected district
    def numberOfParcels(self, district):
        layers_p = QgsProject.instance().mapLayersByName("Muenster_Parcels")
        layer_p = layers_p[0]
        counter = 0
        # Check for every parcel wether it lies in the selected district
        for feature in layer_p.getFeatures():
            if district.geometry().intersects(feature.geometry()):
                counter = counter + 1
        
        return counter
        
    # Calculate the number of schools or pools in the selected district
    def numberOfSOP(self, context, parameters, district):
        # Get schools or pools
        poi_string = self.parameterAsString(
            parameters,
            self.POI,
            context
        )
        
        # Define the name of the type attribute
        typename = ""
        # Check which POI is selected
        if poi_string == "Schools":
            # Schools is selected
            layers = QgsProject.instance().mapLayersByName("Schools")
            typename = "SchoolType"
        else:
            # Pools is selected
            layers = QgsProject.instance().mapLayersByName("public_swimming_pools")
            typename = "Type"
            
        layer = layers[0]
        
        counter = 0
        sop_in_d = [] # list for storing all features which lie in the selected district
        # Check for every school or pool wether it lies in the selected district
        for feature in layer.getFeatures():
            if district.geometry().contains(feature.geometry()):
                counter = counter + 1
                sop_in_d.append(feature[typename])
        
        return counter, sop_in_d
    
    def createPDF(self, outputPath, context, parameters):
        
        # Get selected district from GUI
        d_string = self.parameterAsString(
            parameters,
            self.DISTRICTS,
            context
        )
        # select the feature by the district name choosen by the user
        self.layer_d.selectByExpression(f"\"Name\" LIKE '{d_string}'", QgsVectorLayer.SetSelection)
        district = self.layer_d.selectedFeatures()[0]
        
        # Calculate all the parameters
        area = self.sizeArea(district)
        households = self.numberOfHousholds(district)
        parcels = self.numberOfParcels(district)
        sop = self.numberOfSOP(context, parameters,district)
        schools_or_pools = sop[0]
        
        # Calculate the frequenzies of the types
        schools_or_pools_features = sop[1]
        freq = Counter(schools_or_pools_features)
        types = list(freq.keys()) # List which all the types
        counts = list(freq.values()) # List with the counts of each type
        
        # Make the barchart
        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        ax.bar(types, counts)
        bar_path = 'D:/barchart.png'
        plt.savefig(bar_path)
        plt.close()
        
        # Zoom to selected features
        iface.mapCanvas().zoomToSelected()
        iface.mapCanvas().refresh()
        time.sleep(5)
        
        # Take Screenshot of the map
        picture_path = 'D:/feature.png'
        iface.mapCanvas().saveAsImage(picture_path)
        
        # Create Canvas for displaying the pdf
        c = canvas.Canvas(outputPath)
        
        # Title
        c.setFont("Helvetica", 30)
        c.drawString(100,750,f"City District Profile {d_string}")
        c.setFont("Helvetica", 12)
        
        # Draw all parameters
        c.drawString(100,715,f"Parent District: {district['P_District']}")
        c.drawString(100,700,f"Size: {area} m²")
        c.drawString(100,685,f"Number of housholds: {households}")
        c.drawString(100,670,f"Number of parcels: {parcels}")
        if schools_or_pools == 0:
            c.drawString(100,655,"No schools/pools in this district.")
        else:
            c.drawString(100,655,f"Number of schools/pools: {schools_or_pools}")
        
        # Draw image of map
        map = ImageReader(picture_path)
        c.drawImage(map, 100, 500, width=300, height=150)
        
        # Draw the barchart
        barchart = ImageReader(bar_path)
        c.drawImage(barchart, 100, 300, width=300, height=150)
 
        c.save()
        
        os.remove(picture_path)
        os.remove(bar_path)

    def processAlgorithm(self, parameters, context, feedback):
        outputPath = self.parameterAsFileOutput(parameters, 'PDF_OUTPUT', context)
        self.createPDF(outputPath, context, parameters)
        return{"PDF_OUTPUT":outputPath}
    
