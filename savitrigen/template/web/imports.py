from string import Template

PluginImportTemplate = Template(
r"""import { web as ${capitalized}Module } from '$plugin_name'"""
)

PluginInstanceTemplate = Template(
r"""${capitalized}Module(),"""
)

LocaleImportTemplate = Template(
r"""${locale_key}: require('./i18n/${locale}/index.json'),"""
)
