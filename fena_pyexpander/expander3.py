#!c:\python36\python.exe
# -*- coding: UTF-8 -*-
"""
expander.py: this is the pyexpander application.

NOTE: THIS IS A MODIFIED VERSION OF PYEXPANDER as of July 2018
License: https://bitbucket.org/goetzpf/pyexpander/src/b466de6fd801545650edfa790a18f022dc7e151a/LICENSE?at=default&fileviewer=file-view-default
Original: http://pyexpander.sourceforge.net/
"""

# pylint: disable=C0322,C0103,R0903

from optparse import OptionParser
#import string
import os.path
import sys

if __name__ == "__main__":
    sys.path.append("..")

import fena_pyexpander.lib as pyexpander

# version of the program:
__version__= "1.8.3" #VERSION#

assert __version__==pyexpander.__version__

def process_files(options,args):
    """process all the command line options."""
    my_globals={}
    if options.eval is not None:
        for expr in options.eval:
            # pylint: disable=W0122
            exec(expr, my_globals)
            # pylint: enable=W0122
    filelist= []
    if options.file is not None:
        filelist= options.file
    if len(args)>0: # extra arguments
        filelist.extend(args)
    if len(filelist)<=0:
        pyexpander.expandFile(filename=None,
                              external_definitions=my_globals,
                              allow_nobracket_vars=options.simple_vars,
                              auto_continuation=options.auto_continuation,
                              auto_indent=options.auto_indent,
                              include_paths=options.include,
                              auto_indent_python=options.auto_indent_python,
                              no_stdin_warning=options.no_stdin_msg)
    else:
        for f in filelist:
            # all files are expanded in a single scope:
            my_globals= \
                pyexpander.expandFile(filename=f,
                                      external_definitions=my_globals,
                                      allow_nobracket_vars=options.simple_vars,
                                      auto_continuation=options.auto_continuation,
                                      auto_indent=options.auto_indent,
                                      auto_indent_python=options.auto_indent_python,
                                      include_paths=options.include)

def script_shortname():
    """return the name of this script without a path component."""
    return os.path.basename(sys.argv[0])

def print_summary():
    """print a short summary of the scripts function."""
    print(("%-20s: a powerful macro expension language "+\
           "based on python ...\n") % script_shortname())

def main():
    """The main function.

    parse the command-line options and perform the command
    """
    # command-line options and command-line help:
    usage = "usage: %prog [options] {files}"

    parser = OptionParser(usage=usage,
                          version="%%prog %s" % __version__,
                          description="expands macros in a file "+\
                                      "with pyexpander.")

    parser.add_option("--summary",
                      action="store_true",
                      help="Print a summary of the function of the program.",
                     )
    parser.add_option("-f", "--file",
                      action="append",
                      type="string",
                      help="Specify a FILE to process. This "
                           "option may be used more than once "
                           "to process more than one file but note "
                           "than this option is not really needed. "
                           "Files can also be specified directly after "
                           "the other command line options. If not given, "
                           "the program gets it's input from stdin.",
                      metavar="FILE"
                     )
    parser.add_option("--eval",
                      action="append",
                      type="string",
                      help="Evaluate PYTHONEXPRESSION in global context.",
                      metavar="PYTHONEXPRESSION"
                     )
    parser.add_option("-I", "--include",
                      action="append",
                      type="string",
                      help="Add PATH to the list of include paths.",
                      metavar="PATH"
                     )
    parser.add_option("-s", "--simple-vars",
                      action="store_true",
                      help="Allow variables without brackets.",
                     )
    parser.add_option("-a", "--auto-continuation",
                      action="store_true",
                      help="Assume '\' at the end of lines with commands",
                     )
    parser.add_option("-i", "--auto-indent",
                      action="store_true",
                      help="Automatically indent macros.",
                     )
    parser.add_option("-p", "--auto-indent-python",
                      action="store_true",
                      help="Automatically indent python output.",
                     )
    parser.add_option("--no-stdin-msg",
                      action="store_true",
                      help= "Do not print a message on stderr when the "
                            "program is reading it's input from stdin."
                     )

    # x= sys.argv
    (options, args) = parser.parse_args()
    # options: the options-object
    # args: list of left-over args

    if options.summary:
        print_summary()
        sys.exit(0)

    process_files(options,args)
    sys.exit(0)

if __name__ == "__main__":
    main()

