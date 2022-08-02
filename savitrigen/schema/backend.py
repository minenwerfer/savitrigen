import typing
from dataclasses import dataclass, field
from savitrigen.guideline import (
    check_collection_naming,
    check_field_naming
)

@dataclass
class Collection(object):
    module:str
    fields:dict
    _fields:dict = field(init=False, repr=False)

    unicon:str = ''
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
    module:str = None
    index:typing.Union[str,list[str]] = None


@dataclass
class BackendSchema(object):
    meta:dict
    collections:dict
    _collections:dict = field(init=False, repr=False)

    plugins:list[str] = None

    @property
    def collections(self) -> dict:
        return self._collections

    @collections.setter
    def collections(self, value:dict) -> None:
        ms = dict()

        for k, v in value.items():
            ms[k] = collection = Collection(**(v | dict(module=k)))
            check_collection_naming(k)

            for f_k, f_v in collection.fields.items():
                collection.fields[f_k] = Field(**f_v).__dict__
                check_field_naming(f_k)

            if True and 'documentation' not in v:
                raise ValueError('current config requires all collections to be documented whereas "{}" is not'.format(k))

        self._collections = ms
