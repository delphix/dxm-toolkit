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
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.profile_expression_api import ProfileExpressionApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel

class DxProfileExt(object):

    swagger_types = {
        'profile_expression_id': 'int',
        'domain_name': 'str',
        'expression_name': 'str',
        'regular_expression': 'str',
        'created_by': 'str',
        'data_level_profiling': 'bool'
    }

    swagger_map = {
        'profile_expression_id': 'profileExpressionId',
        'domain_name': 'domainName',
        'expression_name': 'expressionName',
        'regular_expression': 'regularExpression',
        'created_by': 'createdBy',
        'data_level_profiling': 'dataLevelProfiling'
    }

    def __init__(self):
        """
        Constructor
        """
        #ProfileExpression.__init__(self)
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileExt object")


        self.__api = ProfileExpressionApi
        self.__apiexc = ApiException
        self.__obj = None

    def from_profilesetext(self, profileext):
        self.__obj = profileext
        self.__obj.swagger_map = self.swagger_map
        self.__obj.swagger_types = self.swagger_types

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def profile_expression_id(self):
        if self.obj is not None:
            return self.obj.profile_expression_id
        else:
            return None

    @profile_expression_id.setter
    def profile_expression_id(self, profile_expression_id):
        if self.__obj is not None:
            self.__obj.profile_expression_id = profile_expression_id
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def expression_name(self):
        if self.obj is not None:
            return self.obj.expression_name
        else:
            return None

    @expression_name.setter
    def expression_name(self, expression_name):
        if self.__obj is not None:
            self.__obj.expression_name = expression_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def domain_name(self):
        if self.obj is not None:
            return self.obj.domain_name
        else:
            return None

    @domain_name.setter
    def domain_name(self, domain_name):
        if self.__obj is not None:
            self.__obj.domain_name = domain_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def regular_expression(self):
        if self.obj is not None:
            return self.obj.regular_expression
        else:
            return None

    @regular_expression.setter
    def regular_expression(self, regular_expression):
        if self.__obj is not None:
            self.__obj.regular_expression = regular_expression
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def data_level_profiling(self):
        if self.obj is not None:
            return self.obj.data_level_profiling
        else:
            return None

    @data_level_profiling.setter
    def data_level_profiling(self, data_level_profiling):
        if self.__obj is not None:
            self.__obj.data_level_profiling = data_level_profiling
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def created_by(self):
        if self.obj is not None:
            return self.obj.created_by
        else:
            return None


    def create_profile_expression(self, domain_name, expression_name, regular_expression,  data_level_profiling):

        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.obj.domain_name = domain_name
        self.obj.expression_name = expression_name
        self.obj.regular_expression = regular_expression
        self.obj.data_level_profiling = data_level_profiling


    def add(self):
        """
        Add expression to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if (self.expression_name is None):
            print_error("Expression name is required")
            self.__logger.error("Expression name is required")
            return 1

        if (self.domain_name is None):
            print_error("Domain name is required")
            self.__logger.error("Domain name is required")
            return 1

        if (self.regular_expression is None):
            print_error("Regular expression is required")
            self.__logger.error("Domain name is required")
            return 1

        try:
            self.__logger.debug("create expression input %s" % str(self))
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_profile_expression(self.obj)
            self.from_profilesetext(response)

            self.__logger.debug("expression response %s"
                                % str(response))

            print_message("Expression %s added" % self.expression_name)
            return None
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete expression from Engine
        return a None if non error
        return 1 in case of error
        """

        try:
            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.delete_profile_expression(
                self.profile_expression_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("expression response %s"
                                % str(response))
            print_message("Expression %s deleted" % self.expression_name)
            return None
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update expression in Engine
        return None if non error
        return 1 in case of error
        """

        try:
            api_instance = self.__api(self.__engine.api_client)
            self.__logger.debug("update expression request %s"
                                % str(self))
            response = api_instance.update_profile_expression(
                self.profile_expression_id,
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("expression response %s"
                                % str(response))
            print_message("Expression %s updated" % self.expression_name)
            return None
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
