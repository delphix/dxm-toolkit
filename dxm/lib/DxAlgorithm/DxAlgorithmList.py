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
import operator
from masking_apis.apis.algorithm_api import AlgorithmApi
from masking_apis.apis.sync_api import SyncApi
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxAlgorithm.DxAlgorithm import DxAlgorithm
from dxm.lib.DxDomain.DxDomainList import DxDomainList
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxSync.DxSyncList import DxSyncList

class DxAlgorithmList(object):

    __algorithmList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxAlgorithmList object")
        if not self.__algorithmList:
            self.LoadAlgorithms()

    @classmethod
    def LoadAlgorithms(self):
        """
        Load list of algorithms
        Return None if OK
        """

        try:
            api_instance = AlgorithmApi(self.__engine.api_client)
            api_response = api_instance.get_all_algorithms()

            synclist = DxSyncList()
            sync = synclist.get_all_algorithms()

            # print "DUPKA"
            #
            # sys.exit(1)
            #
            # api_sync = SyncApi(self.__engine.api_client)
            # api_sync_response = api_sync.get_all_syncable_objects()
            # sync = dict([x.object_identifier['algorithmName'], x]
            #             for x in api_sync_response.response_list
            #             if 'algorithmName' in x.object_identifier)


            if api_response.response_list:
                for c in api_response.response_list:
                    alg = DxAlgorithm(self.__engine)
                    alg.from_alg(c)

                    dom = DxDomainList.get_domain_by_algorithm(c.algorithm_name)

                    if dom:
                        alg.domain_name = dom
                    else:
                        alg.domain_name = ''

                    if c.algorithm_name in sync:
                        alg.sync = 1
                    self.__algorithmList[c.algorithm_name] = alg
            else:
                print_error("No algorithm found")
                self.__logger.error("No algorithm found")
                return 1

            return None

        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a algorithm object by refrerence
        :param1 reference: algorithm name
        None if not found
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__algorithmList[reference]

        except KeyError as e:
            self.__logger.debug("can't find algorithm object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            return None


    @classmethod
    def get_allref(self, sortby1='algorithm_name'):
        """
        return a list of all references
        """
        return sorted(self.__algorithmList, key=lambda k:
                      getattr(self.__algorithmList[k], sortby1).lower())
