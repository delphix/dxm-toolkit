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
import sys
from masking_apis.apis.domain_api import DomainApi
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxDomain.DxDomain import DxDomain
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxDomainList(object):

    __domainList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxDomainList object")

    @classmethod
    def LoadDomains(self):
        """
        Load list of domains
        Return None if OK
        """

        try:
            api_instance = DomainApi(self.__engine.api_client)
            api_response = api_instance.get_all_domains()

            if api_response.response_list:
                for c in api_response.response_list:
                    dom = DxDomain(self.__engine)
                    dom.from_domain(c)
                    self.__domainList[c.domain_name] = dom
            else:
                print_error("No domain found")
                self.__logger.error("No domain found")
                return 1
                
            return None

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a domain object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__domainList[reference]

        except KeyError as e:
            self.__logger.debug("can't find domain object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__domainList.keys()

    @classmethod
    def get_domain_by_name(self, name):
        """
        Domain name is a ref 
        """
        return self.get_by_ref(name)

    @classmethod
    def get_domain_by_algorithm(self, alg):
        domains = get_objref_by_val_and_attribute(alg, self, 'default_algorithm_code')
        if len(domains) < 1:
            print_error("Domain for algorithm %s not found" % alg)
            self.__logger.error("Domain for algorithm %s not found" % alg)
            return None

        if len(domains) > 1:
            print_error("Domain for algorithm %s is not unique" % alg)
            self.__logger.error("Domain for algorithm %s is not unique" % alg)
            return None

        return domains[0]