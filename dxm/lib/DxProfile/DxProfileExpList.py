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
from dxm.lib.DxProfile.DxProfileExt import DxProfileExt
from dxm.lib.DxLogging import print_error
from dxm.lib.DxTools.DxTools import paginator


class DxProfileExpList(object):

    __engine = None
    __profileexp_list = {}
    __logger = None

    @classmethod
    def __init__(self):
        """
        Constructor
        """
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileExpList object")
        self.LoadProfileExt()

    @classmethod
    def LoadProfileExt(self):
        """
        Load list of profiles expressions
        Return None if OK
        """

        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.api.profile_expression_api import ProfileExpressionApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.api.profile_expression_api import ProfileExpressionApi
            from masking_api_53.rest import ApiException

        self.__api = ProfileExpressionApi
        self.__apiexc = ApiException

        try:

            api_instance = self.__api(self.__engine.api_client)
            profileexts = paginator(
                            api_instance,
                            "get_all_profile_expressions",
                            _request_timeout=self.__engine.get_timeout())

            if profileexts.response_list:
                for pe in profileexts.response_list:
                    proext = DxProfileExt()
                    proext.from_profilesetext(pe)
                    self.__profileexp_list[pe.profile_expression_id] = proext
            else:
                print_error("No Profile expression found")
                self.__logger.error("No Profile expression found")

            self.__logger.debug("All Profile expression loaded")

        except self.__apiexc as e:
            print_error("Can't load Profile expression list %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a DxProfileExt object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__profileexp_list[reference]

        except KeyError as e:
            self.__logger.debug("can't find profile expression object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__profileexp_list.keys()

    @classmethod
    def get_profileExpId_by_name(self, name):
        """
        :param1 name: name of profile expression set
        return profile expression id
        """
        reflist = get_objref_by_val_and_attribute(
                    name,
                    self,
                    'expression_name')
        if len(reflist) == 0:
            self.__logger.error('Profile expression %s not found' % name)
            print_error('Profile expression %s not found' % name)
            return None

        if len(reflist) > 1:
            self.__logger.error(
                'Profile expression name %s is not unique' % name)
            print_error(
                'Profile expression name %s is not unique' % name)
            return None

        return reflist[0]

    @classmethod
    def add(self, exp):
        """
        Add an Expression to a list and Engine
        :param exp: Expression object to add to Engine and list
        return None if OK
        """

        if (exp.add() is None):
            self.__logger.debug("Adding expression %s to list" % exp)
            self.__profileexp_list[exp.profile_expression_id] = exp
            return None
        else:
            return 1

    @classmethod
    def delete(self, profile_expression_id):
        """
        Delete a job from a list and Engine
        :param masking_job_id: masking job id to delete from Engine and list
        return None if OK
        """

        exp = self.get_by_ref(profile_expression_id)

        if exp is not None:
            if exp.delete() is None:
                return None
            else:
                return 1
        else:
            print_error("Expression with id %s not found" % profile_expression_id)
            return 1
