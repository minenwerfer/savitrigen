savitrigen
==========

Savitri Project's official code generation tool.

Usage
=====
Once installed, savitrigen will become available as a Python executable module.
You can call it by running `python -m savitrigen [options]`

Behavior
========
Savitrigen will look for `source/.gitignore` to check if the bootstrap repository has already been cloned. If it hasn't already, savitrigen will then clone it inside `source` folder. In the next step it will check if npm modules has already been installed then install it if it hasn't. Thus savitrigen will skip the cloning/installation steps in consecutive runs.

Savitrigen will then produce the project scaffolding according to `briefing.yml`. If it isn't being run for the first time, it'll overwrite existing files and leave extra files untouched. At the moment there's not a cleanup routine (for safety reasons), so if a entity is removed from `briefing.yml` then savitrigen is run for a second time then this entity residual files will remain and will have to be manually removed.
