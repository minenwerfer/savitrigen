from string import Template

IndexTemplate = Template(
r"""import { init } from '@savitri/api/server'

${module_imports}

const config = {
  modules: [
${module_instances}
  ]
}

init(config)
    .then(server => server.start())
"""
)