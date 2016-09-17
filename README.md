# textx-tools

The developer tool infrastructure for textX.

The main idea is to separate development tooling from the textX runtime.  This
way core textX library will be kept to its minimum in terms of dependencies
and code size.

This project will be in charge to provide a command line interface to various
textX commands (e.g. textX project scafolding, visualization, model checking,
code generation).  This library is used during the development process.

Code generators and various DSLs will be plugins to this framework.
