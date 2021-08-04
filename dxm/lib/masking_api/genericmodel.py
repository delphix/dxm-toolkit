import re
import pprint
import json

class GenericModel(object):
    def __init__(self, data, swagger_types=None, swagger_map=None):
        self.swagger_types = swagger_types
        self.swagger_map = swagger_map

        for name, value in data.items():
            name = self.to_snake_case(name)
            value = self._wrap(value)
            setattr(self, name, value)

    def to_snake_case(self, name):
        name = name.replace('_','')
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)): 
            return type(value)([self._wrap(v) for v in value])
        else:
            return GenericModel(value) if isinstance(value, dict) else value

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda x: { k:v for k,v in x.__dict__.items() if "swagger" not in k } ))

    def to_dict_all(self):
        return json.loads(json.dumps(self, default=lambda x: x.__dict__ ))

    def to_str(self):
        return pprint.pformat(self.to_dict_all())

    def __repr__(self):
        return self.to_str()