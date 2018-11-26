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
# Author  : Edward de los Santos
# Author  : Marcin Przepiorowski
# Date    : Oct 2017


import logging
import requests
from packaging import version
from datetime import datetime, timedelta
#import pickle
from dxm.lib.DxEngine.DxConfig import DxConfig
from masking_apis.rest import ApiException
from masking_apis.configuration import Configuration
from masking_apis.api_client import ApiClient
from masking_apis.models.login import Login
from masking_apis.apis.login_api import LoginApi
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message
from masking_apis.apis.application_api import ApplicationApi
from masking_apis.apis.system_information_api import SystemInformationApi


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
    def __init__(self, name, address, username, password, port=8282,
                 protocol="http"):
        """
        Constructor
        :param address: Engine addess
        :param username: username
        :param password: password
        :param port: masking port (default 8282)
        :param protocol: connection protocol (default http)
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        """
        self.__address = address
        self.__name = name
        self.__username = username
        self.__password = password
        self.__port = port
        self.__protocol = protocol

        self.__logger = logging.getLogger()
        self.__logger.debug("creating DxMaskingEngine object")
        self.__logger.debug(("parameters: %s %s %s %s %s"
                            % (address, username,
                               password, port, protocol)))
        self.__base_url = self.__protocol + "://" + address + ":" \
            + str(self.__port) + "/masking/api"

        config = Configuration()
        config.host = self.__base_url
        config.debug = False

        if self.__logger.getEffectiveLevel() == logging.DEBUG:
            for name, logger in config.logger.items():
                logger.setLevel(logging.DEBUG)
                logger.removeHandler(config.logger_stream_handler)

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

        self.api_client = ApiClient()

        #set number of retries to one
        # set timeout on request level as it is overwritten anyway
        # to do
        # change all requests to add timeout
        self.api_client.rest_client.pool_manager.connection_pool_kw['retries'] = 0


        apikey = self.load()

        try:
            self.__logger.debug("Check if old session is valid")
            self.api_client.set_default_header(header_name='authorization',
                                               header_value=apikey)
            app = ApplicationApi(self.api_client)
            app.get_all_applications(_request_timeout=self.get_timeout())

        except ApiException as e:
            if e.status == 401:
                self.__logger.debug("Logging into Delphix Masking")
                login_api = LoginApi(self.api_client)
                login = Login(self.__username, self.__password)
                try:
                    self.__logger.debug("sending a login request. "
                                        "Payload %s" % login)
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
        try:
            si = SystemInformationApi(self.api_client)
            retobj = si.get_system_information()
            ret = retobj.version
        except ApiException:
            print "Old engine"
            ret = "5.2.0.0"

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
    def save(self, apikey):
        """
        Save session to file or database
        param1: apikey: Authorization key
        """
        # binary_file = open('engine.bin', mode='wb')
        # pickle.dump(apikey, binary_file)
        # binary_file.close()
        config = DxConfig()
        config.set_key(self.__name, None, apikey)



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

        config = DxConfig()
        auth_key = config.get_key(self.__name, None)
        return auth_key

    @classmethod
    def get_timeout(self):
        """
        Return timeout for query
        Tuple (connect_timeout, read_timeout)
        """
        return (5, 15)


    @classmethod
    def getlogs(self, outputlog):
        """
        Temporary procedure using GUI hack to download logs
        """

        base_url = self.__protocol + "://" + self.__address \
                   + ":" + str(self.__port)
        loginurl = base_url + '/dmsuite/login.do'
        logsurl = base_url + '/dmsuite/logsReport.do'
        dataurl = base_url + '/dmsuite/logsReport.do?action=download'

        session = requests.session()

        req_headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                    }

        formdata = {
                    'userName': self.__username,
                    'password': self.__password,
                   }

        # Authenticate
        session.post(
            loginurl, data=formdata, headers=req_headers,
            allow_redirects=False)
        session.get(logsurl)
        r2 = session.get(dataurl)

        try:
            outputlog.write(r2.text)
            outputlog.close()
            print_message("Log saved to file %s" % outputlog.name)
            return 0
        except Exception as e:
            print_error("Problem with file %s Error: %s" %
                       (outputlog.name, str(e)))
            return 1

            # if datafound:
            #     print line
