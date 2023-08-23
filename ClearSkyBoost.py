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

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from qgis.core import QgsProcessingAlgorithm, QgsApplication
from .ClearSkyBoost_provider import ClearSkyBoostProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class ClearSkyBoostPlugin(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = ClearSkyBoostProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
