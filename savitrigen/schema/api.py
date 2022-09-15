import typing
from dataclasses import dataclass, field
from savitrigen.guideline import (
    check_collection_naming,
    check_field_naming
)

from .util import dataclass_to_dict, snake_to_camel

@dataclass
class ApiConfig(object):
    group:str = None
    roles:list[str] = None
    allow_signup:list[str] = None
    signup_defaults:dict = None
    populate_user_extra:list[str] = None

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
class CollectionAction(object):
    name:str
    unicon:str = None
    ask:bool = None
    fetch_item:bool = None
    clear_item:bool = None


@dataclass
class Collection(object):
    collection:str
    fields:dict
    options:ControllerOptions
    actions:dict
    individual_actions:dict

    _fields:dict = field(init=False, repr=False)
    _options:ControllerOptions = field(init=False, repr=False)
    _actions:dict = field(init=False, repr=False)
    _individual_actions:dict = field(init=False, repr=False)

    form:list[str] = None
    table:list[str] = None
    form_layout:dict = None

    alias:str = None
    unicon:str = None
    strict:bool = None
    route:bool = None
    report:bool = None
    presets:list[str] = None
    methods:list[str] = None

    """Those below are unused"""
    documentation:str = 'undocumented'
    translation:dict = None

    @property
    def fields(self) -> dict:
        if not self._fields:
            return None

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
        return dataclass_to_dict(self._options, convert_casing=True)

    @options.setter
    def options(self, _value:dict) -> None:
        if not _value:
            self._options = None
            return

        value = _value | {
            'query_preset': _value.get('query_preset')
        }

        self._options = ControllerOptions(**value)

    @property
    def actions(self) -> dict:
        if not self._actions:
            return None

        return {
            snake_to_camel(k): dataclass_to_dict(v, convert_casing=True)
            for k, v in self._actions.items()
        }

    @actions.setter
    def actions(self, value:dict) -> dict:
        if not value:
            self._actions = None
            return

        self._actions = {
            k: CollectionAction(v)
            for k, v in value.items()
        }

    @property
    def individual_actions(self) -> dict:
        if not self._individual_actions:
            return None

        return {
            snake_to_camel(k): dataclass_to_dict(v, convert_casing=True)
            for k, v in self._individual_actions.items()
        }

    @individual_actions.setter
    def individual_actions(self, value:dict) -> dict:
        if not value:
            self._individual_actions = None
            return

        self._individual_actions = {
            k: CollectionAction(**v)
            for k, v in value.items()
        }


@dataclass
class Field(object):
    label:str
    type:str = None

    description:str = None

    required:bool = False
    readonly:bool = False
    array:bool = False
    expand:bool = False
    values:list = None
    mask:str = None

    """Collection specific properties"""
    collection:str = None
    index:typing.Union[str,list[str]] = None
    form:list[str] = None


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

        def fulfill(v):
            keys = [
                'options',
                'fields',
                'actions',
                'individual_actions'
            ]

            return {
                k: v.get(k, None)
                for k in keys
            }

        for k, v in value.items():
            k = snake_to_camel(k)
            collection = v | {
                'collection': k,
                **fulfill(v)
            }

            ms[k] = collection = Collection(**collection)
            check_collection_naming(k)

            if collection.fields:
                for f_k, f_v in collection.fields.items():
                    collection.fields[f_k] = Field(**f_v).__dict__
                    check_field_naming(f_k)

            if True and 'documentation' not in v:
                raise ValueError('current config requires all collections to be documented whereas "{}" is not'.format(k))

        self._collections = ms
