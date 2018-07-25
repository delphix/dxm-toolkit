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
# Date    : March 2018
# Comments: List of the Database connectors


import logging
from dxm.lib.DxConnector.DxConnector import DxConnector


class SybaseConnector(DxConnector):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DxConnector.__init__(self, engine)
        self.database_type = 'SYBASE'
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating SybaseConnector object")



    def get_type_properties(self):
        """
        Return dict with properties specific for connector type
        """
        props = {
            'username': self.username,
            'databaseName': self.database_name,
        }
        return props

    def get_properties(self):
        """
        Return dict with properties required for connector type
        """

        props = {
            'port': self.port,
            'host': self.host,
            'username': self.username,
            'schemaName': self.schema_name,
            'connectorName': self.connector_name,
            'password': self.password,
            'databaseType': self.database_type,
            'environmentId': self.environment_id,
            'databaseName': self.database_name
        }

        empty = 0
        for k in props.keys():
            if (props[k] is None):
                print "Property %s can't be empty" % k
                empty = empty + 1

        if empty == 0:
            return props
        else:
            return None
