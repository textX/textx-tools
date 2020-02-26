# textx-tools

**DEPRECATED** by textX and textX-dev projects.

The developer tool infrastructure for [textX](https://github.com/igordejanovic/textX).

The main idea is to separate development tooling from the textX runtime.  This
way core textX library will be kept to its minimum in terms of dependencies
and code size.

This tool is pluggable. You can define your own subcommands. See `setup.py`.

# For what it is used?

 - textX project scaffolding (three types of projects: language, generator,
   application)
 - Meta-model (grammar) and models visualization
 - Meta-model (grammar) and model checking
 - Running code generation process.

# Installation

This tool is in early stage of development so development version must be used
at the moment. Also, you must first install textX from master branch.
    
    $ pip install --upgrade https://github.com/igordejanovic/textX/archive/master.zip
    $ pip install --upgrade https://github.com/igordejanovic/textx-tools/archive/master.zip

I highly suggest you to use [virtualenv](https://virtualenv.pypa.io/) as it
enables easy creation of isolated environments.

# Quick intro

Getting general help:

    $ textx --help

    Usage: textx [OPTIONS] COMMAND [ARGS]...

    textx developer tools

    Options:
    --help  Show this message and exit.

    Commands:
    list-langs    Lists registered textX languages.
    list-gens     Lists registered textX code generators.
    startproject  Generates scaffolding for textX projects.
    vis           Visualize (meta)model using dot.
    generate      Runs source code generator.
    check         Checks (meta)model syntax validity.

Getting help on subcommand:

    $ textx vis --help
    Usage: textx vis [OPTIONS] MODEL_FILE

    Visualize (meta)model using dot.

    Options:
    -l, --language TEXT  Registered language name. Default is "textx" - for
                        textX grammars.
    -d, --debug          run in debug mode
    --help               Show this message and exit.

Create language project:

    $ textx startproject -t lang mylang
    Generating language project "mylang" in folder "textx-lang-mylang".
    Creating README.md
    Creating mylang/__init__.py
    Creating setup.py
    Creating mylang/lang.py
    Creating mylang/mylang.tx
    Done.

Install language project in development mode:

    $ pip install -e textx-lang-mylang

Create generator project for mylang language:

    $ textx startproject -t gen -l mylang angularjs
    Generating generator project "angularjs" in folder "textx-gen-mylang-angularjs".
    Creating README.md
    Creating mylang_angularjs/mylang_angularjs.genconf
    Creating mylang_angularjs/__init__.py
    Creating mylang_angularjs/templates/hello.html
    Creating setup.py
    Creating mylang_angularjs/gen.py
    Done.

Install generator project in development mode:

    $ pip install -e textx-gen-mylang-angularjs

List registered languages:

    $ textx list-langs -v
    genconf - textx-tools 0.1 (/home/igor/Projekti/GitHub/textx-tools)
        Language for generators configuration.
    mylang - textx-lang-mylang 0.1 (/home/igor/tmp/textx-lang-mylang)
        mylang language.

List registered generators:

    $ textx list-gens -v
    mylang_angularjs (mylang) - textx-gen-mylang-angularjs 0.1 (/home/igor/tmp/textx-gen-mylang-angularjs)
        angularjs generator for mylang language

Create application project:

    $ textx startproject myapp
    Generating app project "myapp" in folder "myapp".
    Creating README.md
    Creating src/.keep
    Creating model/mymodel.er
    Creating templates/README.md
    Creating genconf/er_flask.genconf
    Creating README.md
    Done.

**Read generated `README.md` for each type of project to get you started.**

# Workflow

- Design your language in the the language project. Use check and vis commands
  during development.
- Implement your generator in the generator project. Write code templates and
  genconf generator configurations.
- Use your language to write application model in the application project.
  Configure generators (at least specify models). If needed do templates and
  rules override.
- Generate code using 'textx generate' command.
- To support manual changes to the generated code generate code on a dedicated
  git branch. Merge with the development branch.

In general, language and generator development should be done by language
designer team members. Application developers use languages to make models,
generate code and do manual changes to the code.


# TODO

- Tests
- Documentation
- Examples. Currently [ER
  language](https://github.com/igordejanovic/textx-lang-er) and
  [flask](https://github.com/igordejanovic/textx-gen-er-flask) and angularjs
  generators for the ER language are in the development. Still in early stage.

