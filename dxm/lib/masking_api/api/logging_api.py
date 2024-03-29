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


class LoggingApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_execution_components(self, execution_id, **kwargs):  # noqa: E501
        """Get all execution components logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_execution_components(execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int execution_id: The ID of the Execution to get all component logs (required)
        :param int page_number: The page number for which to get executions component. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: ExecutionComponentLogsList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_execution_components_with_http_info(execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_all_execution_components_with_http_info(execution_id, **kwargs)  # noqa: E501
            return data

    def get_all_execution_components_with_http_info(self, execution_id, **kwargs):  # noqa: E501
        """Get all execution components logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_execution_components_with_http_info(execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int execution_id: The ID of the Execution to get all component logs (required)
        :param int page_number: The page number for which to get executions component. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: ExecutionComponentLogsList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['execution_id', 'page_number', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_execution_components" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'execution_id' is set
        if self.api_client.client_side_validation and ('execution_id' not in params or
                                                       params['execution_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `execution_id` when calling `get_all_execution_components`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'execution_id' in params:
            query_params.append(('execution_id', params['execution_id']))  # noqa: E501
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
            '/execution-component-log', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExecutionComponentLogsList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_execution_logs(self, **kwargs):  # noqa: E501
        """Get all execution logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_execution_logs(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int job_id: The ID of the job to get all executions for
        :param int page_number: The page number for which to get executions. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :param str execution_status: The status of the job execution. Note that, if this parameter is excluded, then all executions will be returned.
        :return: ExecutionLogsList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_execution_logs_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_execution_logs_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_execution_logs_with_http_info(self, **kwargs):  # noqa: E501
        """Get all execution logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_execution_logs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int job_id: The ID of the job to get all executions for
        :param int page_number: The page number for which to get executions. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :param str execution_status: The status of the job execution. Note that, if this parameter is excluded, then all executions will be returned.
        :return: ExecutionLogsList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['job_id', 'page_number', 'page_size', 'execution_status']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_execution_logs" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'job_id' in params:
            query_params.append(('job_id', params['job_id']))  # noqa: E501
        if 'page_number' in params:
            query_params.append(('page_number', params['page_number']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'execution_status' in params:
            query_params.append(('execution_status', params['execution_status']))  # noqa: E501

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
            '/execution-logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExecutionLogsList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_logs(self, **kwargs):  # noqa: E501
        """Get all logs. Note that the logs will be returned in order from most recent to least recent.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_logs(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str log_level: The log level of the log file. Note that, if this parameter is excluded, the log files will be returned in alphabetical order with respect to their log level.
        :param int page_number: The page number for which to get logs. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: LogFileInfoList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_logs_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_logs_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_logs_with_http_info(self, **kwargs):  # noqa: E501
        """Get all logs. Note that the logs will be returned in order from most recent to least recent.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_logs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str log_level: The log level of the log file. Note that, if this parameter is excluded, the log files will be returned in alphabetical order with respect to their log level.
        :param int page_number: The page number for which to get logs. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: LogFileInfoList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['log_level', 'page_number', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_logs" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'log_level' in params:
            query_params.append(('log_level', params['log_level']))  # noqa: E501
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
            '/application-logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LogFileInfoList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_audit_logs(self, **kwargs):  # noqa: E501
        """Get all audit logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_audit_logs(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str user_name: The name of the user that took the action for this entry.
        :param str action_type: The type of action that occurred for this Audit Log entry.
        :param str target: The type object or operation that the action occurred on for this Audit Log entry.
        :param str status: The status of the action that occurred for this Audit Log entry. This can change over time as ATTEMPTED actions are completed.
        :param str start_time: The date after which all audit logs should be retrieved. Note that the format of the string should be the same date-time format as in the response bodies.
        :param str end_time: The date before which all audit logs should be retrieved. Note that the format of the string should be the same date-time format as in the response bodies.
        :param str search_string: Search for activity description containing substring.
        :param str sort_by: Sort by field.
        :param str sort_dir: Sort by direction.
        :param int page_number: The page number for which to get logs. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: AuditLogList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_audit_logs_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_audit_logs_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_audit_logs_with_http_info(self, **kwargs):  # noqa: E501
        """Get all audit logs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_audit_logs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str user_name: The name of the user that took the action for this entry.
        :param str action_type: The type of action that occurred for this Audit Log entry.
        :param str target: The type object or operation that the action occurred on for this Audit Log entry.
        :param str status: The status of the action that occurred for this Audit Log entry. This can change over time as ATTEMPTED actions are completed.
        :param str start_time: The date after which all audit logs should be retrieved. Note that the format of the string should be the same date-time format as in the response bodies.
        :param str end_time: The date before which all audit logs should be retrieved. Note that the format of the string should be the same date-time format as in the response bodies.
        :param str search_string: Search for activity description containing substring.
        :param str sort_by: Sort by field.
        :param str sort_dir: Sort by direction.
        :param int page_number: The page number for which to get logs. This will default to the first page if excluded
        :param int page_size: The maximum number of objects to return. This will default to the DEFAULT_API_PAGE_SIZE property if not provided
        :return: AuditLogList
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['user_name', 'action_type', 'target', 'status', 'start_time', 'end_time', 'search_string', 'sort_by', 'sort_dir', 'page_number', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_audit_logs" % key
                )
            params[key] = val
        del params['kwargs']

        if self.api_client.client_side_validation and ('user_name' in params and
                                                       len(params['user_name']) > 1000):
            raise ValueError("Invalid value for parameter `user_name` when calling `get_audit_logs`, length must be less than or equal to `1000`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'user_name' in params:
            query_params.append(('user_name', params['user_name']))  # noqa: E501
        if 'action_type' in params:
            query_params.append(('action_type', params['action_type']))  # noqa: E501
        if 'target' in params:
            query_params.append(('target', params['target']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'start_time' in params:
            query_params.append(('start_time', params['start_time']))  # noqa: E501
        if 'end_time' in params:
            query_params.append(('end_time', params['end_time']))  # noqa: E501
        if 'search_string' in params:
            query_params.append(('search_string', params['search_string']))  # noqa: E501
        if 'sort_by' in params:
            query_params.append(('sort_by', params['sort_by']))  # noqa: E501
        if 'sort_dir' in params:
            query_params.append(('sort_dir', params['sort_dir']))  # noqa: E501
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
            '/audit-logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuditLogList',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_execution_component_by_id(self, component_id, **kwargs):  # noqa: E501
        """Get execution component log by component ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_execution_component_by_id(component_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int component_id: The ID of the execution to get (required)
        :return: ExecutionComponentLog
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_execution_component_by_id_with_http_info(component_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_execution_component_by_id_with_http_info(component_id, **kwargs)  # noqa: E501
            return data

    def get_execution_component_by_id_with_http_info(self, component_id, **kwargs):  # noqa: E501
        """Get execution component log by component ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_execution_component_by_id_with_http_info(component_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int component_id: The ID of the execution to get (required)
        :return: ExecutionComponentLog
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['component_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_execution_component_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'component_id' is set
        if self.api_client.client_side_validation and ('component_id' not in params or
                                                       params['component_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `component_id` when calling `get_execution_component_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'component_id' in params:
            path_params['componentId'] = params['component_id']  # noqa: E501

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
            '/execution-component-log/{componentId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExecutionComponentLog',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_execution_logs_by_id(self, execution_id, **kwargs):  # noqa: E501
        """Get all execution log by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_execution_logs_by_id(execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int execution_id: The ID of the execution to get (required)
        :return: ExecutionLog
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_execution_logs_by_id_with_http_info(execution_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_execution_logs_by_id_with_http_info(execution_id, **kwargs)  # noqa: E501
            return data

    def get_execution_logs_by_id_with_http_info(self, execution_id, **kwargs):  # noqa: E501
        """Get all execution log by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_execution_logs_by_id_with_http_info(execution_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int execution_id: The ID of the execution to get (required)
        :return: ExecutionLog
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['execution_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_execution_logs_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'execution_id' is set
        if self.api_client.client_side_validation and ('execution_id' not in params or
                                                       params['execution_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `execution_id` when calling `get_execution_logs_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'execution_id' in params:
            path_params['executionId'] = params['execution_id']  # noqa: E501

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
            '/execution-logs/{executionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExecutionLog',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
