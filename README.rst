savitrigen
==========
Savitri Project's official code generation tool.

Usage
=====
Once installed, savitrigen will become available as a Python executable module.
You can call it by running `python -m savitrigen [options]`.

To get started, list available presets with `python -m savitrigen -l`, then choose one with `python -m savitrigen -p [preset]`. This will create a `savitrigen.yml` file in your current working directory. To parse it run savitrigen without any options, like `python -m savitrigen`. That's pretty much the CLI usage.

Behavior
========
Savitrigen will look for `source/.gitignore` to check if the bootstrap repository has already been cloned. If it hasn't already, savitrigen will then clone it inside `source` folder. In the next step it will check if npm modules has already been installed then install it if it hasn't. Thus savitrigen will skip the cloning/installation steps in consecutive runs.

A diff-patch algorithm is used to update the code without touching external changes. It's nonetheless advisable to commit changes before rerunning the code generation.
