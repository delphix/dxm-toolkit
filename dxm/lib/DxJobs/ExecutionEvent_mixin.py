import pprint

class ExecutionEvent_mixin:
    swagger_types = { 
     'execution_event_id' : 'integer',  
     'execution_id' : 'integer',  
     'event_type' : 'string',  
     'severity' : 'string',  
     'cause' : 'string',  
     'count' : 'integer',  
     'time_stamp' : 'string',  
     'execution_component_id' : 'integer',  
     'masked_object_name' : 'string',  
     'masked_object_parent_name' : 'string',  
     'algorithm_name' : 'string',  
     'exception_type' : 'string',  
     'exception_detail' : 'string' 
     }

    swagger_map = { 
     'execution_event_id' : 'executionEventId',  
     'execution_id' : 'executionId',  
     'event_type' : 'eventType',  
     'severity' : 'severity',  
     'cause' : 'cause',  
     'count' : 'count',  
     'time_stamp' : 'timeStamp',  
     'execution_component_id' : 'executionComponentId',  
     'masked_object_name' : 'maskedObjectName',  
     'masked_object_parent_name' : 'maskedObjectParentName',  
     'algorithm_name' : 'algorithmName',  
     'exception_type' : 'exceptionType',  
     'exception_detail' : 'exceptionDetail' 
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
    def execution_event_id(self):
        if self.obj is not None and hasattr(self.obj,'execution_event_id'):
            return self.obj.execution_event_id
        else:
            return None

    @execution_event_id.setter
    def execution_event_id(self, execution_event_id):
        if self.obj is not None:
            self.obj.execution_event_id = execution_event_id
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
    def event_type(self):
        if self.obj is not None and hasattr(self.obj,'event_type'):
            return self.obj.event_type
        else:
            return None

    @event_type.setter
    def event_type(self, event_type):
        if self.obj is not None:
            self.obj.event_type = event_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def severity(self):
        if self.obj is not None and hasattr(self.obj,'severity'):
            return self.obj.severity
        else:
            return None

    @severity.setter
    def severity(self, severity):
        if self.obj is not None:
            self.obj.severity = severity
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def cause(self):
        if self.obj is not None and hasattr(self.obj,'cause'):
            return self.obj.cause
        else:
            return None

    @cause.setter
    def cause(self, cause):
        if self.obj is not None:
            self.obj.cause = cause
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def count(self):
        if self.obj is not None and hasattr(self.obj,'count'):
            return self.obj.count
        else:
            return None

    @count.setter
    def count(self, count):
        if self.obj is not None:
            self.obj.count = count
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def time_stamp(self):
        if self.obj is not None and hasattr(self.obj,'time_stamp'):
            return self.obj.time_stamp
        else:
            return None

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        if self.obj is not None:
            self.obj.time_stamp = time_stamp
        else:
            raise ValueError("Object needs to be initialized first")
     
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
    def masked_object_name(self):
        if self.obj is not None and hasattr(self.obj,'masked_object_name'):
            return self.obj.masked_object_name
        else:
            return None

    @masked_object_name.setter
    def masked_object_name(self, masked_object_name):
        if self.obj is not None:
            self.obj.masked_object_name = masked_object_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def masked_object_parent_name(self):
        if self.obj is not None and hasattr(self.obj,'masked_object_parent_name'):
            return self.obj.masked_object_parent_name
        else:
            return None

    @masked_object_parent_name.setter
    def masked_object_parent_name(self, masked_object_parent_name):
        if self.obj is not None:
            self.obj.masked_object_parent_name = masked_object_parent_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def algorithm_name(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_name'):
            return self.obj.algorithm_name
        else:
            return None

    @algorithm_name.setter
    def algorithm_name(self, algorithm_name):
        if self.obj is not None:
            self.obj.algorithm_name = algorithm_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def exception_type(self):
        if self.obj is not None and hasattr(self.obj,'exception_type'):
            return self.obj.exception_type
        else:
            return None

    @exception_type.setter
    def exception_type(self, exception_type):
        if self.obj is not None:
            self.obj.exception_type = exception_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def exception_detail(self):
        if self.obj is not None and hasattr(self.obj,'exception_detail'):
            return self.obj.exception_detail
        else:
            return None

    @exception_detail.setter
    def exception_detail(self, exception_detail):
        if self.obj is not None:
            self.obj.exception_detail = exception_detail
        else:
            raise ValueError("Object needs to be initialized first")
          