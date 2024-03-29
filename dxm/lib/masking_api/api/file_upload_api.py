# coding: utf-8

"""
    Masking API

    Schema for the Continuous Compliance Engine API  # noqa: E501

    OpenAPI spec version: 5.1.18
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from dxm.lib.masking_api.api_client import ApiClient


class FileUploadApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_all_file_uploads(self, **kwargs):  # noqa: E501
        """Delete all files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_all_file_uploads(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool permanent: This indicates whether all of the files that should be deleted are in the permanent upload directory. This defaults to false so all of the files that are deleted are in the temporary upload directory.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_all_file_uploads_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.delete_all_file_uploads_with_http_info(**kwargs)  # noqa: E501
            return data

    def delete_all_file_uploads_with_http_info(self, **kwargs):  # noqa: E501
        """Delete all files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_all_file_uploads_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool permanent: This indicates whether all of the files that should be deleted are in the permanent upload directory. This defaults to false so all of the files that are deleted are in the temporary upload directory.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['permanent']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_all_file_uploads" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'permanent' in params:
            query_params.append(('permanent', params['permanent']))  # noqa: E501

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
            '/file-uploads', 'DELETE',
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

    def delete_file_by_uuid(self, file_uuid, **kwargs):  # noqa: E501
        """Delete permanent file upload by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file_by_uuid(file_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_file_by_uuid_with_http_info(file_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_file_by_uuid_with_http_info(file_uuid, **kwargs)  # noqa: E501
            return data

    def delete_file_by_uuid_with_http_info(self, file_uuid, **kwargs):  # noqa: E501
        """Delete permanent file upload by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_file_by_uuid_with_http_info(file_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_file_by_uuid" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_uuid' is set
        if self.api_client.client_side_validation and ('file_uuid' not in params or
                                                       params['file_uuid'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `file_uuid` when calling `delete_file_by_uuid`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_uuid' in params:
            path_params['fileUuid'] = params['file_uuid']  # noqa: E501

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
            '/file-uploads/{fileUuid}', 'DELETE',
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

    def get_all_files(self, **kwargs):  # noqa: E501
        """Get all files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_files(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool permanent: This indicates whether the file should be persisted permanently. Note that this should be set to true for files like an OAuth settings file, i.e., files that are not explicitly referenced by a JDBC driver, algorithm or driver support plugin, or connection properties file.
        :param int page_number: The page number for which to get algorithms. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: FileUploadList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_files_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_files_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_files_with_http_info(self, **kwargs):  # noqa: E501
        """Get all files  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_files_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param bool permanent: This indicates whether the file should be persisted permanently. Note that this should be set to true for files like an OAuth settings file, i.e., files that are not explicitly referenced by a JDBC driver, algorithm or driver support plugin, or connection properties file.
        :param int page_number: The page number for which to get algorithms. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: FileUploadList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['permanent', 'page_number', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_files" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'permanent' in params:
            query_params.append(('permanent', params['permanent']))  # noqa: E501
        if 'page_number' in params:
            query_params.append(('page_number', params['page_number']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501

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
            '/file-uploads', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileUploadList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file_by_uuid(self, file_uuid, **kwargs):  # noqa: E501
        """Get file upload by ID  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_by_uuid(file_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to get (required)
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_by_uuid_with_http_info(file_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_by_uuid_with_http_info(file_uuid, **kwargs)  # noqa: E501
            return data

    def get_file_by_uuid_with_http_info(self, file_uuid, **kwargs):  # noqa: E501
        """Get file upload by ID  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_by_uuid_with_http_info(file_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to get (required)
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file_by_uuid" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_uuid' is set
        if self.api_client.client_side_validation and ('file_uuid' not in params or
                                                       params['file_uuid'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `file_uuid` when calling `get_file_by_uuid`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_uuid' in params:
            path_params['fileUuid'] = params['file_uuid']  # noqa: E501

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
            '/file-uploads/{fileUuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileUpload',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_file_by_uuid(self, file_uuid, file, **kwargs):  # noqa: E501
        """Update permanent file upload by ID  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_by_uuid(file_uuid, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to update (required)
        :param file file: The file to be uploaded. (required)
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_file_by_uuid_with_http_info(file_uuid, file, **kwargs)  # noqa: E501
        else:
            (data) = self.update_file_by_uuid_with_http_info(file_uuid, file, **kwargs)  # noqa: E501
            return data

    def update_file_by_uuid_with_http_info(self, file_uuid, file, **kwargs):  # noqa: E501
        """Update permanent file upload by ID  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_file_by_uuid_with_http_info(file_uuid, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_uuid: The unique identifier of the permanently uploaded file to update (required)
        :param file file: The file to be uploaded. (required)
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file_uuid', 'file']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_file_by_uuid" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_uuid' is set
        if self.api_client.client_side_validation and ('file_uuid' not in params or
                                                       params['file_uuid'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `file_uuid` when calling `update_file_by_uuid`")  # noqa: E501
        # verify the required parameter 'file' is set
        if self.api_client.client_side_validation and ('file' not in params or
                                                       params['file'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `file` when calling `update_file_by_uuid`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_uuid' in params:
            path_params['fileUuid'] = params['file_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            local_var_files['file'] = params['file']  # noqa: E501

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
            '/file-uploads/{fileUuid}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileUpload',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def upload_file(self, file, **kwargs):  # noqa: E501
        """Upload file  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_file(file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file file: The file to be uploaded. (required)
        :param bool permanent: This indicates whether the file should be persisted permanently. Note that this should be set to true for files like an OAuth settings file, i.e., files that are not explicitly referenced by a JDBC driver, algorithm or driver support plugin, or connection properties file.
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.upload_file_with_http_info(file, **kwargs)  # noqa: E501
        else:
            (data) = self.upload_file_with_http_info(file, **kwargs)  # noqa: E501
            return data

    def upload_file_with_http_info(self, file, **kwargs):  # noqa: E501
        """Upload file  # noqa: E501

        WARNING: The generated curl command is incorrect, so please refer to the Masking API guide for instructions on how to upload files through the API  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.upload_file_with_http_info(file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param file file: The file to be uploaded. (required)
        :param bool permanent: This indicates whether the file should be persisted permanently. Note that this should be set to true for files like an OAuth settings file, i.e., files that are not explicitly referenced by a JDBC driver, algorithm or driver support plugin, or connection properties file.
        :return: FileUpload
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file', 'permanent']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upload_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file' is set
        if self.api_client.client_side_validation and ('file' not in params or
                                                       params['file'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `file` when calling `upload_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'permanent' in params:
            query_params.append(('permanent', params['permanent']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in params:
            local_var_files['file'] = params['file']  # noqa: E501

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
            '/file-uploads', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileUpload',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
