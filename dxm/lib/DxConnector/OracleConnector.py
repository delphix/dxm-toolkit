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


class OracleConnector(DxConnector):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DxConnector.__init__(self, engine)
        self.__engine = engine
        self.database_type = 'ORACLE'
        self.__logger = logging.getLogger()
        self.__logger.debug("creating OracleConnector object")

    @property
    def schema_name(self):
        return self._schema_name

    @schema_name.setter
    def schema_name(self, schema_name):
        """
        schemaName
        :param schemaName: Schema Name
        """
        self._schema_name = schema_name.upper()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        """
        username
        :param username: User Name
        """
        self._username = username.upper()

    def get_type_properties(self):
        """
        Return dict with properties specific for connector type
        """
        props = {
            'loginID': self.username,
            'SID': self.sid,
        }
        return props


    def get_properties(self):
        """
        Return dictionaty with properties required for connector type
        """


        props = {
            'sid': self.sid,
            'port': self.port,
            'host': self.host,
            'username': self.username,
            'schema_name': self.schema_name,
            'connector_name': self.connector_name,
            'password': self.password,
            'database_type': self.database_type,
            'environment_id': self.environment_id
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
