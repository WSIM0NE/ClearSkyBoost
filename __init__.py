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

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'MCC & UMaine'
__date__ = '2023-07-10'
__copyright__ = '(C) 2023 by MCC & UMaine'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ClearSkyBoost class from file ClearSkyBoost.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ClearSkyBoost import ClearSkyBoostPlugin
    return ClearSkyBoostPlugin()
