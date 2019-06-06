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
# Copyright (c) 2019 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : May 2019


import logging
from masking_apis.models.user import User
from masking_apis.models.non_admin_properties import NonAdminProperties
from masking_apis.apis.user_api import UserApi
from masking_apis.rest import ApiException
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxUser(User):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        User.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine

    def from_user(self, user):
        """
        Copy properties from User object into DxUser
        :param role: User object
        """
        self.__dict__.update(user.__dict__)

    def delete_nap(self):
        """
        Delete NonAdminProperties
        """
        self._non_admin_properties = None

    def add(self):
        """
        Add user to Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        if self.user_name is None:
            print_error("User name is required")
            self.__logger.error("User name is required")
            return 1

        if self.first_name is None:
            print_error("User first name is required")
            self.__logger.error("User first name is required")
            return 1

        if self.last_name is None:
            print_error("User last name is required")
            self.__logger.error("User last name is required")
            return 1

        if self.email is None:
            print_error("User email is required")
            self.__logger.error("User email is required")
            return 1

        if self.is_admin is None:
            print_error("User type (admin/non-admin) is required")
            self.__logger.error("User type (admin/non-admin) is required")
            return 1

        if not self.is_admin and self.non_admin_properties is None:
            print_error("Non admin user requires a non admin properties")
            self.__logger.error("Non admin user requires a non admin properties")
            return 1

        if self.password is None:
            print_error("User password is required")
            self.__logger.error("User password is required")
            return 1

        if self.is_locked is None:
            self.__logger.error("Setting is_locked to false")
            self.is_locked = False

        if self.show_welcome is None:
            self.__logger.error("Setting show_welcome to false")
            self.show_welcome = False

        api_instance = UserApi(self.__engine.api_client)

        try:
            self.__logger.debug("create user input %s" % str(self))
            response = api_instance.create_user(
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create user response %s"
                                % str(response))

            self.user_id = response.user_id
            print_message("User %s added" % self.user_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self, force):
        """
        Delete user from Masking engine and print status message
        :param force: if True, change user to non-admin and delete
        return a None if non error
        return 1 in case of error
        """

        if self.is_admin and force:
            self.is_admin = False
            nap = NonAdminProperties()
            nap.environment_ids = []
            nap.role_id = 1
            self.non_admin_properties = nap
            if self.update() is not None:
                print_error("Can't switch to non-admin in force mode")
                self.__logger.debug("Can't switch to non-admin in force mode")
                return 1

        api_instance = UserApi(self.__engine.api_client)

        try:
            self.__logger.debug("delete user id %s"
                                % self.user_id)
            response = api_instance.delete_user_by_id(
                self.user_id,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete user response %s"
                                % str(response))
            print_message("User %s deleted" % self.user_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update user on Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        api_instance = UserApi(self.__engine.api_client)

        try:
            self.__logger.debug("update user id %s"
                                % self.user_id)
            response = api_instance.update_user_by_id(
                self.user_id,
                self,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("update user response %s"
                                % str(response))
            print_message("User %s updated" % self.user_name)
            return 0
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
