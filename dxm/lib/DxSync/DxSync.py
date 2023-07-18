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
# Copyright (c) 2018,2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : December 2018


import logging
import pickle
import json
import os
import re

from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.sync_api import SyncApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.DxSync.ExportObjectMetadata_mixin import ExportObjectMetadata_mixin

class DxSync(ExportObjectMetadata_mixin):

    import_swagger_types = {
        'export_response_metadata': 'dict',
        'blob': 'str',
        'signature': 'str',
        'public_key': 'str'
    }

    import_swagger_map = {
        'export_response_metadata': 'exportResponseMetadata',
        'blob': 'blob',
        'signature': 'signature',
        'public_key': 'publicKey'
    }


    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #ExportObjectMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__synctype = None
        self.__logger.debug("creating DxSync object")

        self.__api = SyncApi
        self.__apiexc = ApiException
        self._obj = None


    def load_object(self, sync):
        """
        Set obj properties with Sync object
        :param sync: Sync object
        """
        self._obj = sync
        self._obj.swagger_map = self.swagger_map
        self._obj.swagger_types = self.swagger_types
        self._obj.object_identifier.swagger_map = {
            'id' : 'id',
            'algorithm_name' : 'algorithmName'
        }
        self._obj.object_identifier.swagger_types = {
            'id' : 'int',
            'algorithm_name' : 'str'
        }



    def export(self, name, path=None):
        """
        Export algorithm into file
        :param path: path to save algorithm
        """
        api_sync = self.__api(self.__engine.api_client)
        self.__logger.debug("Export input {}".format(self.obj))


        check = re.match(r'Not Syncable: (.*)', self.revision_hash)
        
        if check:
            print_error("Can't export - {}".format(check.groups()[0]))
            return 1

        export_list = []
        export_list.append(self.obj)

        api_response = api_sync.export(export_list)
        self.__logger.debug("Export response (without blob) %s"
                            % str(api_response.export_response_metadata))
        filename = os.path.join(path, '{}_{}.bin'.format(self.object_type.lower(), name))
        self.__logger.debug("saving to %s" % filename)

        dependencylist = [
            b["object_type"]
            for b
            in api_response.export_response_metadata.to_dict()["exported_object_list"]]

        try:
            binary_file = open(filename, mode='wb')
            pickle.dump(api_response, binary_file)
            binary_file.close()
            print_message("Exported object types: ")
            print_message(",".join(dependencylist))
            print_message("Object saved to %s" % filename)
            return 0
        except Exception as e:
            self.__logger.debug("Problem with saving object to %s" % filename)
            self.__logger.debug(str(e))
            print_error("Problem with saving object to %s" % filename)
            print_error(str(e))
            return 1


    def importsync(self, path, environment_id, force):
        """
        Import algorithm from file
        :param1 path: path to save algorithm
        :param2 environment_id: target envitonment id
        :param3 force: force import
        """

        try:
            binary_file = path
            syncobj = pickle.load(binary_file)
            binary_file.close()
        except Exception as e:
            print_error("There is an error with reading file %s"
                        % path.name)
            self.__logger.debug("There is an error with reading file %s"
                                % path.name)
            return 1


        syncobj.swagger_types = self.import_swagger_types
        syncobj.swagger_map = self.import_swagger_map

        try:
            api_sync = self.__api(self.__engine.api_client)
            self.__logger.debug("Import input %s" % self)
            if environment_id is None:
                api_response = api_sync.import_object(
                                syncobj,
                                force_overwrite=force)
            else:
                api_response = api_sync.import_object(
                                syncobj,
                                force_overwrite=force,
                                environment_id=environment_id)
            self.__logger.debug("Import response %s" % str(api_response))
            print_message("File %s was loaded or engine revision is in "
                          "sync with file" % path.name)
            self.__logger.debug("File %s was loaded or engine revision is in "
                                "sync with file" % path.name)
            return 0
        except self.__apiexc as e:
            if e.status == 404 or e.status == 409:
                print_error("Problem with depended objects")
                errpyt = json.loads(e.body)
                for err in errpyt:
                    if err["importStatus"] == "FAILED":
                        print_error("%s %s %s %s" % (
                                    err["objectIdentifier"],
                                    err["objectType"],
                                    err["importStatus"],
                                    err["failureMessage"]))
                        self.__logger.debug("%s %s %s %s" % (
                                    err["objectIdentifier"],
                                    err["objectType"],
                                    err["importStatus"],
                                    err["failureMessage"]))
                    else:
                        print_error("%s %s %s" % (
                                    err["objectIdentifier"],
                                    err["objectType"],
                                    err["importStatus"]))
                        self.__logger.debug("%s %s %s" % (
                                    err["objectIdentifier"],
                                    err["objectType"],
                                    err["importStatus"]))

                return 1
            else:
                print_error("Problem with importing object from path %s"
                            % path.name)
                print_error(str(e))
                self.__logger.debug("Problem with importing object from path %s"
                                    % path.name)
                self.__logger.debug(str(e))
                return 1
