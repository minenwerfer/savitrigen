from string import Template

RouterTemplate = Template(
r"""import { RouterExtension } from '@savitri/web'

export const routerExtension: RouterExtension = {
  //
}
""")


DashboardRouterTemplate = Template(
r"""import { RouterExtension } from '@savitri/web'

export default {
  'dashboard': {
    'dashboard-home': {
      path: 'home',
      component: () => import('./views/home.vue'),
      meta: { title: 'Início' }
    }
  }
} as RouterExtension
""")
