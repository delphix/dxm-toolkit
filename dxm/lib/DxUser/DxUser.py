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
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from dxm.lib.masking_api.api.user_api import UserApi
from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.genericmodel import GenericModel


def DxUserNonAdmin(role_id, environment_ids):
    swagger_map = {
        'role_id': 'roleId',
        'environment_ids': 'environmentIds'
    }

    swagger_types = {
        'role_id': 'int',
        'environment_ids': 'list'
    }


    obj = GenericModel({ x:None for x in swagger_map.values()}, swagger_types, swagger_map)
    obj.role_id = role_id
    obj.environment_ids = environment_ids
    return obj


class DxUser(object):

    swagger_map = {
        'user_id': 'userId',
        'user_name': 'userName',
        'password': 'password',
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email': 'email',
        'is_admin': 'isAdmin',
        'show_welcome': 'showWelcome',
        'is_locked': 'isLocked',
        'non_admin_properties': 'nonAdminProperties',
        'api_access': 'apiAccess',
        'user_status': 'userStatus'
    }

    swagger_types = {
        'user_id': 'int',
        'user_name': 'str',
        'password': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'is_admin': 'bool',
        'show_welcome': 'bool',
        'is_locked': 'bool',
        'non_admin_properties': 'dict1',
        'api_access': 'bool',
        'user_status': 'str'
    }

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        #User.__init__(self)
        self.__logger = logging.getLogger()
        self.__engine = engine
        # if (self.__engine.version_ge('6.0.0')):
        #     from masking_api_60.models.user import User
        #     from masking_api_60.models.non_admin_properties import NonAdminProperties
        #     from masking_api_60.api.user_api import UserApi
        #     from masking_api_60.rest import ApiException
        # else:
        #     from masking_api_53.models.user import User
        #     from masking_api_53.models.non_admin_properties import NonAdminProperties
        #     from masking_api_53.api.user_api import UserApi
        #     from masking_api_53.rest import ApiException

        self.__api = UserApi
        # self.__model = User
        # self.__modelnap = NonAdminProperties
        self.__apiexc = ApiException
        self.__obj = None

    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None


    @property
    def user_id(self):
        if self.obj is not None:
            return self.obj.user_id
        else:
            return None

    @user_id.setter
    def user_id(self, user_id):
        if self.__obj is not None:
            self.__obj.user_id = user_id
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def user_id(self):
        if self.obj is not None:
            return self.obj.user_id
        else:
            return None

    @user_id.setter
    def user_id(self, user_id):
        if self.__obj is not None:
            self.__obj.user_id = user_id
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def user_name(self):
        if self.obj is not None:
            return self.obj.user_name
        else:
            return None

    @user_name.setter
    def user_name(self, user_name):
        if self.__obj is not None:
            print("W sweterze 2")
            self.__obj.user_name = user_name
        else:
            raise ValueError("Object needs to be initialized first")

            

    @property
    def password(self):
        if self.obj is not None:
            return 'xxxxxxxxx'
        else:
            return None

    @password.setter
    def password(self, password):
        if self.__obj is not None:
            self.__obj.password = password
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def first_name(self):
        if self.obj is not None:
            return self.obj.first_name
        else:
            return None

    @first_name.setter
    def first_name(self, first_name):
        if self.__obj is not None:
            self.__obj.first_name = first_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def last_name(self):
        if self.obj is not None:
            return self.obj.last_name
        else:
            return None

    @last_name.setter
    def last_name(self, last_name):
        if self.__obj is not None:
            self.__obj.last_name = last_name
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def email(self):
        if self.obj is not None:
            return self.obj.email
        else:
            return None

    @email.setter
    def email(self, email):
        if self.__obj is not None:
            self.__obj.email = email
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def is_admin(self):
        if self.obj is not None:
            return self.obj.is_admin
        else:
            return None

    @is_admin.setter
    def is_admin(self, is_admin):
        if self.__obj is not None:
            self.__obj.is_admin = is_admin
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def show_welcome(self):
        if self.obj is not None:
            return self.obj.show_welcome
        else:
            return None

    @show_welcome.setter
    def show_welcome(self, show_welcome):
        if self.__obj is not None:
            self.__obj.show_welcome = show_welcome
        else:
            raise ValueError("Object needs to be initialized first")

    @property
    def is_locked(self):
        if self.obj is not None:
            if hasattr(self.obj,"is_locked"):
                return self.obj.is_locked
            elif hasattr(self.obj,"user_status"):
                if self.obj.user_status == 'ACTIVE':
                    return False
                else:
                    return True
            else:
                raise ValueError("is_locked not implemented / API change")
        else:
            return None

    @is_locked.setter
    def is_locked(self, is_locked):

        if self.__engine.version_le("6.0.6.0"):
            if self.__obj is not None:
                self.__obj.is_locked = is_locked
            else:
                raise ValueError("Object needs to be initialized first")
        else:
            if is_locked == True:
                status = "LOCKED"
            else:
                status = "ACTIVE"
            if self.__obj is not None:
                self.__obj.user_status = status
            else:
                raise ValueError("Object needs to be initialized first") 


    @property
    def non_admin_properties(self):
        if self.obj is not None:
            if hasattr(self.obj, 'non_admin_properties'):
                return self.obj.non_admin_properties
            else:
                return None
        else:
            return None

    @non_admin_properties.setter
    def non_admin_properties(self, non_admin_properties):
        if self.__obj is not None:
            self.__obj.non_admin_properties = non_admin_properties
        else:
            raise ValueError("Object needs to be initialized first")

    def from_user(self, user):
        self.__obj = user
        self.__obj.swagger_map = self.swagger_map
        self.__obj.swagger_types = self.swagger_types

        if hasattr(self.__obj,'non_admin_properties') and self.__obj.non_admin_properties is not None:
            self.__obj.non_admin_properties.swagger_map =  {
                                                                'role_id': 'roleId',
                                                                'environment_ids': 'environmentIds'
                                                            }
            self.__obj.non_admin_properties.swagger_types = {
                                                                'role_id': 'int',
                                                                'environment_ids': 'list'
                                                            }


    def create_user(self, user_name, password, first_name, last_name, email, is_admin, non_admin_properties):
        # self.__obj = self.__model(user_name=user_name, password=password, first_name=first_name, last_name=last_name, 
        #                          email=email, is_admin=is_admin, non_admin_properties=non_admin_properties, is_locked=False)



        self.__obj = GenericModel({ x:None for x in self.swagger_map.values()}, self.swagger_types, self.swagger_map)
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.is_locked=False
        self.non_admin_properties = non_admin_properties


    def delete_nap(self):
        """
        Delete NonAdminProperties
        """
        self.obj._non_admin_properties = None

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


        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("create user input %s" % str(self))
            response = api_instance.create_user(
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("create user response %s"
                                % str(response))

            self.user_id = response.user_id
            print_message("User %s added" % self.user_name)
            return 0
        except self.__apiexc as e:
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
            nap = self.__modelnap(environment_ids=[], role_id=1)
            self.non_admin_properties = nap
            if self.update() != 0:
                print_error("Can't switch to non-admin in force mode")
                self.__logger.debug("Can't switch to non-admin in force mode")
                return 1

        api_instance = self.__api(self.__engine.api_client)

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
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update user on Masking engine and print status message
        return 0 if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("update user id %s"
                                % self.user_id)

            response = api_instance.update_user_by_id(
                self.user_id,
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("update user response %s"
                                % str(response))
            print_message("User %s updated" % self.user_name)
            return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1
