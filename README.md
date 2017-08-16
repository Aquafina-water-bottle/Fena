Command Compiler Unlimited (CCU), a spiritual successor to Command Block Parser (CBP), is a minecraft scripting language that will make understand large numbers of commands easier while being extremely flexibile to cater to any individual's command needs. However, just like CBP, this adds an extra layer of complexity to working with commands, and this will have no checks on whether a command is supposed to work or not.

A random feature list in no particular order:
* support for command blocks (groups, conditional, combiners) with either relative or direct coordinates
* general mcfunction support (nicknames and file encapsulation visualized by number of tab spaces)
* scoreboard, execute, selector and function shortcuts
* variables (normal, functions and arrays) with general coordinate manipulation support and parameter support
* files for parsed commands, setblock commands and combiner commands
* server support to prevent kicking the player when using combiners
* adding 'minecraft:' over certain commands if plugins are used
* support for minecraft versions between 1.10 and 1.12
* support for including custom plugin commands if necessary under the config file
* basic math (`%, ^, *, /, -, +` as operators, `SIN, COS, TAN, LOG, LOG10` functions with integer and double support)
* easy conversion between decimals and integers, including library entrys to always round up/down
* if/else/elif statements and for loops that works with either strings or numbers
* general rcon support (although it's really horrible imo)
* combining lines in various different ways
* comments & comment blocks
* various ways of importing different files
* a built in library that will be expanded heavily as time goes by (already has lists, easy install / uninstall arrays for objectives and teams, etc.)

P.S. I lied about it compiling. It's more like a text interpreter. I don't know how to name programs or use terms properly. Deal with it.
