from string import Template

"""Unused"""
ComponentTemplate = Template(
r"""<template>
</template>

<script setup lang="ts">
import { useStore } from '@savitri/web'

const store = useStore('${name}')
</script>
""")

DashboardHomeComponentTemplate = Template(
r"""<template>
  <sv-prose class="tw-mt-4">
    <template #title>Parabéns</template>
    <ul class="
        tw-flex
        tw-flex-col
        tw-gap-y-3
        tw-list-disc
        tw-pl-4
    ">
      <li
        v-for="(item, index) in items"
        v-html="item"
        :key="`item-$${index}`"
      />
    </ul>
  </sv-prose>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { SvProse } from '@savitri/components'

const productName = inject('productName')
const baseVersion = inject('baseVersion')

const items = [
  'Você configurou um projeto com sucesso',
  'Nome do projeto : ' + productName,
  'Versão do Savitri: ' + baseVersion
]
</script>
""")
