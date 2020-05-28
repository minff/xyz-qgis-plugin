# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
# License-Filename: LICENSE
#
###############################################################################


from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem
from qgis.PyQt.QtCore import QIdentityProxyModel, Qt, QVariant
from .token_model import EditableGroupTokenInfoModel

class FilterModel(EditableGroupTokenInfoModel):
    INFO_KEYS = ["name","operator","values"]
    SERIALIZE_KEYS = []
    TOKEN_KEY = "name"
    DELIM = ","

    def __init__(self, parent=None):
        super().__init__(parent)        
        self.filters = list()
        self._refresh_token()
        
    def set_filters(self, filters):
        self.filters = list(filters)
    def get_filters(self):
        return self.filters

    def load_ini(self, ini):
        raise NotImplementedError()
    def _load_ini(self, ini):
        raise NotImplementedError()
    def _write_to_file(self):
        raise NotImplementedError()
    def set_default_servers(self, *a):
        raise NotImplementedError()

    def _refresh_token(self):
        self.cache_tokens = list()
        self.clear()
        self.setHorizontalHeaderLabels(self.INFO_KEYS)
        it = self.invisibleRootItem()
        for token_info in self.filters:
            if not token_info.get("name"): continue
            if not token_info.get("values"): continue
            it.appendRow([QStandardItem(t)  
                for t in self.items_from_token_info(token_info)
            ])

    def cb_write_token(self):
        self.filters = list(self.cache_tokens)

    def _cb_remove_token_from_file(self, root, i0, i1):
        if not self._is_valid_single_selection(i0, i1): return
        token = self.cache_tokens.pop(i0)

    def _cb_append_token_to_file(self, root, i0, i1):
        if not self._is_valid_single_selection(i0, i1): return
        token = self.get_token_info(i0)
        self.cache_tokens.insert(i0,token)

    def _cb_changed_token_to_file(self, idx_top_left, idx_bot_right):
        i0 = idx_top_left.row()
        i1 = idx_bot_right.row()
        if not self._is_valid_single_selection(i0, i1): return
        token = self.get_token_info(i0)
        self.cache_tokens[i0] = token

    # functions for lineedit

    def get_display_str(self):
        return "&".join(
            "".join(d[k] for k in ["name","operator","values"]) 
            for d in self.get_filters()
        )
