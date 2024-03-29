from string import Template

ControllerTemplate = Template(
r"""import { Mutable } from '@savitri/api'
import { ${model_pascal_case}Document, ${model_pascal_case} } from '${model_path}'
import { default as Description } from './index.json'

/**
    @remarks Generated by savitrigen v${savitrigen_version}
    @copyright ${copyright}
    ${documentation}
*/

export class ${pascal_case}Controller extends Mutable<${model_pascal_case}Document> {
  constructor() {
    super(${model_pascal_case}, Description)
  }
}
""")

