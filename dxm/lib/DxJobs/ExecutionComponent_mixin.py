import pprint

class ExecutionComponent_mixin:
    swagger_types = { 
     'execution_component_id' : 'integer',  
     'component_name' : 'string',  
     'execution_id' : 'integer',  
     'status' : 'string',  
     'rows_masked' : 'integer',  
     'rows_total' : 'integer',  
     'bytes_processed' : 'integer',  
     'bytes_total' : 'integer',  
     'start_time' : 'string',  
     'end_time' : 'string',  
     'log_file' : 'string',  
     'non_conforming_data_count' : 'integer' 
     }

    swagger_map = { 
     'execution_component_id' : 'executionComponentId',  
     'component_name' : 'componentName',  
     'execution_id' : 'executionId',  
     'status' : 'status',  
     'rows_masked' : 'rowsMasked',  
     'rows_total' : 'rowsTotal',  
     'bytes_processed' : 'bytesProcessed',  
     'bytes_total' : 'bytesTotal',  
     'start_time' : 'startTime',  
     'end_time' : 'endTime',  
     'log_file' : 'logFile',  
     'non_conforming_data_count' : 'nonConformingDataCount' 
     }

    @property
    def obj(self):
        if self._obj is not None:
            return self._obj
        else:
            return None

    @obj.setter
    def obj(self, value):
        self._obj = value

    def to_dict_all(self):
        return { k:getattr(self, k) for k,v in self.swagger_map.items() if hasattr(self, k) }

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()

     
    @property
    def execution_component_id(self):
        if self.obj is not None and hasattr(self.obj,'execution_component_id'):
            return self.obj.execution_component_id
        else:
            return None

    @execution_component_id.setter
    def execution_component_id(self, execution_component_id):
        if self.obj is not None:
            self.obj.execution_component_id = execution_component_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def component_name(self):
        if self.obj is not None and hasattr(self.obj,'component_name'):
            return self.obj.component_name
        else:
            return None

    @component_name.setter
    def component_name(self, component_name):
        if self.obj is not None:
            self.obj.component_name = component_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def execution_id(self):
        if self.obj is not None and hasattr(self.obj,'execution_id'):
            return self.obj.execution_id
        else:
            return None

    @execution_id.setter
    def execution_id(self, execution_id):
        if self.obj is not None:
            self.obj.execution_id = execution_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def status(self):
        if self.obj is not None and hasattr(self.obj,'status'):
            return self.obj.status
        else:
            return None

    @status.setter
    def status(self, status):
        if self.obj is not None:
            self.obj.status = status
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def rows_masked(self):
        if self.obj is not None and hasattr(self.obj,'rows_masked'):
            return self.obj.rows_masked
        else:
            return None

    @rows_masked.setter
    def rows_masked(self, rows_masked):
        if self.obj is not None:
            self.obj.rows_masked = rows_masked
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def rows_total(self):
        if self.obj is not None and hasattr(self.obj,'rows_total'):
            return self.obj.rows_total
        else:
            return None

    @rows_total.setter
    def rows_total(self, rows_total):
        if self.obj is not None:
            self.obj.rows_total = rows_total
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def bytes_processed(self):
        if self.obj is not None and hasattr(self.obj,'bytes_processed'):
            return self.obj.bytes_processed
        else:
            return None

    @bytes_processed.setter
    def bytes_processed(self, bytes_processed):
        if self.obj is not None:
            self.obj.bytes_processed = bytes_processed
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def bytes_total(self):
        if self.obj is not None and hasattr(self.obj,'bytes_total'):
            return self.obj.bytes_total
        else:
            return None

    @bytes_total.setter
    def bytes_total(self, bytes_total):
        if self.obj is not None:
            self.obj.bytes_total = bytes_total
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def start_time(self):
        if self.obj is not None and hasattr(self.obj,'start_time'):
            return self.obj.start_time
        else:
            return None

    @start_time.setter
    def start_time(self, start_time):
        if self.obj is not None:
            self.obj.start_time = start_time
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def end_time(self):
        if self.obj is not None and hasattr(self.obj,'end_time'):
            return self.obj.end_time
        else:
            return None

    @end_time.setter
    def end_time(self, end_time):
        if self.obj is not None:
            self.obj.end_time = end_time
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def log_file(self):
        if self.obj is not None and hasattr(self.obj,'log_file'):
            return self.obj.log_file
        else:
            return None

    @log_file.setter
    def log_file(self, log_file):
        if self.obj is not None:
            self.obj.log_file = log_file
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def non_conforming_data_count(self):
        if self.obj is not None and hasattr(self.obj,'non_conforming_data_count'):
            return self.obj.non_conforming_data_count
        else:
            return None

    @non_conforming_data_count.setter
    def non_conforming_data_count(self, non_conforming_data_count):
        if self.obj is not None:
            self.obj.non_conforming_data_count = non_conforming_data_count
        else:
            raise ValueError("Object needs to be initialized first")
          