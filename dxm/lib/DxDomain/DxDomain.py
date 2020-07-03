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


class DxDomain(object):
    

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
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.domain import Domain
            from masking_api_60.api.domain_api import DomainApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.domain import Domain
            from masking_api_53.api.domain_api import DomainApi
            from masking_api_53.rest import ApiException

        self.__api = DomainApi
        self.__model = Domain
        self.__apiexc = ApiException
        self.__obj = None

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    def from_domain(self, dom):
        """
        Set obj properties with a Domain object
        :param column: Domain object
        """
        self.__obj = dom

    @property
    def domain_name(self):
        if self.obj is not None:
            return self.obj.domain_name
        else:
            return None

    @property
    def default_algorithm_code(self):
        if self.obj is not None:
            return self.obj.default_algorithm_code
        else:
            return None

    @property
    def default_tokenization_code(self):
        if self.obj is not None:
            return self.obj.default_tokenization_code
        else:
            return None

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

        if (self.obj.classification is None):
            print_error("Domain classification is required")
            self.__logger.error("Domain classification is required")
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
                self,
                _request_timeout=self.__engine.get_timeout()
            )
            self.from_domain(response)
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

        api_instance = DomainApi(self.__engine.api_client)

        try:
            self.__logger.debug("update domain name %s"
                                % self.domain_name)
            response = api_instance.update_domain(self.domain_name,
                self,
                _request_timeout=self.__engine.get_timeout()
            )
            self.__logger.debug("delete domain name response %s"
                                % str(response))
            print_message("Domain %s updated" % self.domain_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1