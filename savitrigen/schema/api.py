import typing
from dataclasses import dataclass, field
from savitrigen.guideline import (
    check_collection_naming,
    check_field_naming
)

from .util import dataclass_to_dict, snake_to_camel

@dataclass
class ApiConfig(object):
    roles: list[str]

@dataclass
class QueryPreset(object):
    filters:dict = None
    sort:dict = None

@dataclass
class ControllerOptions(object):
    query_preset:QueryPreset
    _query_preset:QueryPreset = field(init=False, repr=False)

    @property
    def query_preset(self) -> QueryPreset:
        return self._query_preset

    @query_preset.setter
    def query_preset(self, value:dict) -> None:
        self._query_preset = QueryPreset(**value) \
            if value else None


@dataclass
class Collection(object):
    collection:str
    fields:dict
    options:ControllerOptions

    _fields:dict = field(init=False, repr=False)
    _options:ControllerOptions = field(init=False, repr=False)

    alias:str = None
    unicon:str = None
    strict:bool = False
    route:bool = False
    report:bool = False
    presets:list[str] = None
    methods:list[str] = None

    """Those below are unused"""
    documentation:str = 'undocumented'
    translation:dict = None

    @property
    def fields(self) -> dict:
        ms = dict()

        for k, v in self._fields.items():
            ms[k] = {
                f_k: f_v
                for f_k, f_v in v.items()
                if f_v is not None
            }

        return ms

    @fields.setter
    def fields(self, value:dict) -> None:
        self._fields = value

    @property
    def options(self) -> ControllerOptions:
        return self._options

    @options.setter
    def options(self, _value:dict) -> None:
        value = _value | {
            'query_preset': _value.get('query_preset')
        }

        value = ControllerOptions(**value)
        self._options = {
            snake_to_camel(k): v
            for k, v in dataclass_to_dict(value).items()
        }


@dataclass
class Field(object):
    label:str
    type:str = None

    description:str = None

    required:bool = False
    readonly:bool = False
    array:bool = False
    values:list = None
    mask:str = None

    """Collection specific properties"""
    collection:str = None
    index:typing.Union[str,list[str]] = None


@dataclass
class ApiSchema(object):
    meta:dict
    config:dict
    collections:dict

    _config:dict = field(init=False, repr=False)
    _collections:dict = field(init=False, repr=False)

    plugins:list[str] = None

    @property
    def config(self) -> dict:
        return self._config

    @config.setter
    def config(self, value:dict) -> None:
        self._config = ApiConfig(**value)

    @property
    def collections(self) -> dict:
        return self._collections

    @collections.setter
    def collections(self, value:dict) -> None:
        ms = dict()

        for k, v in value.items():
            collection = v | {
                'collection': k,
                'options': v.get('options', {}),
                'fields': v.get('fields', {})
            }

            ms[k] = collection = Collection(**collection)
            check_collection_naming(k)

            for f_k, f_v in collection.fields.items():
                collection.fields[f_k] = Field(**f_v).__dict__
                check_field_naming(f_k)

            if True and 'documentation' not in v:
                raise ValueError('current config requires all collections to be documented whereas "{}" is not'.format(k))

        self._collections = ms
