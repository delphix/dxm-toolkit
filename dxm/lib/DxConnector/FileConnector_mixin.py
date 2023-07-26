import pprint

class FileConnector_mixin:
    swagger_types = { 
     'file_connector_id' : 'integer',  
     'connector_name' : 'string',  
     'environment_id' : 'integer',  
     'file_type' : 'string',  
     'connection_info' : 'connection_info' 
     }

    swagger_map = { 
     'file_connector_id' : 'fileConnectorId',  
     'connector_name' : 'connectorName',  
     'environment_id' : 'environmentId',  
     'file_type' : 'fileType',  
     'connection_info' : 'connectionInfo' 
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
    def file_connector_id(self):
        if self.obj is not None and hasattr(self.obj,'file_connector_id'):
            return self.obj.file_connector_id
        else:
            return None

    @file_connector_id.setter
    def file_connector_id(self, file_connector_id):
        if self.obj is not None:
            self.obj.file_connector_id = file_connector_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def connector_name(self):
        if self.obj is not None and hasattr(self.obj,'connector_name'):
            return self.obj.connector_name
        else:
            return None

    @connector_name.setter
    def connector_name(self, connector_name):
        if self.obj is not None:
            self.obj.connector_name = connector_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def environment_id(self):
        if self.obj is not None and hasattr(self.obj,'environment_id'):
            return self.obj.environment_id
        else:
            return None

    @environment_id.setter
    def environment_id(self, environment_id):
        if self.obj is not None:
            self.obj.environment_id = environment_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_type(self):
        if self.obj is not None and hasattr(self.obj,'file_type'):
            return self.obj.file_type
        else:
            return None

    @file_type.setter
    def file_type(self, file_type):
        if self.obj is not None:
            self.obj.file_type = file_type
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def connection_info(self):
        if self.obj is not None and hasattr(self.obj,'connection_info'):
            return self.obj.connection_info
        else:
            return None

    @connection_info.setter
    def connection_info(self, connection_info):
        if self.obj is not None:
            self.obj.connection_info = connection_info
        else:
            raise ValueError("Object needs to be initialized first")
          