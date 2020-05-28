# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
# License-Filename: LICENSE
#
###############################################################################

from qgis.PyQt.QtWidgets import QDialog
from . import get_ui_class

from ..xyz_qgis.models.filter_model import FilterModel
from .util_dialog import ConfirmDialog
from .filter_info_dialog import NewFilterInfoDialog, EditFilterInfoDialog
from .token_dialog import TokenDialog
from qgis.PyQt.QtGui import QStandardItem

class FilterDialog(TokenDialog):
    # Extend TokenDialog
    # refactor tokendialog for resuability

    title = "Filter feature by property"
    message = "Multiple property names represent AND operation. Multiple values represent OR operation."
    token_info_keys = ["name", "operator", "values"]
    NewInfoDialog = NewFilterInfoDialog
    EditInfoDialog = EditFilterInfoDialog

    def __init__(self, parent=None):
        super().__init__(parent)
        for btn in [self.btn_up, self.btn_down]:
            policy = btn.sizePolicy()
            policy.setRetainSizeWhenHidden(True)
            btn.setSizePolicy(policy)
            btn.setVisible(False)
        
    def _make_delete_message(self, token_info):
        return "Do you want to Delete ?"

    def get_filters(self):
        return self.token_model.get_filters()

    def get_display_str(self):
        return self.token_model.get_display_str()
        
        