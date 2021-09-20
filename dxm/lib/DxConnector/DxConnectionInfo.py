#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2018 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : April 2018


import logging
import time
import pprint
import pytz
from tqdm import tqdm
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.genericmodel import GenericModel



class DxConnectionInfo(object):

    swagger_types = {
        'connection_mode': 'str',
        'path': 'str',
        'mount_id': 'int',
        'host': 'str',
        'login_name': 'str',
        'password': 'str',
        'port': 'int',
        'ssh_key': 'str',
        'user_dir_is_root': 'bool'
    }

    swagger_map = {
        'connection_mode': 'connectionMode',
        'path': 'path',
        'mount_id': 'mountId',
        'host': 'host',
        'login_name': 'loginName',
        'password': 'password',
        'port': 'port',
        'ssh_key': 'sshKey',
        'user_dir_is_root': 'userDirIsRoot'
    }

    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def connection_mode(self):
        if self.obj is not None and hasattr(self.obj,'connection_mode'):
            return self.obj.connection_mode
        else:
            return None

    @connection_mode.setter
    def connection_mode(self, connection_mode):
        if self.obj is not None:
            self.obj.connection_mode = connection_mode
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def path(self):
        if self.obj is not None and hasattr(self.obj,'path'):
            return self.obj.path
        else:
            return None

    @path.setter
    def path(self, path):
        if self.obj is not None:
            self.obj.path = path
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def mount_id(self):
        if self.obj is not None and hasattr(self.obj,'mount_id'):
            return self.obj.mount_id
        else:
            return None

    @mount_id.setter
    def mount_id(self, mount_id):
        if self.obj is not None:
            self.obj.mount_id = mount_id
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def host(self):
        if self.obj is not None and hasattr(self.obj,'host'):
            return self.obj.host
        else:
            return None

    @host.setter
    def host(self, host):
        if self.obj is not None:
            self.obj.host = host
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def login_name(self):
        if self.obj is not None and hasattr(self.obj,'login_name'):
            return self.obj.login_name
        else:
            return None

    @login_name.setter
    def login_name(self, login_name):
        if self.obj is not None:
            self.obj.login_name = login_name
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def password(self):
        if self.obj is not None and hasattr(self.obj,'password'):
            return self.obj.password
        else:
            return None

    @password.setter
    def password(self, password):
        if self.obj is not None:
            self.obj.password = password
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def port(self):
        if self.obj is not None and hasattr(self.obj,'port'):
            return self.obj.port
        else:
            return None

    @port.setter
    def port(self, port):
        if self.obj is not None:
            self.obj.port = port
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def ssh_key(self):
        if self.obj is not None and hasattr(self.obj,'ssh_key'):
            return self.obj.ssh_key
        else:
            return None

    @ssh_key.setter
    def ssh_key(self, ssh_key):
        if self.obj is not None:
            self.obj.ssh_key = ssh_key
        else:
            raise ValueError("Object needs to be initialized first")


    @property
    def user_dir_is_root(self):
        if self.obj is not None and hasattr(self.obj,'user_dir_is_root'):
            return self.obj.user_dir_is_root
        else:
            return None

    @user_dir_is_root.setter
    def user_dir_is_root(self, user_dir_is_root):
        if self.obj is not None:
            self.obj.user_dir_is_root = user_dir_is_root
        else:
            raise ValueError("Object needs to be initialized first")

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()