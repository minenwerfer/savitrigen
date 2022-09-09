from string import Template

IndexTemplate = Template(
r"""import { init } from '@savitri/api/server'

${module_imports}

const provide = ${provide}

const modules = [
${module_instances}
]

init({ provide, modules })
    .then(server => server.start())
"""
)
