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
from masking_apis.models.profile_expression import ProfileExpression
from masking_apis.apis.profile_expression_api import ProfileExpressionApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxProfileExt(ProfileExpression):

    def __init__(self):
        """
        Constructor
        """
        ProfileExpression.__init__(self)
        self.__engine = DxMaskingEngine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxProfileExt object")

    def from_profilesetext(self, profileext):
        """
        Copy properties from ProfileExpression object into DxProfileExt
        :param profileext: ProfileExpression object
        """
        self.__dict__.update(profileext.__dict__)

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
            api_instance = ProfileExpressionApi(self.__engine.api_client)
            response = api_instance.create_profile_expression(self)
            self.from_profilesetext(response)

            self.__logger.debug("expression response %s"
                                % str(response))

            print_message("Expression %s added" % self.expression_name)
            return None
        except ApiException as e:
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
            api_instance = ProfileExpressionApi(self.__engine.api_client)
            response = api_instance.delete_profile_expression(
                self.profile_expression_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("expression response %s"
                                % str(response))
            print_message("Expression %s deleted" % self.expression_name)
            return None
        except ApiException as e:
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
            api_instance = ProfileExpressionApi(self.__engine.api_client)
            self.__logger.debug("update expression request %s"
                                % str(self))
            response = api_instance.update_profile_expression(
                self.profile_expression_id,
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("expression response %s"
                                % str(response))
            print_message("Expression %s updated" % self.expression_name)
            return None
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
