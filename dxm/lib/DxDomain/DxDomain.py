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
from masking_apis.models.domain import Domain
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxDomain(Domain):
    

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        Domain.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__domain_name = None
        self.__sync = None
        self.__logger.debug("creating DxDomain object")

    def from_domain(self, dom):
        """
        Copy properties from domain object into DxDomain
        :param column: Domain object
        """
        self.__dict__.update(dom.__dict__)
