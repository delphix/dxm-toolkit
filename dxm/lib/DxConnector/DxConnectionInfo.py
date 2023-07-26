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



import pprint
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxConnector.ConnectionInfo_mixin import ConnectionInfo_mixin


class DxConnectionInfo(ConnectionInfo_mixin):


    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)


