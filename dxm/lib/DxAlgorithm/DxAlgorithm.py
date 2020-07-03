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

from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxAlgorithm(object):

    def __init__(self, engine):
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
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.algorithm import Algorithm
            from masking_api_60.api.sync_api import SyncApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.algorithm import Algorithm
            from masking_api_53.api.sync_api import SyncApi
            from masking_api_53.rest import ApiException

        self.__api = SyncApi
        self.__model = Algorithm
        self.__apiexc = ApiException
        self.__obj = None


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    def from_alg(self, alg):
        """
        Set obj properties with a Algorithm object
        :param column: Algorithm object
        """
        self.__obj = alg

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

    @property
    def algorithm_name(self):
        if self.obj is not None:
            return self.obj.algorithm_name
        else:
            return None

    @property
    def algorithm_type(self):
        if self.obj is not None:
            return self.obj.algorithm_type
        else:
            return None

    # def export(self, path=None):
    #     """
    #     Export algorithm into file
    #     :param path: path to save algorithm
    #     """
    #     api_sync = SyncApi(self.__engine.api_client)
    #     self.__logger.debug("Export input %s" % self.sync)
    #     export_list = []
    #     export_list.append(self.sync)
    #     api_response = api_sync.export(export_list)
    #     self.__logger.debug("Export response %s" % str(api_response))
    #
    #     # binary_file = open('{0}.alg'.format(self.algorithm_name), mode='wb')
    #     # json.dump(api_response.blob, binary_file)
    #     # binary_file.close()
    #
    #     binary_file = open('{0}.alg_bin '.format(self.algorithm_name), mode='wb')
    #     pickle.dump(api_response, binary_file)
    #     binary_file.close()
    #
    #
    # def importalg(self, path=None):
    #     """
    #     Import algorithm from file
    #     :param path: path to save algorithm
    #     """
    #
    #     binary_file = open('{0}.alg_bin'.format("EU_LAST_NAME"), mode='rb')
    #     algobj = pickle.load(binary_file)
    #     binary_file.close()
    #
    #
    #     api_sync = SyncApi(self.__engine.api_client)
    #     self.__logger.debug("Import input %s" % self.sync)
    #     api_response = api_sync.import_object(algobj, force_overwrite=True)
    #     self.__logger.debug("Import response %s" % str(api_response))
    #
    #     # binary_file = open('{0}.alg'.format(self.algorithm_name), mode='wb')
    #     # json.dump(api_response.blob, binary_file)
    #     # binary_file.close()
