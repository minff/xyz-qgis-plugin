# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 HERE Europe B.V.
#
# SPDX-License-Identifier: MIT
# License-Filename: LICENSE
#
###############################################################################


import configparser

from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem
from qgis.PyQt.QtCore import QIdentityProxyModel, Qt, QVariant

class UsedToken():
    def __init__(self):
        self.set_invalid_token_idx(0)
    def set_invalid_token_idx(self, invalid_idx):
        self.invalid_idx = invalid_idx
        self.reset_used_token_idx()
    def get_invalid_token_idx(self):
        return self.invalid_idx
    def set_used_token_idx(self, idx):
        self.used_token_idx = idx
    def get_used_token_idx(self):
        return self.used_token_idx
    def reset_used_token_idx(self):
        self.used_token_idx = self.invalid_idx

class EditableGroupTokenInfoModel(QStandardItemModel, UsedToken):
    """ Grouped Token Model, Cached changes and write to file at the end
    """
    INFO_KEYS = ["name","token"]
    SERIALIZE_KEYS = ["token","name"]
    TOKEN_KEY = "token"
    DELIM = ","

    def __init__(self, parent=None):
        super().__init__(parent)
        UsedToken.__init__(self)
        self.ini = ""
        self._config_callback() # persistent
        self.group_key = "PRD"

    def update_from_model(self, other_model):
        self.token_groups.read_dict(other_model.get_dict())

    def get_dict(self):
        # return dict(self.token_groups._sections)
        return {s: dict(self.token_groups.items(s)) for s in self.token_groups.sections()}
        
    def load_ini(self, ini):
        self._load_ini(ini)
        self.ini = ini # must be after loaded
        self._refresh_token()
        
    def get_ini(self):
        return self.ini
    

    def _write_to_file(self):
        if self.ini == "": return
        with open(self.ini, "w") as f:
            self.token_groups.write(f)

    
    def set_default_servers(self, default_api_urls):
        self.default_api_urls = default_api_urls
        self.default_api_envs = {v:k for k, v in default_api_urls.items()}

    def set_server(self, server):
        # TODO default_api_envs not guaranteed to be init
        self.group_key = self.default_api_envs.get(server, server)
        self._refresh_token()

    def _refresh_token(self):
        self.cache_tokens = list()
        s = self.group_key
        if not self.token_groups.has_section(s):
            self.token_groups.add_section(s)
        tokens = self.token_groups.options(s)
        self.clear()
        
        self.setHorizontalHeaderLabels(self.INFO_KEYS)
        it = self.invisibleRootItem()
        # it.appendRow(QStandardItem())
        
        for line in tokens:
            if not line: continue
            token_info = self.deserialize_line(line)
            if not token_info.get(self.TOKEN_KEY): continue
            if token_info.get(self.TOKEN_KEY) == "[]": continue
            it.appendRow([QStandardItem(t)  
                for t in self.items_from_token_info(
                    token_info
                )
            ])

    def _load_ini(self, ini):
        token_groups = configparser.ConfigParser(allow_no_value=True,delimiters=("*",))
        token_groups.optionxform = str
        with open(ini,"a+") as f:
            f.seek(0)
            token_groups.read_file(f)
        self.token_groups = token_groups

    def get_text(self, row, col):
        it = self.item(row, col)
        return it.text().strip() if it else "None"

    def get_token_info(self, row):
        return dict(
            [k, self.get_text(row, col)]
            for col, k in enumerate(self.INFO_KEYS)
        )

    def items_from_token_info(self, token_info: dict):
        return [token_info.get(k,"") for k in self.INFO_KEYS]

    def deserialize_line(self, line):
        infos = line.split(self.DELIM,maxsplit=1)
        return dict(zip(self.SERIALIZE_KEYS, map(str.strip, infos)))

    def serialize_token_row(self, row):
        return self.serialize_token_info(self.get_token_info(row))

    def serialize_token_info(self, token_info):
        lst_txt = [token_info.get(k,"").strip() for k in self.SERIALIZE_KEYS]
        return self.DELIM.join(lst_txt)



    def cb_refresh_token(self):
        self._refresh_token()

    def _config_callback(self):
        try: self.rowsInserted.disconnect()
        except TypeError: pass
        try: self.rowsAboutToBeRemoved.disconnect()
        except TypeError: pass

        self.rowsInserted.connect(self._cb_append_token_to_file)

        # persistent remove (uncomment next line)
        self.rowsAboutToBeRemoved.connect(self._cb_remove_token_from_file)

        try: self.itemChanged.disconnect()
        except TypeError: pass
        # self.rowsMoved.connect(print)
        self.dataChanged.connect(self._cb_changed_token_to_file)

    def cb_write_token(self):
        self.token_groups.remove_section(self.group_key)
        self.token_groups.add_section(self.group_key)
        tokens = self.token_groups.options(self.group_key)
        for token in self.cache_tokens:
            if token.startswith("[]"): print(token)
            self.token_groups.set(self.group_key, token)
        tokens = self.token_groups.options(self.group_key)
        # clean unwanted sections
        for s in self.token_groups.sections():
            if not s: self.token_groups.remove_section(s)
        self._write_to_file()

    def _cb_remove_token_from_file(self, root, i0, i1):
        if not self._is_valid_single_selection(i0, i1): return
        token = self.cache_tokens.pop(i0)

    def _cb_append_token_to_file(self, root, i0, i1):
        if not self._is_valid_single_selection(i0, i1): return
        token = self.serialize_token_row(i0)
        self.cache_tokens.insert(i0,token)

    def _cb_changed_token_to_file(self, idx_top_left, idx_bot_right):
        i0 = idx_top_left.row()
        i1 = idx_bot_right.row()
        if not self._is_valid_single_selection(i0, i1): return
        token = self.serialize_token_row(i0)
        self.cache_tokens[i0] = token

    def _is_valid_single_selection(self, i0, i1):
        """ check for valid single selection (no text input)
        """
        return i0 == i1

class EditableGroupTokenInfoWithServerModel(EditableGroupTokenInfoModel):
    INFO_KEYS = ["name","server"]
    SERIALIZE_KEYS = ["server","name"]
    TOKEN_KEY = "server"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_key = "servers"
        self.set_server = lambda a: None
    
    def set_default_servers(self, default_api_urls):
        self.default_api_urls = default_api_urls
        self.default_api_envs = {v:k for k, v in default_api_urls.items()}
        self._init_default_servers([
            dict(name="HERE Server", server=default_api_urls["PRD"])
        ])

    def _init_default_servers(self, server_infos: list):
        tokens = self.token_groups.options(self.group_key)
        # if tokens: return
        existing_server = dict()
        for idx, token in enumerate(tokens):
            existing_server.setdefault(self.deserialize_line(token)["server"], list()).append(idx)
        
        it = self.invisibleRootItem()
        
        # # remove existing default server
        # removed_idx = sorted(sum((
        #     existing_server.get(sv, list())
        #     for server_info in server_infos
        #     for sv in server_info.pop("old_servers", list()) + [server_info["server"]]
        #     ), list()), reverse=True)
        # for idx in removed_idx:
        #     it.removeRow(idx)

        # add default server
        for i, server_info in enumerate(server_infos):
            if server_info["server"] in existing_server: continue
            if not server_info.get(self.TOKEN_KEY): continue
            it.insertRow(i,[QStandardItem(t)
                for t in self.items_from_token_info(
                    server_info
                )
            ])
        self.cb_write_token()

class ComboBoxProxyModel(QIdentityProxyModel):
    def __init__(self, token_key="token", named_token="{name}", nonamed_token="<noname token> {token}"):
        super().__init__()
        self.token_key = token_key
        self.named_token = named_token
        self.nonamed_token = nonamed_token
    def set_keys(self, keys):
        """ set header keys
        """
        self.keys = keys
        self.col_name = self.get_key_index("name")
        self.col_token = self.get_key_index(self.token_key)
    def get_key_index(self, key):
        return self.keys.index(key)
    def get_value(self, row, col, role):
        return self.sourceModel().item(row, col).data(role)
    def get_text(self, row, col):
        return self.sourceModel().item(row, col).text().strip()
    def get_token(self, row):
        it = self.sourceModel().item(row, self.col_token)
        return it.text().strip() if it else ""
    def data(self, index, role):
        val = super().data(index, role)
        if role == Qt.DisplayRole:
            name = self.get_text(index.row(), self.col_name)
            token = self.get_text(index.row(), self.col_token)
            if token:
                msg = self.named_token.format(name=name, token=token) if name else self.nonamed_token.format(token=token)
                return QVariant(msg)
        return val
