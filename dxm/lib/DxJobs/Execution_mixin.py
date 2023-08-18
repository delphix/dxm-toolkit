import pprint

class Execution_mixin:
    swagger_types = { 
     'execution_id' : 'integer',  
     'job_id' : 'integer',  
     'connector_type' : 'string',  
     'source_connector_id' : 'integer',  
     'target_connector_id' : 'integer',  
     'status' : 'string',  
     'rows_masked' : 'integer',  
     'rows_total' : 'integer',  
     'bytes_processed' : 'integer',  
     'bytes_total' : 'integer',  
     'start_time' : 'string',  
     'end_time' : 'string',  
     'submit_time' : 'string' 
     }

    swagger_map = { 
     'execution_id' : 'executionId',  
     'job_id' : 'jobId',  
     'connector_type' : 'connectorType',  
     'source_connector_id' : 'sourceConnectorId',  
     'target_connector_id' : 'targetConnectorId',  
     'status' : 'status',  
     'rows_masked' : 'rowsMasked',  
     'rows_total' : 'rowsTotal',  
     'bytes_processed' : 'bytesProcessed',  
     'bytes_total' : 'bytesTotal',  
     'start_time' : 'startTime',  
     'end_time' : 'endTime',  
     'submit_time' : 'submitTime' 
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
    def job_id(self):
        if self.obj is not None and hasattr(self.obj,'job_id'):
            return self.obj.job_id
        else:
            return None

    @job_id.setter
    def job_id(self, job_id):
        if self.obj is not None:
            self.obj.job_id = job_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def connector_type(self):
        if self.obj is not None and hasattr(self.obj,'connector_type'):
            return self.obj.connector_type
        else:
            return None

    @connector_type.setter
    def connector_type(self, connector_type):
        if self.obj is not None:
            self.obj.connector_type = connector_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def source_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'source_connector_id'):
            return self.obj.source_connector_id
        else:
            return None

    @source_connector_id.setter
    def source_connector_id(self, source_connector_id):
        if self.obj is not None:
            self.obj.source_connector_id = source_connector_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def target_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'target_connector_id'):
            return self.obj.target_connector_id
        else:
            return None

    @target_connector_id.setter
    def target_connector_id(self, target_connector_id):
        if self.obj is not None:
            self.obj.target_connector_id = target_connector_id
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
    def submit_time(self):
        if self.obj is not None and hasattr(self.obj,'submit_time'):
            return self.obj.submit_time
        else:
            return None

    @submit_time.setter
    def submit_time(self, submit_time):
        if self.obj is not None:
            self.obj.submit_time = submit_time
        else:
            raise ValueError("Object needs to be initialized first")
          