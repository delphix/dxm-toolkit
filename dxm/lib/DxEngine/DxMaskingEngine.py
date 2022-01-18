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
# Date    : Oct 2017


import logging
import requests
import sys
import re
import urllib3
import ssl
import certifi
from packaging import version
from datetime import datetime, timedelta
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

import os

import json

import six
from urllib3 import make_headers, ProxyManager, PoolManager

#import pickle
from dxm.lib.DxEngine.DxConfig import DxConfig

from dxm.lib.masking_api.rest import ApiException
from dxm.lib.masking_api.configuration import Configuration
from dxm.lib.masking_api.api_client import ApiClient
from dxm.lib.masking_api.api.login_api import LoginApi
from dxm.lib.masking_api.api.application_api import ApplicationApi
from dxm.lib.masking_api.api.system_information_api import SystemInformationApi
from dxm.lib.masking_api.api.logging_api import LoggingApi
from dxm.lib.masking_api.api.file_download_api import FileDownloadApi


class DxMaskingEngine(object):

    api_client = None
    __address = None
    __name = None
    __username = None
    __password = None
    __port = None
    __protocol = None
    __logger = None

    @classmethod
    def __init__(self, engine_tuple):
        """
        Constructor
        :param address: Engine addess
        :param username: username
        :param password: password
        :param port: masking port (default 8282)
        :param protocol: connection protocol (default http)
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        tuple:
        engine_name,ip_address,username,password, protocol,port, defengine, auth_id
        """

        self.__address = engine_tuple[1]
        self.__name = engine_tuple[0]
        self.__username = engine_tuple[2]
        self.__password = engine_tuple[3]
        self.__port = engine_tuple[5]
        self.__protocol = engine_tuple[4]
        self.__version = None

        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxMaskingEngine object")
        self.__logger.debug(("parameters: %s %s %s %s %s"
                            % (self.__address, self.__username,
                               self.__password, self.__port, self.__protocol)))
        self.__base_url = self.__protocol + "://" + self.__address + ":" \
            + str(self.__port) + "/masking/api"

        self.config = Configuration()
        self.config.host = self.__base_url
        self.config.debug = False
        self.config.client_side_validation = False

        if engine_tuple[8]:
            #proxy settings
            dxconfig = DxConfig
            self.config.proxy = engine_tuple[8]
            if engine_tuple[9]:
                self.config.proxyuser = engine_tuple[9]
                self.config.proxypass = dxconfig.get_proxy_password(engine_tuple[9])
            else:
                self.config.proxyuser = None
                self.config.proxypass = None


        # to disable certs
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.config.verify_ssl = False

        if self.__logger.getEffectiveLevel() == logging.DEBUG:
            for name, logger in self.config.logger.items():
                logger.setLevel(logging.DEBUG)
                logger.removeHandler(self.config.logger_stream_handler)



    @classmethod
    def get_config(self):
        return self.config


    @classmethod
    def get_username(self):
        return self.__username

    @classmethod
    def get_name(self):
        return self.__name


    @classmethod
    def get_session(self):
        """
        Create a session with a Masking engine
        :return autorization key for a session
        """

        self.api_client = ApiClient(self.config)
        #set number of retries to one
        # set timeout on request level as it is overwritten anyway
        # to do
        # change all requests to add timeout
        self.api_client.rest_client.pool_manager.connection_pool_kw['retries'] = 0
        apikey = self.load()

        try:
            self.__logger.debug("Check if old session is valid")
            if apikey is not None:
                self.api_client.set_default_header(header_name='authorization',
                                                   header_value=apikey)
            app = ApplicationApi(self.api_client)
            app.get_all_applications(_request_timeout=self.get_timeout())

        except ApiException as e:
            if e.status == 401:
                password = DxConfig.decrypt_password(self.__password)
                if password is None:
                    print_error("Problem with password decryption. Can't connect to engine")
                    return 1
                self.__logger.debug("Logging into Delphix Masking")
                login_api = LoginApi(self.api_client)
                login = { 
                    "username": self.__username, 
                    "password": password
                }
                try:
                    self.__logger.debug("sending a login request. "
                                        "Username {}".format(self.__username))
                    login_response = login_api.login(
                        login,
                        _request_timeout=self.get_timeout())
                    self.__logger.debug("login response %s"
                                        % login_response)
                    self.api_client.set_default_header(
                                header_name='authorization',
                                header_value=login_response.authorization
                    )
                    self.save(login_response.authorization)
                    return None
                except ApiException as e:
                    print_error("Can't login to engine %s (IP: %s)"
                                % (self.__name, self.__address))
                    print_error(e.body)
                    return 1
            else:
                print_error("Something went wrong %s" % e)
                self.__logger.error("Something went wrong %s" % e)
                return 1

        except Exception as e:
            # if engine is down this one should kick off
            print_error("Can't login to engine %s (IP: %s)"
                        % (self.__name, self.__address))
            self.__logger.debug(str(e))
            return 1

    @classmethod
    def get_version(self):
        """
        Return version of engine
        return: version of engine as string. ex 5.3.0.0 or 5.2.0.0
        """

        if self.__version is not None:
            return self.__version

        try:
            si = SystemInformationApi(self.api_client)
            retobj = si.get_system_information()
            ret = retobj.version
        except ApiException:
            ret = "5.2.0.0"

        self.__version = ret
        return ret

    @classmethod
    def version_ge(self, version_engine):
        """
        Compare an input parameter with engine version.
        param1: version_engine: version number to compare ex. "5.3"
        return: True if engine has higher or equal version
        """
        engine_ver = self.get_version()
        return version.parse(engine_ver) >= version.parse(version_engine)

    @classmethod
    def version_le(self, version_engine):
        """
        Compare an input parameter with engine version.
        param1: version_engine: version number to compare ex. "5.3"
        return: True if engine has higher or equal version
        """
        engine_ver = self.get_version()
        return version.parse(engine_ver) <= version.parse(version_engine)

    @classmethod
    def save(self, apikey):
        """
        Save session to file or database
        param1: apikey: Authorization key
        """
        # binary_file = open('engine.bin', mode='wb')
        # pickle.dump(apikey, binary_file)
        # binary_file.close()
        config = DxConfig
        config.set_key(self.__name, self.__username, apikey)



    @classmethod
    def load(self):
        """
        Load session from file or database
        """
        # try:
        #     binary_file = open('engine.bin', mode='rb')
        #     apikey = pickle.load(binary_file)
        #     binary_file.close()
        #     return apikey
        # except IOError:
        #     print_error("Session file not found")
        #     self.__logger.error("Session file not found")

        config = DxConfig
        auth_key = config.get_key(self.__name, self.__username)
        return auth_key

    @classmethod
    def get_timeout(self):
        """
        Return timeout for query
        Tuple (connect_timeout, read_timeout)
        """
        return (5, 15)

    @classmethod
    def getlogs(self, outputlog,page_size,level):
        """
        Get engine logs via API
        """

        file = outputlog.name
        outputlog.write(" ")
        outputlog.close()

        try:
            si = LoggingApi(self.api_client)
            arr = si.get_all_logs(page_size=page_size, log_level=level)
        except ApiException as e:
            print_error("Problem with LoggingAPI %s Error: %s" % (outputlog.name, str(e)))
            return 1

        loglist = arr.response_list
        loglist.reverse()

        self.__logger.debug("List of log files")
        self.__logger.debug(loglist)

        for l in loglist:
            try:
                data = FileDownloadApi(self.api_client)
                data_file = data.download_file(l.file_download_id)
            except ApiException as e:
                print_error("Problem with FileDownloadApi %s Error: %s" % (outputlog.name, str(e)))
                return 1

            try:
                outputlog = open(file,"a")
                outputlog.write(data_file)
                outputlog.close()
            except Exception as e:
                print_error("Failed to write file %s because error: %s" % (outputlog.name, str(e)))
                return 1

        print_message("Log saved to file %s" % outputlog.name)
        return 0

