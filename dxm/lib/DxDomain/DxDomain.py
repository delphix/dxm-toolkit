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
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.domain_api import DomainApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel
from dxm.lib.DxDomain.Domain_mixin import Domain_mixin

class DxDomain(Domain_mixin):


    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #Domain.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__sync = None
        self.__logger.debug("creating DxDomain object")


        self.__api = DomainApi
        self.__apiexc = ApiException
        self._obj = None


    def load_obj(self, dom):
        """
        Set obj properties with a Domain object
        :param column: Domain object
        """
        self._obj = dom
        self._obj.swagger_map = self.swagger_map
        self._obj.swagger_types = self.swagger_types




    def create_domain(self, domain_name, domain_classification, default_algorithm_code):
        self._obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.domain_name = domain_name
        self.obj.domain_classification = domain_classification
        self.obj.default_algorithm_code = default_algorithm_code



    def add(self):
        """
        Add File type to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.obj.domain_name is None):
            print_error("Domain name is required")
            self.__logger.error("Domain name is required")
            return 1

        if (self.obj.default_algorithm_code is None):
            print_error("Domain default algorithm is required")
            self.__logger.error("Domain default algorithm is required")
            return 1

        try:
            self.__logger.debug("create domain input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("API instance created")
            response = api_instance.create_domain(
                self.obj,
                _request_timeout=self.__engine.get_timeout()
            )
            self.load_obj(response)
            self.__logger.debug("domain response %s"
                                % str(response))

            print_message("Domain %s added" % self.obj.domain_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def delete(self):
        """
        Delete domain
        return a 0 if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete domain name %s"
                                % self.obj.domain_name)
            response = api_instance.delete_domain(
                self.obj.domain_name,
                _request_timeout=self.__engine.get_timeout()
            )
            self.__logger.debug("delete domain name response %s"
                                % str(response))
            print_message("Domain %s deleted" % self.obj.domain_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1


    def update(self):
        """
        Delete domain
        return a 0 if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("update domain name %s"
                                % self.domain_name)
            response = api_instance.update_domain(self.domain_name,
                self.obj,
                _request_timeout=self.__engine.get_timeout()
            )
            self.__logger.debug("delete domain name response %s"
                                % str(response))
            print_message("Domain %s updated" % self.domain_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1