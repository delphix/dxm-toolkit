import pprint

class FileFieldMetadata_mixin:
    swagger_types = { 
     'file_field_metadata_id' : 'integer',  
     'file_format_id' : 'integer',  
     'record_type_id' : 'integer',  
     'field_length' : 'integer',  
     'field_name' : 'string',  
     'field_position_number' : 'integer',  
     'algorithm_name' : 'string',  
     'algorithm_field_id' : 'integer',  
     'algorithm_group_no' : 'integer',  
     'domain_name' : 'string',  
     'date_format' : 'string',  
     'is_masked' : 'boolean',  
     'is_profiler_writable' : 'boolean',  
     'notes' : 'string' 
     }

    swagger_map = { 
     'file_field_metadata_id' : 'fileFieldMetadataId',  
     'file_format_id' : 'fileFormatId',  
     'record_type_id' : 'recordTypeId',  
     'field_length' : 'fieldLength',  
     'field_name' : 'fieldName',  
     'field_position_number' : 'fieldPositionNumber',  
     'algorithm_name' : 'algorithmName',  
     'algorithm_field_id' : 'algorithmFieldId',  
     'algorithm_group_no' : 'algorithmGroupNo',  
     'domain_name' : 'domainName',  
     'date_format' : 'dateFormat',  
     'is_masked' : 'isMasked',  
     'is_profiler_writable' : 'isProfilerWritable',  
     'notes' : 'notes' 
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
    def file_field_metadata_id(self):
        if self.obj is not None and hasattr(self.obj,'file_field_metadata_id'):
            return self.obj.file_field_metadata_id
        else:
            return None

    @file_field_metadata_id.setter
    def file_field_metadata_id(self, file_field_metadata_id):
        if self.obj is not None:
            self.obj.file_field_metadata_id = file_field_metadata_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def file_format_id(self):
        if self.obj is not None and hasattr(self.obj,'file_format_id'):
            return self.obj.file_format_id
        else:
            return None

    @file_format_id.setter
    def file_format_id(self, file_format_id):
        if self.obj is not None:
            self.obj.file_format_id = file_format_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def record_type_id(self):
        if self.obj is not None and hasattr(self.obj,'record_type_id'):
            return self.obj.record_type_id
        else:
            return None

    @record_type_id.setter
    def record_type_id(self, record_type_id):
        if self.obj is not None:
            self.obj.record_type_id = record_type_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def field_length(self):
        if self.obj is not None and hasattr(self.obj,'field_length'):
            return self.obj.field_length
        else:
            return None

    @field_length.setter
    def field_length(self, field_length):
        if self.obj is not None:
            self.obj.field_length = field_length
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def field_name(self):
        if self.obj is not None and hasattr(self.obj,'field_name'):
            return self.obj.field_name
        else:
            return None

    @field_name.setter
    def field_name(self, field_name):
        if self.obj is not None:
            self.obj.field_name = field_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def field_position_number(self):
        if self.obj is not None and hasattr(self.obj,'field_position_number'):
            return self.obj.field_position_number
        else:
            return None

    @field_position_number.setter
    def field_position_number(self, field_position_number):
        if self.obj is not None:
            self.obj.field_position_number = field_position_number
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
    def algorithm_field_id(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_field_id'):
            return self.obj.algorithm_field_id
        else:
            return None

    @algorithm_field_id.setter
    def algorithm_field_id(self, algorithm_field_id):
        if self.obj is not None:
            self.obj.algorithm_field_id = algorithm_field_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def algorithm_group_no(self):
        if self.obj is not None and hasattr(self.obj,'algorithm_group_no'):
            return self.obj.algorithm_group_no
        else:
            return None

    @algorithm_group_no.setter
    def algorithm_group_no(self, algorithm_group_no):
        if self.obj is not None:
            self.obj.algorithm_group_no = algorithm_group_no
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def domain_name(self):
        if self.obj is not None and hasattr(self.obj,'domain_name'):
            return self.obj.domain_name
        else:
            return None

    @domain_name.setter
    def domain_name(self, domain_name):
        if self.obj is not None:
            self.obj.domain_name = domain_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def date_format(self):
        if self.obj is not None and hasattr(self.obj,'date_format'):
            return self.obj.date_format
        else:
            return None

    @date_format.setter
    def date_format(self, date_format):
        if self.obj is not None:
            self.obj.date_format = date_format
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_masked(self):
        if self.obj is not None and hasattr(self.obj,'is_masked'):
            return self.obj.is_masked
        else:
            return None

    @is_masked.setter
    def is_masked(self, is_masked):
        if self.obj is not None:
            self.obj.is_masked = is_masked
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_profiler_writable(self):
        if self.obj is not None and hasattr(self.obj,'is_profiler_writable'):
            return self.obj.is_profiler_writable
        else:
            return None

    @is_profiler_writable.setter
    def is_profiler_writable(self, is_profiler_writable):
        if self.obj is not None:
            self.obj.is_profiler_writable = is_profiler_writable
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def notes(self):
        if self.obj is not None and hasattr(self.obj,'notes'):
            return self.obj.notes
        else:
            return None

    @notes.setter
    def notes(self, notes):
        if self.obj is not None:
            self.obj.notes = notes
        else:
            raise ValueError("Object needs to be initialized first")
          