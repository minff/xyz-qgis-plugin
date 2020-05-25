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
    token_info_keys = ["name", "operator", "values"]
    NewInfoDialog = NewFilterInfoDialog
    EditInfoDialog = EditFilterInfoDialog
    
    def _make_delete_message(self, token_info):
        return "Do you want to Delete ?"

    def get_filters(self):
        return self.token_model.get_filters()
        
    # def _config(self, token_model: FilterModel):
    #     self.token_model = token_model
    #     self.tableView.setModel( token_model)
    #     self.accepted.connect( token_model.cb_write_token)
    #     self.rejected.connect( token_model.cb_refresh_token)
        