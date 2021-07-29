# coding: utf-8

"""
    Masking API

    Schema for the Masking Engine API  # noqa: E501

    OpenAPI spec version: 5.1.8
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from dxm.lib.masking_api.api_client import ApiClient


class SshKeyApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_ssh_key(self, ssh_key, **kwargs):  # noqa: E501
        """Create SSH key  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_ssh_key(ssh_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file ssh_key: The SSH key to be uploaded. The logical name of the SSH key will be exactly the name of this uploaded file (required)
        :return: SshKey
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_ssh_key_with_http_info(ssh_key, **kwargs)  # noqa: E501
        else:
            (data) = self.create_ssh_key_with_http_info(ssh_key, **kwargs)  # noqa: E501
            return data

    def create_ssh_key_with_http_info(self, ssh_key, **kwargs):  # noqa: E501
        """Create SSH key  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_ssh_key_with_http_info(ssh_key, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file ssh_key: The SSH key to be uploaded. The logical name of the SSH key will be exactly the name of this uploaded file (required)
        :return: SshKey
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ssh_key']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_ssh_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ssh_key' is set
        if self.api_client.client_side_validation and ('ssh_key' not in params or
                                                       params['ssh_key'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `ssh_key` when calling `create_ssh_key`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'ssh_key' in params:
            local_var_files['sshKey'] = params['ssh_key']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/ssh-keys', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SshKey',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_ssh_key(self, ssh_key_name, **kwargs):  # noqa: E501
        """Delete SSH key by name  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_ssh_key(ssh_key_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ssh_key_name: The name of the SSH key to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_ssh_key_with_http_info(ssh_key_name, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_ssh_key_with_http_info(ssh_key_name, **kwargs)  # noqa: E501
            return data

    def delete_ssh_key_with_http_info(self, ssh_key_name, **kwargs):  # noqa: E501
        """Delete SSH key by name  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_ssh_key_with_http_info(ssh_key_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str ssh_key_name: The name of the SSH key to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ssh_key_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_ssh_key" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'ssh_key_name' is set
        if self.api_client.client_side_validation and ('ssh_key_name' not in params or
                                                       params['ssh_key_name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `ssh_key_name` when calling `delete_ssh_key`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'ssh_key_name' in params:
            path_params['sshKeyName'] = params['ssh_key_name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/ssh-keys/{sshKeyName}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_ssh_keys(self, **kwargs):  # noqa: E501
        """Get all SSH keys  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_ssh_keys(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[SshKey]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_ssh_keys_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_ssh_keys_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_ssh_keys_with_http_info(self, **kwargs):  # noqa: E501
        """Get all SSH keys  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_ssh_keys_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: list[SshKey]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_ssh_keys" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/ssh-keys', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[SshKey]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)