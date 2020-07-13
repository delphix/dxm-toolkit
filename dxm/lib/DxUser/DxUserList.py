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
import sys
from dxm.lib.DxUser.DxUser import DxUser
from dxm.lib.DxTools.DxTools import get_objref_by_val_and_attribute
from dxm.lib.DxTools.DxTools import paginator
from dxm.lib.DxEngine.DxMaskingEngine import DxMaskingEngine
from dxm.lib.DxLogging import print_error


class DxUserList(object):

    # global list of roles on the class level
    __userList = {}
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
        self.__logger.debug("creating DxUserList object")
        self.LoadUsers()

    @classmethod
    def LoadUsers(self):
        """
        Load users list from Engine into global list
        return None if OK
        return 1 if error
        """

        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.api.user_api import UserApi
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.api.user_api import UserApi
            from masking_api_53.rest import ApiException

        self.__api = UserApi
        self.__apiexc = ApiException

        self.__userList.clear()
        try:
            api_instance = self.__api(self.__engine.api_client)
            userlist = paginator(
                        api_instance,
                        "get_all_users",
                        _request_timeout=self.__engine.get_timeout())

            if userlist.response_list:
                for c in userlist.response_list:
                    user = DxUser(self.__engine)
                    user.from_user(c)
                    self.__userList[c.user_id] = user
            else:
                self.__logger.error("No users found")
                print_error("No users found")

        except self.__apiexc as e:
            self.__logger.error("Can't load users %s" % e.body)
            print_error("Can't load users %s" % e.body)
            return 1

    @classmethod
    def get_by_ref(self, reference):
        """
        return a DxUser object by refrerence
        """
        try:
            self.__logger.debug("reference %s" % reference)
            return self.__userList[reference]

        except KeyError as e:
            self.__logger.debug("can't find user object"
                                " for reference %s" % reference)
            self.__logger.debug(e)
            sys.exit(1)

    @classmethod
    def get_allref(self):
        """
        return a list of all references
        """
        return self.__userList.keys()

    @classmethod
    def get_userId_by_name(self, name):
        """
        Return an user id for name
        :param name: User name
        return role_id if found
        return None if not found or not unique
        """
        users = get_objref_by_val_and_attribute(name, self,
                                                'user_name')
        if len(users) < 1:
            print_error("User %s not found" % name)
            self.__logger.error("User %s not found " % name)
            return None

        if len(users) > 1:
            print_error("User name %s is not unique" % name)
            self.__logger.error("User %s is not unique" % name)
            return None

        return users[0]

    @classmethod
    def add(self, user):
        """
        Add an user to a list and Engine
        :param user: User object to add to Engine and list
        return None if OK
        """

        if (user.add() is None):
            self.__logger.debug("Adding user %s to list" % user)
            self.__userList[user.user_id] = user
            return None
        else:
            return 1

    @classmethod
    def delete(self, user_id, force):
        """
        Delete an environment from a list and Engine
        :param user_id: User id to delete from Engine and list
        :param force: change user to non-admin and delete
        return None if OK
        """

        userobj = self.get_by_ref(user_id)
        if userobj is not None:
            if userobj.delete(force) == 0:
                return 0
            else:
                return 1
        else:
            print_error("User with id %s not found" % user_id)
            return 1
