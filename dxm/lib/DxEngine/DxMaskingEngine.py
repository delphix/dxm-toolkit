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
from packaging import version
from datetime import datetime, timedelta
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message

import os
import urllib3
import ssl
import certifi
from urllib3 import make_headers, ProxyManager, PoolManager

#import pickle
from dxm.lib.DxEngine.DxConfig import DxConfig
try:
    from masking_api_60.rest import ApiException
    from masking_api_60.configuration import Configuration
    from masking_api_60.api_client import ApiClient
    from masking_api_60.models.login import Login
    from masking_api_60.api.login_api import LoginApi
    from masking_api_60.api.application_api import ApplicationApi
    from masking_api_60.api.system_information_api import SystemInformationApi
    from masking_api_60.api.logging_api import LoggingApi
    from masking_api_60.api.file_download_api import FileDownloadApi

    class DxApiClient(ApiClient):

        def __init__(self, configuration=None, header_name=None, header_value=None,
                    cookie=None):

            super(DxApiClient, self).__init__(configuration=configuration, header_name=header_name, header_value=header_value,
                                            cookie=cookie)


            if configuration.verify_ssl:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE

            # ca_certs
            if configuration.ssl_ca_cert:
                ca_certs = configuration.ssl_ca_cert
            else:
                # if not set certificate file, use Mozilla's root certificates.
                ca_certs = certifi.where()

            addition_pool_args = {}
            if configuration.assert_hostname is not None:
                addition_pool_args['assert_hostname'] = configuration.assert_hostname  # noqa: E501

            maxsize = 4
            if maxsize is None:
                if configuration.connection_pool_maxsize is not None:
                    maxsize = configuration.connection_pool_maxsize
                else:
                    maxsize = 4

            # https pool manager
            if configuration.proxy:
                if configuration.proxyuser:
                    default_headers = make_headers(proxy_basic_auth='{}:{}'.format(configuration.proxyuser, configuration.proxypass))
                else:
                    default_headers = make_headers()
                self.rest_client.pool_manager = urllib3.ProxyManager(
                    num_pools=4,
                    maxsize=maxsize,
                    cert_reqs=cert_reqs,
                    ca_certs=ca_certs,
                    cert_file=configuration.cert_file,
                    key_file=configuration.key_file,
                    proxy_url=configuration.proxy,
                    proxy_headers = default_headers,
                    **addition_pool_args
                )
            else:
                self.rest_client.pool_manager = urllib3.PoolManager(
                    num_pools=4,
                    maxsize=maxsize,
                    cert_reqs=cert_reqs,
                    ca_certs=ca_certs,
                    cert_file=configuration.cert_file,
                    key_file=configuration.key_file,
                    **addition_pool_args
                )

        def _ApiClient__deserialize_file(self, response):
            """Deserializes body to file

            Return a body of request

            :param response:  RESTResponse.
            :return: file path.
            """

            return response.data


        def request(self, method, url, query_params=None, headers=None,
                post_params=None, body=None, _preload_content=True,
                _request_timeout=None):
            
            if logging.getLogger('debugfile').getEffectiveLevel() == 9:
                logging_file("SAVE TO FILE {} {} {}".format(url, query_params, body))
            response = super(DxApiClient, self).request(method, url, query_params, headers,
                                            post_params, body, _preload_content,
                                            _request_timeout)

            if logging.getLogger('debugfile').getEffectiveLevel() == 9:
                logging_file("SAVE TO FILE {} {} {}".format(response.status, response.reason, response.data))
            return response


except ModuleNotFoundError:
    try:
        from masking_api_53.rest import ApiException 
        from masking_api_53.configuration import Configuration
        from masking_api_53.api_client import ApiClient
        from masking_api_53.models.login import Login
        from masking_api_53.api.login_api import LoginApi
        from masking_api_53.api.application_api import ApplicationApi
        from masking_api_53.api.system_information_api import SystemInformationApi
        from masking_api_53.api.logging_api import LoggingApi
        from masking_api_53.api.file_download_api import FileDownloadApi
    except ModuleNotFoundError:
        print_error("You need to have at least one Masking API installed.")
        sys.exit(1)    







def logging_file(message):
    pass


try:

    from masking_api_53.api_client import ApiClient as ApiClient5

    class DxApiClient5(ApiClient5):

        def __init__(self, configuration=None, header_name=None, header_value=None,
                    cookie=None):

            super(DxApiClient5, self).__init__(configuration=configuration, header_name=header_name, header_value=header_value,
                                            cookie=cookie)


            if configuration.verify_ssl:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE

            # ca_certs
            if configuration.ssl_ca_cert:
                ca_certs = configuration.ssl_ca_cert
            else:
                # if not set certificate file, use Mozilla's root certificates.
                ca_certs = certifi.where()

            addition_pool_args = {}
            if configuration.assert_hostname is not None:
                addition_pool_args['assert_hostname'] = configuration.assert_hostname  # noqa: E501

            maxsize = 4
            if maxsize is None:
                if configuration.connection_pool_maxsize is not None:
                    maxsize = configuration.connection_pool_maxsize
                else:
                    maxsize = 4

            # https pool manager
            if configuration.proxy:
                if configuration.proxyuser:
                    default_headers = make_headers(proxy_basic_auth='{}:{}'.format(configuration.proxyuser, configuration.proxypass))
                else:
                    default_headers = make_headers()
                self.rest_client.pool_manager = urllib3.ProxyManager(
                    num_pools=4,
                    maxsize=maxsize,
                    cert_reqs=cert_reqs,
                    ca_certs=ca_certs,
                    cert_file=configuration.cert_file,
                    key_file=configuration.key_file,
                    proxy_url=configuration.proxy,
                    proxy_headers = default_headers,
                    **addition_pool_args
                )
            else:
                self.rest_client.pool_manager = urllib3.PoolManager(
                    num_pools=4,
                    maxsize=maxsize,
                    cert_reqs=cert_reqs,
                    ca_certs=ca_certs,
                    cert_file=configuration.cert_file,
                    key_file=configuration.key_file,
                    **addition_pool_args
                )

        def _ApiClient__deserialize_file(self, response):
            """Deserializes body to file

            Return a body of request

            :param response:  RESTResponse.
            :return: file path.
            """

            return response.data



        def request(self, method, url, query_params=None, headers=None,
                post_params=None, body=None, _preload_content=True,
                _request_timeout=None):
            
            if logging.getLogger().getEffectiveLevel() == 9:
                logging_file("SAVE TO FILE 5 {} {} {}".format(url, query_params, body))
            response = super(DxApiClient5, self).request(method, url, query_params, headers,
                                            post_params, body, _preload_content,
                                            _request_timeout)

            if logging.getLogger().getEffectiveLevel() == 9:
                logging_file("SAVE TO FILE 5 {} {} {}".format(response.status, response.reason, response.data))
            return response

except ModuleNotFoundError:
    pass

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

        if engine_tuple[8]:
            #proxy settings
            dxconfig = DxConfig()
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

        if "masking_api_53.api" in sys.modules.keys():
            is_api5 = True
            version = 5
        else:
            is_api5 = False

        if "masking_api_60.api" in sys.modules.keys():
            is_api6 = True
            version = 6
        else:
            is_api6 = False

        self.get_session_worker(version=version)
        if self.get_version()<"6.0.0.0":
            if is_api5:    
                self.__logger.debug("Change API from 6 to 5") 
                self.get_session_worker(version=5) 
            else:
                print_error("Delphix Engine version is not supported by compiled API. Please generate SDK with proper version")
                sys.exit(1)

        if self.get_version()>="6.0.0.0" and is_api6 == False:
            print_error("Delphix Engine version is not supported by compiled API. Please generate SDK with proper version")
            sys.exit(1)         
        



    @classmethod
    def get_session_worker(self, version):
        """
        Create a session with a Masking engine
        :return autorization key for a session
        """

        if version==5:
            self.api_client = DxApiClient5(self.config)
        else:
            try:
                self.api_client = DxApiClient(self.config)
            except NameError:
                self.__logger.debug("No 6 libs, failing back to 5") 
                self.api_client = DxApiClient5(self.config)


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
                password = DxConfig().decrypt_password(self.__password)
                if password is None:
                    print_error("Problem with password decryption. Can't connect to engine")
                    return 1
                self.__logger.debug("Logging into Delphix Masking")
                login_api = LoginApi(self.api_client)
                login = Login(self.__username, password)
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
        return (5, 60)
        """    enginelist = get_list_of_engines(p_engine)

    if enginelist is None:
        return 1

    data = DataFormatter()
    data_header = [
                    ("Engine name", 30),
                    ("Application name", 30),
                  ]
    data.create_header(data_header)
    data.format_type = format
    for engine_tuple in enginelist:
        engine_obj = DxMaskingEngine(engine_tuple)
        if engine_obj.get_session():
            continue
        applist = DxApplicationList()
        # load all objects
        applist.LoadApplications()
      """
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

        print(loglist)

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

