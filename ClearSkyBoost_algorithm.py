# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ClearSkyBoost
                                 A QGIS plugin
 Remove clouds from sentinel2 imagery
                              -------------------
        begin                : 2023-07-10
        copyright            : (C) 2023 by MCC & UMaine
        email                : gis.williamasimone@gmail.com
 ***************************************************************************/

"""

__author__ = 'MCC & UMaine'
__date__ = '2023-07-10'
__copyright__ = '(C) 2023 by MCC & UMaine'
__revision__ = '$Format:%H$'

import sys
import os



# import argparse
# import tempfile
# import glob
# from osgeo import gdal
# from osgeo_utils import gdal_merge
# import argparse
# import tempfile
# import glob
# from osgeo import gdal
# from osgeo_utils import gdal_merge
# from rios import fileinfo
# from rios.imagewriter import DEFAULTDRIVERNAME, dfltDriverOptions
# from fmask import config
# from fmask import fmaskerrors
# ###from fmask.cmdline import sentinel2makeAnglesImage
# from fmask import fmask
# from fmask import sen2meta



sys.path.append(os.getcwd())
libs_folder = os.path.join(os.path.dirname(__file__), "libs")
if libs_folder not in sys.path:
    sys.path.append(libs_folder)
from .libs.fmask.cmdline.sentinel2Stacked import mainRoutine

from qgis.core import QgsProcessingAlgorithm
from qgis.core import (QgsProcessingParameterFileDestination, 
QgsProcessingParameterFile, 
QgsProcessingAlgorithm,
QgsProcessingParameterEnum, 
QgsProcessingParameterNumber,
QgsProcessingParameterBoolean,
QgsProcessingParameterString)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QLineEdit



class ClearSkyBoostAlgorithm(QgsProcessingAlgorithm):
    SAFE_DIR='SAFE Directory'
    OUTPUT_PATH="Output Mask Path"
    RESOLUTION = 'RESOLUTION'
    MIN_CLOUD_SIZE = 'MIN_CLOUD_SIZE'
    KEEP_INTERMEDIATE = 'KEEP INTERMEDIATE'
    BUFFER_DISTANCE = 'BUFFER_DISTANCE'
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
                self.SAFE_DIR,
                'Specify the directory where your source files are located',
                defaultValue=os.path.expanduser('~'),
                behavior=QgsProcessingParameterFile.Folder
        ))
        self.addParameter(QgsProcessingParameterFileDestination(
                self.OUTPUT_PATH,
                'Specify the output mask file',
                createByDefault=True,
                defaultValue=os.path.join(os.path.expanduser('~'), 'cloud_mask.tif'),
                fileFilter='GeoTIFF (*.tif)'
        ))
        self.addParameter(QgsProcessingParameterEnum(
                self.RESOLUTION,
                'Select image resolution, 10m for more detail or 20m for faster processing.',
                options=['10','20'],
                defaultValue= '20'
        ))
        
        cloudparam=QgsProcessingParameterNumber(
            self.MIN_CLOUD_SIZE,
            'Select the minimum cloud size (in pixels) to retain',
            type=QgsProcessingParameterNumber.Double,
            defaultValue=2,
            minValue=1,
            maxValue=5,
            optional=True)
        cloudparam.setMetadata({'widget_wrapper':
                           {'decimals':0}})
        self.addParameter(cloudparam)

        self.addParameter(QgsProcessingParameterBoolean(
            self.KEEP_INTERMEDIATE,
            'Keep Intermediate Files',
            defaultValue=False
        ))
        self.addParameter(QgsProcessingParameterNumber(
            self.BUFFER_DISTANCE,
            'Cloud and Shadow Buffer Distance (in meters)',
            type=QgsProcessingParameterNumber.Double,
            defaultValue=None,
            minValue=10,
            maxValue=1000,
            optional=True
        ))
        
    def processAlgorithm(self, parameters, context, feedback):
        safe_dir = self.parameterAsFile(parameters, self.SAFE_DIR, context)
        if "L1C" not in str(safe_dir):
            feedback.reportError('Please use Sentinel2 data with an L1C sensor type.', True)
            return {}
        else:
                output_path = self.parameterAsFile(parameters, self.OUTPUT_PATH, context)
        
        
        
        resolution = self.parameterAsString(parameters, self.RESOLUTION, context)
        min_cloud_size = self.parameterAsInt(parameters, self.MIN_CLOUD_SIZE, context)
        keep_intermediate = self.parameterAsBool(parameters, self.KEEP_INTERMEDIATE, context)
        buffer_distance = self.parameterAsDouble(parameters, self.BUFFER_DISTANCE, context)
        if buffer_distance is None:
            if resolution == '10':
                buffer_distance = 10 * 3  # 3 times the resolution (10m)
            else:
                buffer_distance = 20 * 3  # 3 times the resolution (20m)

        feedback.pushInfo(f"Safe directory: {safe_dir}")
        feedback.pushInfo(f"Output path: {output_path}")
        feedback.pushInfo(f'Selected resolution: {resolution}m')
        feedback.pushInfo(f"Minimum Cloud Size: {min_cloud_size:.2f}")
        feedback.pushInfo(f"Keep Intermediate Files: {keep_intermediate}")
        feedback.pushInfo(f"Buffer Distance: {buffer_distance}m")
        feedback.pushInfo("System path:")
        for path in sys.path:
            feedback.pushInfo(path)


        mainRoutine(["--safedir", safe_dir, 
                     '-o', output_path,
                     "--pixsize", resolution,
                     "--mincloudsize", str(min_cloud_size),
                     "--cloudbufferdistance", str(buffer_distance),
                     "--shadowbufferdistance", str(buffer_distance)
                     ], feedback=feedback)
        return {}

    def name(self):
            """
            Returns the algorithm name, used for identifying the algorithm. This
            string should be fixed for the algorithm, and must not be localised.
            The name should be unique within each provider. Names should contain
            lowercase alphanumeric characters only and no spaces or other
            formatting characters.
            """
            return 'ClearSkyBoost'

    def displayName(self):
            """
            Returns the translated algorithm name, which should be used for any
            user-visible display of the algorithm name.
            """
            return self.tr(self.name())

    def group(self):
            """
            Returns the name of the group this algorithm belongs to. This string
            should be localised.
            """
            return self.tr(self.groupId())

    def groupId(self):
            """
            Returns the unique ID of the group this algorithm belongs to. This
            string should be fixed for the algorithm, and must not be localised.
            The group id should be unique within each provider. Group id should
            contain lowercase alphanumeric characters only and no spaces or other
            formatting characters.
            """
            return 'ClearSkyBoost'

    def tr(self, string):
            return QCoreApplication.translate('Processing', string)

    def createInstance(self):
            return ClearSkyBoostAlgorithm()


