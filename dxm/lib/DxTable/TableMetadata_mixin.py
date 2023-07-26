import pprint

class TableMetadata_mixin:
    swagger_types = { 
     'table_metadata_id' : 'integer',  
     'table_name' : 'string',  
     'ruleset_id' : 'integer',  
     'custom_sql' : 'string',  
     'where_clause' : 'string',  
     'having_clause' : 'string',  
     'key_column' : 'string',  
     'is_masked' : 'boolean' 
     }

    swagger_map = { 
     'table_metadata_id' : 'tableMetadataId',  
     'table_name' : 'tableName',  
     'ruleset_id' : 'rulesetId',  
     'custom_sql' : 'customSql',  
     'where_clause' : 'whereClause',  
     'having_clause' : 'havingClause',  
     'key_column' : 'keyColumn',  
     'is_masked' : 'isMasked' 
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
    def table_name(self):
        if self.obj is not None and hasattr(self.obj,'table_name'):
            return self.obj.table_name
        else:
            return None

    @table_name.setter
    def table_name(self, table_name):
        if self.obj is not None:
            self.obj.table_name = table_name
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def ruleset_id(self):
        if self.obj is not None and hasattr(self.obj,'ruleset_id'):
            return self.obj.ruleset_id
        else:
            return None

    @ruleset_id.setter
    def ruleset_id(self, ruleset_id):
        if self.obj is not None:
            self.obj.ruleset_id = ruleset_id
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def custom_sql(self):
        if self.obj is not None and hasattr(self.obj,'custom_sql'):
            return self.obj.custom_sql
        else:
            return None

    @custom_sql.setter
    def custom_sql(self, custom_sql):
        if self.obj is not None:
            self.obj.custom_sql = custom_sql
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def where_clause(self):
        if self.obj is not None and hasattr(self.obj,'where_clause'):
            return self.obj.where_clause
        else:
            return None

    @where_clause.setter
    def where_clause(self, where_clause):
        if self.obj is not None:
            self.obj.where_clause = where_clause
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def having_clause(self):
        if self.obj is not None and hasattr(self.obj,'having_clause'):
            return self.obj.having_clause
        else:
            return None

    @having_clause.setter
    def having_clause(self, having_clause):
        if self.obj is not None:
            self.obj.having_clause = having_clause
        else:
            raise ValueError("Object needs to be initialized first")
     
    @property
    def key_column(self):
        if self.obj is not None and hasattr(self.obj,'key_column'):
            return self.obj.key_column
        else:
            return None

    @key_column.setter
    def key_column(self, key_column):
        if self.obj is not None:
            self.obj.key_column = key_column
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
          