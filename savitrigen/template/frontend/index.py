from string import Template

ModuleIndexTemplate = Template(
r"""export * from './router'
import * as router from './router'
import * as store from './store'

export default () => ({
  ...router,
  ...store
})
""")

IndexTemplate = Template(
r"""import { useApp } from '@savitri/frontend'
import { SvMain } from '@savitri/components'

${module_imports}

import InternalModule from './modules/internal'

const options = {
  component: SvMain,
  modules: [
${module_instances}
    InternalModule()
  ],
  i18n: {
    locale: '${default_locale}',
    messages: {
${locale_imports}
    ...require('./i18n/pt_BR/index.json')
    }
  },
  menuSchema: {
    'Início': {
      children: [
${menu_entries}
      ]
    },
    'Schemauração': {
      children: [
        'dashboard-accessProfile',
        'dashboard-user',
      ]
    }
  }
}

useApp(options).then(({ app }) => {
  app.mount('#app')
})
""")

