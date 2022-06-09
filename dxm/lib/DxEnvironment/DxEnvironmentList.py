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
# Copyright (c) 2018-2020 by Delphix. All rights reserved.
#
# Author  : Edward de los Santos
# Author  : Marcin Przepiorowski
# Date    : March 2018


import logging
import sys
from dxm.lib.DxEnvironment.DxEnvironment import DxEnvironment
from dxm.lib.DxApplication.DxApplicationList import DxApplicationList
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator 
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxLogging import print_error
from dxm.lib.masking_api.api.environment_api import EnvironmentApi
from dxm.lib.masking_api.rest import ApiException

class DxEnvironmentList(object):

    # global list of environments on the class level
    __environmentList = {}
    __engine = None
    __logger = None
    __loaded_engine = None

    @classmethod
    def __init__(self):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxEnvironmentList object")
        self.LoadEnvironments()

    @classmethod
    def LoadEnvironments(self):
        """
        Load environment list from Engine into global list
        return None if OK
        return 1 if error
        """


        if self.__loaded_engine is None:
            self.__loaded_engine = self.__engine.get_name()

        
        if self.__loaded_engine == self.__engine.get_name() and self.__environmentList != {}:
           return None
        else:
            # delete a list as we can have multi engines
            self.__environmentList.clear()
            self.__loaded_engine = self.__engine.get_name()

        appList = DxApplicationList()
        appList.LoadApplications()
        self.__api = EnvironmentApi
        self.__apiexc = ApiException

        try:
            api_instance = self.__api(self.__engine.api_client)
            envlist = paginator(
                        api_instance,
                        "get_all_environments",
                        _request_timeout=self.__engine.get_timeout())

            if envlist.response_list:
                for c in envlist.response_list:
                    environment = DxEnvironment(self.__engine)
                    environment.from_environment(c)
                    if hasattr(c, "application_id"):
                        app = appList.get_by_ref(c.application_id)
                        environment.application_name = app.application_name
                    self.__environmentList[c.environment_id] = environment
            else:
                self.__logger.error("No environments found")
                #print_error("No environments found")

        except self.__apiexc as e:
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
            self.__logger.debug(self.__environmentList[reference])
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
        self.__logger.debug("Search for environement: {}".format(name))
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


        self.__logger.debug("Found: {}".format(environments[0]))
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
                del self.__environmentList[environmentId]
                return None
            else:
                return 1
        else:
            print_error("Environment with id %s not found" % environmentId)
            return 1
