# {{project_name}}

TODO: Write project description.

This is textX code generator project scaffolding. Generators are specified for
a particular textX language.  This one uses `{{language}}` language.

Generator templates are stored in `{{package_name}}/templates` folder.
They are referenced by the genconf model in
`{{package_name}}/{{package_name}}.genconf`.
By default, [Jinja2](http://jinja.pocoo.org/) template engine is used but you
can change that.
Generator registration and template rendering function can be found in
`{{package_name}}/gen.py`

This generator is registered in setuptools entry point `textx_gen` inside
setup.py. After installation it will be visible to the textx tool.

It is recommended to install this project in the development mode for
development.

To do that run this from the project folder:

    $ pip install -e .

This command will list all registered generators:

    $ textx list-gens


To test generator create textX app project:

    $ textx startproject myproject


and make genconf in that project under `genconf` folder with the name
`{{package_name}}.genconf` and the {{langauge}} model in `model` folder.
Reference your model from the genconf.

Use:

    $ textx generate

from your app project to generate code.

By all means, you should be using
[virtualenv](https://github.com/pypa/virtualenv).


