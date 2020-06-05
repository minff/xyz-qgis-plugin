# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
# License-Filename: LICENSE
#
###############################################################################


from ..xyz_qgis.models.token_model import (
    EditableGroupTokenInfoModel,
    EditableGroupTokenInfoWithServerModel)
from .base_token_dialog import BaseTokenDialog
from .ux.server_ux import ServerUX


class TokenDialog(BaseTokenDialog, ServerUX):
    
    def __init__(self, parent=None):
        """init window"""
        super().__init__(parent)
        self.comboBox_server_url.setVisible(True)
        self.btn_server.setVisible(True)

    def exec_(self):
        self.comboBox_server_url.setCurrentIndex(self.get_active_server_idx())
        return super().exec_()

    def config(self, token_model: EditableGroupTokenInfoModel):
        BaseTokenDialog.config(self, token_model)

    def config_server(self, server_model: EditableGroupTokenInfoWithServerModel, comboBox_server_url):
        ServerUX.config(self, server_model)
        
        self.comboBox_server_url.currentIndexChanged[int].connect(comboBox_server_url.setCurrentIndex)
        self.btn_server.clicked.connect(self.open_server_dialog)
        
