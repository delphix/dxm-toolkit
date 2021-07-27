import urllib3
import ssl
import certifi
from urllib3 import make_headers, ProxyManager, PoolManager
import logging



try:

    from masking_api_53.api_client import ApiClient as ApiClient5
    from masking_api_53.configuration import Configuration

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





class ClientFactory(object):

    def __init__(self, version, engine, config):
        self.__version = version
        self.__engine = engine
        self.__config = config

    def getapi(self):


        print("VERSION {}".format(self.__version))



        if (self.__engine.version_le(self.__version)):
            from masking_api_53.api_client import ApiClient as ApiClient5
            from masking_api_53.configuration import Configuration

        elif (self.__engine.version_le(self.__version)):
            print("SLON")
            from masking_api_v514.api_client import ApiClient as ApiClient5
            from masking_api_v514.configuration import Configuration
        else:
            print("KROWA")
            from dxm.lib.masking_api.api_client import ApiClient as ApiClient5
            from dxm.lib.masking_api.configuration import Configuration

        return DxApiClient(self.__config)


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


 


        







