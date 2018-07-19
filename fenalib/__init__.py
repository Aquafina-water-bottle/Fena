"""
General random notes:
    - in general, this is all python valid code

 cmd line      in file (overrides config.py)         config.py
fena.py -v    !pcfg version = "1.12"                version = "1.12"
fena.py -s    !pcfg simple = True                   simple = True

 cmd line      in file (overrides config.py)         config.py
              !cfg output = ""                      output = ""
fena.py -d    !cfg debug = True                     debug = False
fena.py -c    !cfg clean = True                     clean = False
fena.py -e    !cfg ego = True                       ego = True
fena.py -l    !cfg debug_log = True                 debug_log = False
              !cfg plugin_cmds = {"a", "b", "c"}    plugin_cmds = {"tp", "weather", "gamemode"}
              !cfg leading_cmds = {"a", "b", "c"}   leading_cmds = {"execute"}
              !cfg leading_cmds |= {"a"}
              !cfg leading_cmds |= {"a", "b", "c"}

!pcfg version = "1.12"; simple = True

!cfg:
    debug = True
    clean = False

# whether this is used as a part of ego (edgegamers organization) or not
# this should be set to false unless you actually are using this for the ego event server
ego=true

# all commands that can be put before a regular command
# might be removed soon
leading_commands=execute

# any commands that require "minecraft:" before it due to conflicts with plugins
plugin_conflict_commands=tp,weather,gamemode
"""

