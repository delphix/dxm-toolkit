import pprint

class ColumnMetadata_mixin:
    swagger_types = { 
     'column_metadata_id' : 'integer',  
     'column_name' : 'string',  
     'table_metadata_id' : 'integer',  
     'algorithm_name' : 'string',  
     'algorithm_field_id' : 'integer',  
     'algorithm_group_no' : 'integer',  
     'domain_name' : 'string',  
     'data_type' : 'string',  
     'date_format' : 'string',  
     'column_length' : 'integer',  
     'is_masked' : 'boolean',  
     'is_profiler_writable' : 'boolean',  
     'is_primary_key' : 'boolean',  
     'is_index' : 'boolean',  
     'is_foreign_key' : 'boolean',  
     'notes' : 'string' 
     }

    swagger_map = { 
     'column_metadata_id' : 'columnMetadataId',  
     'column_name' : 'columnName',  
     'table_metadata_id' : 'tableMetadataId',  
     'algorithm_name' : 'algorithmName',  
     'algorithm_field_id' : 'algorithmFieldId',  
     'algorithm_group_no' : 'algorithmGroupNo',  
     'domain_name' : 'domainName',  
     'data_type' : 'dataType',  
     'date_format' : 'dateFormat',  
     'column_length' : 'columnLength',  
     'is_masked' : 'isMasked',  
     'is_profiler_writable' : 'isProfilerWritable',  
     'is_primary_key' : 'isPrimaryKey',  
     'is_index' : 'isIndex',  
     'is_foreign_key' : 'isForeignKey',  
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
    def column_metadata_id(self):
        if self.obj is not None and hasattr(self.obj,'column_metadata_id'):
            return self.obj.column_metadata_id
        else:
            return None

    @column_metadata_id.setter
    def column_metadata_id(self, column_metadata_id):
        if self.obj is not None:
            self.obj.column_metadata_id = column_metadata_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def column_name(self):
        if self.obj is not None and hasattr(self.obj,'column_name'):
            return self.obj.column_name
        else:
            return None

    @column_name.setter
    def column_name(self, column_name):
        if self.obj is not None:
            self.obj.column_name = column_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def table_metadata_id(self):
        if self.obj is not None and hasattr(self.obj,'table_metadata_id'):
            return self.obj.table_metadata_id
        else:
            return None

    @table_metadata_id.setter
    def table_metadata_id(self, table_metadata_id):
        if self.obj is not None:
            self.obj.table_metadata_id = table_metadata_id
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
    def data_type(self):
        if self.obj is not None and hasattr(self.obj,'data_type'):
            return self.obj.data_type
        else:
            return None

    @data_type.setter
    def data_type(self, data_type):
        if self.obj is not None:
            self.obj.data_type = data_type
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
    def column_length(self):
        if self.obj is not None and hasattr(self.obj,'column_length'):
            return self.obj.column_length
        else:
            return None

    @column_length.setter
    def column_length(self, column_length):
        if self.obj is not None:
            self.obj.column_length = column_length
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
    def is_primary_key(self):
        if self.obj is not None and hasattr(self.obj,'is_primary_key'):
            return self.obj.is_primary_key
        else:
            return None

    @is_primary_key.setter
    def is_primary_key(self, is_primary_key):
        if self.obj is not None:
            self.obj.is_primary_key = is_primary_key
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_index(self):
        if self.obj is not None and hasattr(self.obj,'is_index'):
            return self.obj.is_index
        else:
            return None

    @is_index.setter
    def is_index(self, is_index):
        if self.obj is not None:
            self.obj.is_index = is_index
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def is_foreign_key(self):
        if self.obj is not None and hasattr(self.obj,'is_foreign_key'):
            return self.obj.is_foreign_key
        else:
            return None

    @is_foreign_key.setter
    def is_foreign_key(self, is_foreign_key):
        if self.obj is not None:
            self.obj.is_foreign_key = is_foreign_key
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
          