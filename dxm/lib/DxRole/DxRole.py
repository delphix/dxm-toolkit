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
# Copyright (c) 2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : May 2019


import logging
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

from dxm.lib.masking_api.api.role_api import RoleApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.DxRole.Role_mixin import Role_mixin

class DxRole(Role_mixin):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Role.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine

        self.__api = RoleApi
        self.__apiexc = ApiException
        self._obj = None

    def from_role(self, role):
        self._obj = role
        self._obj.swagger_map = self.swagger_map
        self._obj.swagger_types = self.swagger_types

