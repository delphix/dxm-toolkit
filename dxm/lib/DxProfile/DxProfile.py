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
# Date    : September 2018


import logging
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxProfile.DxProfileExpList import DxProfileExpList
from masking_apis.models.profile_set import ProfileSet
from masking_apis.apis.profile_set_api import ProfileSetApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxProfile(ProfileSet):

    def __init__(self):
        """
        Constructor
        """
        ProfileSet.__init__(self)
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileSet object")

    def from_profileset(self, profile):
        """
        Copy properties from ProfileSet object into DxProfileSet
        :param con: ProfileSet object
        """
        self.__dict__.update(profile.__dict__)

    def set_expressions_using_names(self, expression_list):
        """
        Set an expression list using an expression names
        param1: expression_list: a list with expression names to set
        return 0 if all OK
        return 1 if expression not found
        """

        expression_ids_list = []
        profileexplist = DxProfileExpList()
        for expname in expression_list:
            peref = profileexplist.get_profileExpId_by_name(expname)
            if peref:
                expression_ids_list.append(peref)
            else:
                return 1

        self.profile_expression_ids = expression_ids_list
        return 0

    def add(self):
        """
        Add profile to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.profile_set_name is None):
            print_error("Profile name is required")
            self.__logger.error("Profile name is required")
            return 1

        if (self.profile_expression_ids is None):
            print_error("expression list is required")
            self.__logger.error("expression list is required")
            return 1

        try:
            self.__logger.debug("create profile input %s" % str(self))
            api_instance = ProfileSetApi(self.__engine.api_client)
            response = api_instance.create_profile_set(self)
            self.from_profileset(response)
            self.__logger.debug("profile response %s"
                                % str(response))
            print_message("Profile %s added" % self.profile_set_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete profile set from Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = ProfileSetApi(self.__engine.api_client)
            response = api_instance.delete_profile_set(
                self.profile_set_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("Profile response %s"
                                % str(response))
            print_message("Profile %s deleted" % self.profile_set_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update profile in Engine
        return a 0 if non error
        return 1 in case of error
        """

        try:
            api_instance = ProfileSetApi(self.__engine.api_client)
            self.__logger.debug("update profile request %s"
                                % str(self))
            response = api_instance.update_profile_set(
                self.profile_set_id,
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("update response %s"
                                % str(response))
            print_message("Profile %s updated" % self.profile_set_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
