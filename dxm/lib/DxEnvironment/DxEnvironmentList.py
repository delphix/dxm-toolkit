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
# Author  : Edward de los Santos
# Author  : Marcin Przepiorowski
# Date    : March 2018


import logging
import sys
from dxm.lib.DxEnvironment.DxEnvironment import DxEnvironment
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from masking_apis.apis.environment_api import EnvironmentApi
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error


class DxEnvironmentList(object):

    # global list of environments on the class level
    __environmentList = {}
    __engine = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxEnvironmentList object")

    @classmethod
    def LoadEnvironments(self):
        """
        Load environment list from Engine into global list
        return None if OK
        return 1 if error
        """

        self.__environmentList.clear()
        try:
            api_instance = EnvironmentApi(self.__engine.api_client)
            a = api_instance.get_all_environments(
                _request_timeout=self.__engine.get_timeout())

            if a.response_list:
                for c in a.response_list:
                    environment = DxEnvironment(self.__engine)
                    environment.from_environment(c)
                    self.__environmentList[c.environment_id] = environment
            else:
                self.__logger.error("No environments found")
                print_error("No environments found")

        except ApiException as e:
            self.__logger.error("Can't load environment %s" % e.body)
            print_error("Can't load environment %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a Environment object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__environmentList[reference]

        except KeyError as e:
            self.__logger.debug("can't find Environment object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__environmentList.keys()

    @classmethod
    def get_environmentId_by_name(self, name):
        """
        Return an environment id for name
        :param name: Environment name
        return environmnent_id if found
        return None if not found or not unique
        """
        environments = get_objref_by_val_and_attribute(name, self,
                                                       'environment_name')
        if len(environments) < 1:
            print_error("Environment %s not found" % name)
            self.__logger.error("Environment %s not found " % name)
            return None

        if len(environments) > 1:
            print_error("Environment name %s is not unique" % name)
            self.__logger.error("Environment %s is not unique" % name)
            return None

        return environments[0]


    @classmethod
    def add(self, environment):
        """
        Add an environment to a list and Engine
        :param environment: Environment object to add to Engine and list
        return None if OK
        """

        if (environment.add() is None):
            self.__logger.debug("Adding environment %s to list" % environment)
            self.__environmentList[environment.environment_id] = environment
            return None
        else:
            return 1

    @classmethod
    def delete(self, environmentId):
        """
        Delete an environment from a list and Engine
        :param environmentId: Environment id to delete from Engine and list
        return None if OK
        """

        environment = self.get_by_ref(environmentId)
        if environment is not None:
            if environment.delete() is None:
                return None
            else:
                return 1
        else:
            print "Environment with id %s not found" % environmentId
            return 1
