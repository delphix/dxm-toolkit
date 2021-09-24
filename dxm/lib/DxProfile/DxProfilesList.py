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
import sys
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxProfile.DxProfile import DxProfile
from dxm.lib.DxLogging import print_error
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.masking_api.api.profile_set_api import ProfileSetApi
from dxm.lib.masking_api.rest import ApiException

class DxProfilesList(object):

    __engine = None
    __profileset_list = {}
    __profileexp = None
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfilesList object")
        self.LoadProfiles()

    @classmethod
    def LoadProfiles(self):
        """
        Load list of profiles sets
        Return None if OK
        """

        self.__api = ProfileSetApi
        self.__apiexc = ApiException

        try:

            api_instance = self.__api(self.__engine.api_client)

            # execapi = ExecutionApi(self.__engine.api_client)
            # execList = paginator(
            #             execapi,
            #             "get_all_executions")
            #
            # if execList.response_list:
            #     for e in execList.response_list:
            #         self.__executionList[e.job_id] = e

            profileset = paginator(
                            api_instance,
                            "get_all_profile_sets",
                            _request_timeout=self.__engine.get_timeout())

            if profileset.response_list:
                for ps in profileset.response_list:
                    profile = DxProfile()
                    profile.from_profileset(ps)
                    self.__profileset_list[ps.profile_set_id] = profile
            else:
                print_error("No Profile sets found")
                self.__logger.error("No Profile sets found")

            self.__logger.debug("All Profile sets loaded")

        except self.__apiexc as e:
            print_error("Can't load Profile sets list %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a DxProfile object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__profileset_list[reference]

        except KeyError as e:
            self.__logger.debug("can't find profile object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__profileset_list.keys()

    @classmethod
    def get_profileSetId_by_name(self, name):
        """
        :param1 name: name of profile set
        return profile set id
        """
        reflist = get_objref_by_val_and_attribute(
                    name,
                    self,
                    'profile_set_name')

        if len(reflist) == 0:
            self.__logger.error('Profile set %s not found' % name)
            print_error('Profile set %s not found' % name)
            return None

        if len(reflist) > 1:
            self.__logger.error('Profile set name %s is not unique' % name)
            print_error('Profile set name %s is not unique' % name)
            return None

        return reflist[0]

    @classmethod
    def add(self, profile):
        """
        Add an profile to a list and Engine
        :param profile: Profile object to add to Engine and list
        return None if OK
        """

        if (profile.add() is None):
            self.__logger.debug("Adding profile %s to list" % profile)
            self.__profileset_list[profile.profile_set_id] = profile
            return None
        else:
            return 1

    @classmethod
    def delete(self, profile_set_id):
        """
        Delete a Profile from a list and Engine
        :param profile_set_id: profile id to delete from Engine and list
        return None if OK
        """

        profile = self.get_by_ref(profile_set_id)
        if profile is not None:
            if profile.delete() is None:
                return None
            else:
                return 1
        else:
            print_error("Profile with id %s not found" % profile_set_id)
            return 1
