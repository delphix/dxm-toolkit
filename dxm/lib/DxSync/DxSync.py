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
import pickle
import json
import os
from masking_apis.models.export_object_metadata import ExportObjectMetadata
from masking_apis.apis.sync_api import SyncApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxSync(ExportObjectMetadata):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        ExportObjectMetadata.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__synctype = None
        self.__logger.debug("creating DxSync object")


    def from_sync(self, sync):
        """
        Copy properties from algorithm object into DxAlgorithm
        :param column: Algorithm object
        """
        self.__dict__.update(sync.__dict__)

    def export(self, name, path=None):
        """
        Export algorithm into file
        :param path: path to save algorithm
        """
        api_sync = SyncApi(self.__engine.api_client)
        self.__logger.debug("Export input %s" % self)
        export_list = []
        export_list.append(self)
        api_response = api_sync.export(export_list)
        self.__logger.debug("Export response (without blob) %s"
                            % str(api_response.export_response_metadata))

        # binary_file = open('{0}.alg'.format(self.algorithm_name), mode='wb')
        # json.dump(api_response.blob, binary_file)
        # binary_file.close()

        filename = os.path.join(path, '{0}.bin'.format(name))
        self.__logger.debug("saving to %s" % filename)
        dependencylist = [
            b["objectType"]
            for b
            in api_response.export_response_metadata["exportedObjectList"]]

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

        try:
            api_sync = SyncApi(self.__engine.api_client)
            self.__logger.debug("Import input %s" % self)
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
        except ApiException as e:
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
        # binary_file = open('{0}.alg'.format(self.algorithm_name), mode='wb')
        # json.dump(api_response.blob, binary_file)
        # binary_file.close()
