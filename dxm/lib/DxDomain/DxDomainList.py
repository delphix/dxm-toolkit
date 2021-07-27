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

from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxDomain.DxDomain import DxDomain
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxLogging import print_error
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.domain_api import DomainApi
from dxm.lib.masking_api.rest import ApiException

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
        self.LoadDomains()

    @classmethod
    def LoadDomains(self):
        """
        Load list of domains
        Return None if OK
        """

        self.__domainList.clear()
        self.__api = DomainApi
        self.__apiexc = ApiException

        try:
            api_instance = self.__api(self.__engine.api_client)
            domain_list = paginator(
                            api_instance,
                            "get_all_domains")

            if domain_list.response_list:
                for c in domain_list.response_list:
                    dom = DxDomain(self.__engine)
                    dom.from_domain(c)
                    self.__domainList[c.domain_name] = dom
            else:
                print_error("No domain found")
                self.__logger.error("No domain found")
                return 1

            return None

        except self.__apiexc as e:
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
            return None

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


    @classmethod
    def add(self, domainobj):
        """
        Add a domain to a list and Engine
        :param1 domainobj: DxDomain object to add to the list and engine
        return 0 if OK
        """

        if (domainobj.add() == 0):
            self.__logger.debug("Adding file type %s to list" % domainobj)
            self.__domainList[domainobj.domain_name] = domainobj
            return 0
        else:
            return 1

    @classmethod
    def delete(self, domainname):
        """
        Delete the domain from a list and Engine
        :param domainname: Domain name to delete
        return 0 if OK
        """

        domainobj = self.get_by_ref(domainname)
        if domainobj is not None:
            if domainobj.delete() is None:
                return 0
            else:
                return 1
        else:
            print_error("Domain name %s not found" % domainname)
            return 1
