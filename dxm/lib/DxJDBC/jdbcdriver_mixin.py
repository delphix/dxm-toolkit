import pprint

class JdbcDriver_mixin:
    swagger_types = { 
     'jdbc_driver_id' : 'integer',  
     'driver_name' : 'string',  
     'driver_class_name' : 'string',  
     'description' : 'string',  
     'version' : 'string',  
     'uploaded_by' : 'string',  
     'upload_date' : 'string',  
     'checksum' : 'string',  
     'built_in' : 'boolean',  
     'logger_installed' : 'boolean',  
     'file_reference_id' : 'string',  
     'driver_support_id' : 'integer' 
     }

    swagger_map = { 
     'jdbc_driver_id' : 'jdbcDriverId',  
     'driver_name' : 'driverName',  
     'driver_class_name' : 'driverClassName',  
     'description' : 'description',  
     'version' : 'version',  
     'uploaded_by' : 'uploadedBy',  
     'upload_date' : 'uploadDate',  
     'checksum' : 'checksum',  
     'built_in' : 'builtIn',  
     'logger_installed' : 'loggerInstalled',  
     'file_reference_id' : 'fileReferenceId',  
     'driver_support_id' : 'driverSupportId' 
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
    def jdbc_driver_id(self):
        if self.obj is not None and hasattr(self.obj,'jdbc_driver_id'):
            return self.obj.jdbc_driver_id
        else:
            return None

    @jdbc_driver_id.setter
    def jdbc_driver_id(self, jdbc_driver_id):
        if self.obj is not None:
            self.obj.jdbc_driver_id = jdbc_driver_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def driver_name(self):
        if self.obj is not None and hasattr(self.obj,'driver_name'):
            return self.obj.driver_name
        else:
            return None

    @driver_name.setter
    def driver_name(self, driver_name):
        if self.obj is not None:
            self.obj.driver_name = driver_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def driver_class_name(self):
        if self.obj is not None and hasattr(self.obj,'driver_class_name'):
            return self.obj.driver_class_name
        else:
            return None

    @driver_class_name.setter
    def driver_class_name(self, driver_class_name):
        if self.obj is not None:
            self.obj.driver_class_name = driver_class_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def description(self):
        if self.obj is not None and hasattr(self.obj,'description'):
            return self.obj.description
        else:
            return None

    @description.setter
    def description(self, description):
        if self.obj is not None:
            self.obj.description = description
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def version(self):
        if self.obj is not None and hasattr(self.obj,'version'):
            return self.obj.version
        else:
            return None

    @version.setter
    def version(self, version):
        if self.obj is not None:
            self.obj.version = version
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def uploaded_by(self):
        if self.obj is not None and hasattr(self.obj,'uploaded_by'):
            return self.obj.uploaded_by
        else:
            return None

    @uploaded_by.setter
    def uploaded_by(self, uploaded_by):
        if self.obj is not None:
            self.obj.uploaded_by = uploaded_by
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def upload_date(self):
        if self.obj is not None and hasattr(self.obj,'upload_date'):
            return self.obj.upload_date
        else:
            return None

    @upload_date.setter
    def upload_date(self, upload_date):
        if self.obj is not None:
            self.obj.upload_date = upload_date
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def checksum(self):
        if self.obj is not None and hasattr(self.obj,'checksum'):
            return self.obj.checksum
        else:
            return None

    @checksum.setter
    def checksum(self, checksum):
        if self.obj is not None:
            self.obj.checksum = checksum
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def built_in(self):
        if self.obj is not None and hasattr(self.obj,'built_in'):
            return self.obj.built_in
        else:
            return None

    @built_in.setter
    def built_in(self, built_in):
        if self.obj is not None:
            self.obj.built_in = built_in
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def logger_installed(self):
        if self.obj is not None and hasattr(self.obj,'logger_installed'):
            return self.obj.logger_installed
        else:
            return None

    @logger_installed.setter
    def logger_installed(self, logger_installed):
        if self.obj is not None:
            self.obj.logger_installed = logger_installed
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_reference_id(self):
        if self.obj is not None and hasattr(self.obj,'file_reference_id'):
            return self.obj.file_reference_id
        else:
            return None

    @file_reference_id.setter
    def file_reference_id(self, file_reference_id):
        if self.obj is not None:
            self.obj.file_reference_id = file_reference_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def driver_support_id(self):
        if self.obj is not None and hasattr(self.obj,'driver_support_id'):
            return self.obj.driver_support_id
        else:
            return None

    @driver_support_id.setter
    def driver_support_id(self, driver_support_id):
        if self.obj is not None:
            self.obj.driver_support_id = driver_support_id
        else:
            raise ValueError("Object needs to be initialized first")
          