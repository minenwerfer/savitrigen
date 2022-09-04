from string import Template

ModuleIndexTemplate = Template(
r"""import routerExtension from './router'

export default () => ({
  routerExtension
})
""")

IndexTemplate = Template(
r"""import { useApp } from '@savitri/web'
import { SvMain } from '@savitri/components'

${module_imports}

import DashboardModule from './modules/dashboard'

const options = {
  component: SvMain,
  modules: [
${module_instances}
    DashboardModule()
  ],
  i18n: {
    locale: '${default_locale}',
    messages: {
${locale_imports}
    ...require('./i18n/pt_BR/index.json')
    }
  },
  menuSchema: ${menu_schema}
}

useApp(options).then(({ app }) => {
  app.mount('#app')
})
""")

