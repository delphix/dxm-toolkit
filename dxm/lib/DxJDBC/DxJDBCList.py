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
# Date    : August 2021


import logging
import sys
from dxm.lib.DxJDBC.DxJDBC import DxJDBC
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxLogging import print_error
from dxm.lib.masking_api.api.jdbc_driver_api import JdbcDriverApi
from dxm.lib.masking_api.rest import ApiException

class DxJDBCList(object):

    __engine = None
    __driverList = {}
    __logger = None

    @classmethod
    def __init__(self):
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxJDBCList object")        
        if not self.__driverList:
            self.LoadDrivers()

    @classmethod
    def LoadDrivers(self):
        """
        Load list of drivers
        Return None if OK
        """

        self.__api = JdbcDriverApi
        self.__apiexc = ApiException

        try:
            api_instance = self.__api(self.__engine.api_client)

            drivers = paginator(
                            api_instance,
                            "get_all_jdbc_drivers")

            if drivers.response_list:
                for c in drivers.response_list:
                    driver = DxJDBC(self.__engine)
                    driver.from_driver(c)
                    self.__driverList[c.jdbc_driver_id] = driver
            else:
                print_error("No JDBC drivers found")
                self.__logger.error("No JDBC drivers found")

        except self.__apiexc as e:
            print_error("Can't load JDBC drivers %s" % e.body)
            return None

    @classmethod
    def get_by_ref(self, reference):
        """
        return a driver object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__driverList[reference]

        except KeyError as e:
            self.__logger.debug("can't find driver object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__driverList.keys()

    @classmethod
    def get_driver_id_by_name(self, name):
        reflist = self.get_driver_id_by_name_worker(name)
        # convert list to single value
        # as there will be only one element in list
        if reflist:
            return reflist[0]
        else:
            return None

    @classmethod
    def get_all_driver_id_by_name(self, name):
        reflist = self.get_driver_id_by_name_worker(name)
        return reflist


    @classmethod
    def get_driver_id_by_name_worker(self, name, check_uniqueness=1):
        """
        :param1 name: name of ruleset
        :param2 check_uniqueness: check uniqueness put None if skip this check
        return list of rulesets
        """
        reflist = get_objref_by_val_and_attribute(name, self, 'driver_name')
        if len(reflist) == 0:
            self.__logger.error('Driver %s not found' % name)
            print_error('Driver %s not found' % name)
            return None

        if check_uniqueness:
            if len(reflist) > 1:
                self.__logger.error('File format %s is not unique' % name)
                print_error('File format %s is not unique' % name)
                return None

        return reflist


    @classmethod
    def add(self, driver):
        """
        Add an File type to a list and Engine
        :param ruleset: File type object to add to Engine and list
        return None if OK
        """

        if (driver.add() == 0):
            self.__logger.debug("Adding driver %s to list" % driver)
            self.__driverList[driver.jdbc_driver_id] = driver
            return None
        else:
            return 1

    @classmethod
    def delete(self, driver_ref):
        """
        Add an File type to a list and Engine
        :param filetype_ref: File format ref to delete from engine and list
        return None if OK
        """

        driver = self.get_by_ref(driver_ref)
        if driver is not None:
            if driver.delete() is None:
                return None
            else:
                return 1
        else:
            print_error("Driver type with id %s not found" % driver_ref)
            return 1
