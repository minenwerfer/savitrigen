from string import Template

IndexTemplate = Template(r"""
export * from './router'
export * from './store'
""")

RouterTemplate = Template(r"""
import { RouterExtension } from 'frontend/router'

export const routerExtension: RouterExtension = {
  //
}
""")

StoreTemplate = Template(r"""
import { StoreExtension } from 'frontend/store'

export const storeExtension: StoreExtension = {
  //
}
""")

ComponentTemplate = Template(r"""
<template>
</template>

<script setup lang="ts">
import {
  toRefs
} from 'vue'

import { useStore } from 'vuex'
import { useModule } from 'frontend/composables'

const store = useStore()
const moduleRefs = reactive(useModule('${name}', store))

const {
  item,
  items

} = toRefs(moduleRefs)
</script>
""")
