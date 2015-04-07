# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OSMDownloaderDialog
                                 A QGIS plugin
 Plugin to download OSM data by area
                             -------------------
        begin                : 2015-04-07
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'osmDownloader_dialog_base.ui'))

from osm_downloader import OSMRequest


class OSMDownloaderDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, startX, startY, endX, endY, parent=None):
        """Constructor."""
        super(OSMDownloaderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.setCoordinates(startX, startY, endX, endY)

    def setCoordinates(self, startX, startY, endX, endY):
        if startX < endX:
            minLong = startX
            maxLong = endX
        else:
            minLong = endX
            maxLong = startX

        if startY < endY:
            minLat = startY
            maxLat = endY
        else:
            minLat = endY
            maxLat = startY

        self.wEdit.setText(str(minLong))
        self.sEdit.setText(str(minLat))
        self.eEdit.setText(str(maxLong))
        self.nEdit.setText(str(maxLat))

    @pyqtSlot()
    def on_saveButton_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(parent=None, caption='Define file name and location', filter='OSM Files(*.osm)')
        fileName += '.osm'
        self.filenameEdit.setText(fileName)

    @pyqtSlot()
    def on_button_box_accepted(self):
        if self.filenameEdit.text() == '':
            QtGui.QMessageBox.warning(self, self.tr("Warning!"), self.tr("Please, select a location to save the file."))
            return

        osmRequest = OSMRequest(self.filenameEdit.text())
        osmRequest.executeRequest(self.wEdit.text(), self.sEdit.text(), self.eEdit.text(), self.nEdit.text())