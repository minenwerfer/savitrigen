from string import Template

"""Used in models"""
DocumentImportTemplate = Template(
r"import { ${pascal_case}Document } from '../${camel_case}/${camel_case}.model'"
)

ReferenceImportTemplate = Template(
r"import '../${camel_case}/${camel_case}.model'"
)

CommonDocumentImportTemplate = Template(
r"import { ${pascal_case}Document } from '@savitri/collections/${camel_case}/${camel_case}.model'"
)

"""Used in index"""
PluginImportTemplate = Template(
r"import { api as ${capitalized}Module } from '$plugin_collection'"
)

PluginInstanceTemplate = Template(
r"${capitalized}Module(),"
)
