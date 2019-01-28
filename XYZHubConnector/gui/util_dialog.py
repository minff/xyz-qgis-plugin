# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
#
###############################################################################


from qgis.PyQt.QtWidgets import QMessageBox
class ConfirmDialog(QMessageBox):
    def __init__(self, parent, txt):
        super().__init__(parent)
        self.setText(txt)
        self.setStandardButtons(self.Ok | self.Cancel)

