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


class MainframeDatasetMetadataApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_mainframe_dataset_metadata(self, body, **kwargs):  # noqa: E501
        """Create Mainframe Dataset metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_mainframe_dataset_metadata(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MainframeDatasetMetadata body: The Mainframe Dataset metadata to create (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_mainframe_dataset_metadata_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.create_mainframe_dataset_metadata_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def create_mainframe_dataset_metadata_with_http_info(self, body, **kwargs):  # noqa: E501
        """Create Mainframe Dataset metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_mainframe_dataset_metadata_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param MainframeDatasetMetadata body: The Mainframe Dataset metadata to create (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_mainframe_dataset_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and ('body' not in params or
                                                       params['body'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `body` when calling `create_mainframe_dataset_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/mainframe-dataset-metadata', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MainframeDatasetMetadata',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_mainframe_dataset_metadata(self, mainframe_dataset_metadata_id, **kwargs):  # noqa: E501
        """Delete Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_mainframe_dataset_metadata(mainframe_dataset_metadata_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, **kwargs)  # noqa: E501
            return data

    def delete_mainframe_dataset_metadata_with_http_info(self, mainframe_dataset_metadata_id, **kwargs):  # noqa: E501
        """Delete Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to delete (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['mainframe_dataset_metadata_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_mainframe_dataset_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'mainframe_dataset_metadata_id' is set
        if self.api_client.client_side_validation and ('mainframe_dataset_metadata_id' not in params or
                                                       params['mainframe_dataset_metadata_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `mainframe_dataset_metadata_id` when calling `delete_mainframe_dataset_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'mainframe_dataset_metadata_id' in params:
            path_params['mainframeDatasetMetadataId'] = params['mainframe_dataset_metadata_id']  # noqa: E501

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
            '/mainframe-dataset-metadata/{mainframeDatasetMetadataId}', 'DELETE',
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

    def get_all_mainframe_dataset_metadata(self, **kwargs):  # noqa: E501
        """Get all Mainframe Dataset metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_mainframe_dataset_metadata(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int ruleset_id: The ID of the ruleset to get all Mainframe Dataset metadata from
        :param int page_number: The page number for which to get Mainframe Dataset metadata. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: MainframeDatasetMetadataList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_mainframe_dataset_metadata_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_mainframe_dataset_metadata_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_mainframe_dataset_metadata_with_http_info(self, **kwargs):  # noqa: E501
        """Get all Mainframe Dataset metadata  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_mainframe_dataset_metadata_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int ruleset_id: The ID of the ruleset to get all Mainframe Dataset metadata from
        :param int page_number: The page number for which to get Mainframe Dataset metadata. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: MainframeDatasetMetadataList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['ruleset_id', 'page_number', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_mainframe_dataset_metadata" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ruleset_id' in params:
            query_params.append(('ruleset_id', params['ruleset_id']))  # noqa: E501
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
            '/mainframe-dataset-metadata', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MainframeDatasetMetadataList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_mainframe_dataset_metadata_by_id(self, mainframe_dataset_metadata_id, **kwargs):  # noqa: E501
        """Get Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_mainframe_dataset_metadata_by_id(mainframe_dataset_metadata_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to get (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_mainframe_dataset_metadata_by_id_with_http_info(mainframe_dataset_metadata_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_mainframe_dataset_metadata_by_id_with_http_info(mainframe_dataset_metadata_id, **kwargs)  # noqa: E501
            return data

    def get_mainframe_dataset_metadata_by_id_with_http_info(self, mainframe_dataset_metadata_id, **kwargs):  # noqa: E501
        """Get Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_mainframe_dataset_metadata_by_id_with_http_info(mainframe_dataset_metadata_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to get (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['mainframe_dataset_metadata_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_mainframe_dataset_metadata_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'mainframe_dataset_metadata_id' is set
        if self.api_client.client_side_validation and ('mainframe_dataset_metadata_id' not in params or
                                                       params['mainframe_dataset_metadata_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `mainframe_dataset_metadata_id` when calling `get_mainframe_dataset_metadata_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'mainframe_dataset_metadata_id' in params:
            path_params['mainframeDatasetMetadataId'] = params['mainframe_dataset_metadata_id']  # noqa: E501

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
            '/mainframe-dataset-metadata/{mainframeDatasetMetadataId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MainframeDatasetMetadata',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_mainframe_dataset_metadata(self, mainframe_dataset_metadata_id, body, **kwargs):  # noqa: E501
        """Update Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_mainframe_dataset_metadata(mainframe_dataset_metadata_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to update (required)
        :param MainframeDatasetMetadata body: The updated Mainframe Dataset metadata (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, body, **kwargs)  # noqa: E501
        else:
            (data) = self.update_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, body, **kwargs)  # noqa: E501
            return data

    def update_mainframe_dataset_metadata_with_http_info(self, mainframe_dataset_metadata_id, body, **kwargs):  # noqa: E501
        """Update Mainframe Dataset metadata by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_mainframe_dataset_metadata_with_http_info(mainframe_dataset_metadata_id, body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int mainframe_dataset_metadata_id: The ID of the Mainframe Dataset metadata to update (required)
        :param MainframeDatasetMetadata body: The updated Mainframe Dataset metadata (required)
        :return: MainframeDatasetMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['mainframe_dataset_metadata_id', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_mainframe_dataset_metadata" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'mainframe_dataset_metadata_id' is set
        if self.api_client.client_side_validation and ('mainframe_dataset_metadata_id' not in params or
                                                       params['mainframe_dataset_metadata_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `mainframe_dataset_metadata_id` when calling `update_mainframe_dataset_metadata`")  # noqa: E501
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and ('body' not in params or
                                                       params['body'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `body` when calling `update_mainframe_dataset_metadata`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'mainframe_dataset_metadata_id' in params:
            path_params['mainframeDatasetMetadataId'] = params['mainframe_dataset_metadata_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/mainframe-dataset-metadata/{mainframeDatasetMetadataId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='MainframeDatasetMetadata',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
