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

from dxm.lib.masking_api.api.sync_api import SyncApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.DxAlgorithm.Algorithm_mixin import Algorithm_mixin

class DxAlgorithm(Algorithm_mixin):

    def __init__(self, engine, existing_object=None):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Algorithm.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__domain_name = None
        self.__sync = None
        self.__logger.debug("creating DxAlgorithm object")
        self._obj = None

        if existing_object is not None:
            self.load_object(existing_object)            

    def load_object(self, alg):
        """
        Set obj properties with a Algorithm object
        :param column: Algorithm object
        """
        self.obj = alg
        self.obj.swagger_map = self.swagger_map
        self.obj.swagger_types = self.swagger_types

    @property
    def domain_name(self):
        return self.__domain_name

    @domain_name.setter
    def domain_name(self, domain):
        self.__domain_name = domain

    @property
    def sync(self):
        return self.__sync

    @sync.setter
    def sync(self, sync):
        self.__sync = sync

