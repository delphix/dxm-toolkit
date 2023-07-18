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
# Copyright (c) 2018.2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : November 2018


import logging
import sys

from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.DxSync.DxSync import DxSync
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.api.sync_api import SyncApi
from dxm.lib.masking_api.rest import ApiException


supported_alg_list = {
    "5.3" : ["SEGMENT", "DATE_SHIFT", "LOOKUP", "TOKENIZATION"], 
    "6.0.4" : ["SEGMENT", "DATE_SHIFT", "LOOKUP", "TOKENIZATION", "USER_ALGORITHM"]
}

class DxSyncList(object):

    __syncableList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self, type=None):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxSyncList object")
        self.LoadSync(type)

    @classmethod
    def LoadSync(self, objecttype=None):
        """
        Load list of syncable objects
        param1: type: load only particular type
        Return None if OK
        """

        self.__syncableList = {}

        self.__api = SyncApi
        self.__apiexc = ApiException

        api_sync_response = None

        if self.__engine.version_le("6.0.3"): # to check
            alglist = supported_alg_list["5.3"]
        else:
            alglist = supported_alg_list["6.0.4"]

        try:
            api_sync = self.__api(self.__engine.api_client)
            if objecttype:
                objecttype = objecttype.upper()

            if objecttype and self.__engine.version_ge("5.3"):
                if objecttype == "ALGORITHM":
                    for atype in alglist:
                        print("trying to get {}".format(atype))
                        partres = paginator(
                                      api_sync,
                                      "get_all_syncable_objects",
                                      object_type=atype)
                        if api_sync_response is None:
                            api_sync_response = partres
                        else:
                            api_sync_response.response_list = \
                                api_sync_response.response_list + \
                                partres.response_list
                else:
                    api_sync_response = paginator(
                                            api_sync,
                                            "get_all_syncable_objects",
                                            object_type=objecttype)
            else:
                if (objecttype is None) \
                   or (objecttype in
                   ["LOOKUP", "DATE_SHIFT", "SEGMENT",
                    "TOKENIZATION", "ALGORITHM"]):
                    api_sync_response = paginator(
                                            api_sync,
                                            "get_all_syncable_objects")
                else:
                    print_error("This object type is not supported"
                                "in version 5.2.X")
                    sys.exit(1)

            if api_sync_response.response_list:
                for c in api_sync_response.response_list:
                    syncobj = DxSync(self.__engine)
                    syncobj.load_object(c)
                    stype = syncobj.object_type

                    if stype in alglist:
                        stype = "ALGORITHM"

                    # print(type(syncobj))
                    # print(type(syncobj.object_identifier))

                    sid = list(syncobj.object_identifier.to_dict().values())[0]
                    if stype not in self.__syncableList:
                        self.__syncableList[stype] = {}
                    self.__syncableList[stype][sid] = syncobj
            else:
                print_error("No syncobject found")
                self.__logger.error("No syncobject found")
                return 1

            return None

        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e.body)
            return 1

    @classmethod
    def get_all_algorithms(self):
        """
        return a list of syncable algorithms
        """

        allalg = self.__syncableList["ALGORITHM"]

        #print(allalg[0].object_identifier.__dict__)

        # check with older engine 
        return sorted(allalg, key=lambda k:
                      allalg[k].object_identifier.algorithm_name.lower())

    @classmethod
    def get_object_by_type_name(self, objecttype, name):
        """
        return an object by type and name
        param1: objectype: object type to return
        param2: name: object name
        """
        try:
            objecttype = objecttype.upper()
            if name in self.__syncableList[objecttype]:
                return self.__syncableList[objecttype][name]
            else:
                return None
        except KeyError:
            # it can happen for older engines using newer dxmc
            return None

    @classmethod
    def get_all_object_by_type(self, objecttype):
        """
        return a list of object type
        param1: objectype: object type to return
        """
        objecttype = objecttype.upper()
        try:
            return self.__syncableList[objecttype]
        except KeyError:
            return []
