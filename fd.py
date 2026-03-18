#!/usr/bin/env python3 

import sys
import os
import subprocess as sp
import argparse
from pathlib import Path

# Constants
RED = "\033[31m"
RESET = "\033[0m"

# Setup arguments
parser = argparse.ArgumentParser(description="Refined CLI to open Finder from Terminal")
parser.add_argument("file_path", nargs="*", default="", help="Path of the directory to open, or path of file to highlight in Finder")
parser.add_argument("-i", action="store_true", help="Sets view mode to icons mode")
parser.add_argument("-l", action="store_true", help="Sets view mode to list mode")
parser.add_argument("-c", action="store_true", help="Sets view mode to columns mode")
# Gallery view is not supported by AppleScript, blame Apple.
# parser.add_argument("-g", action="store_true", help="Sets view mode to gallary mode")
args = parser.parse_args()
print(args)

# Get working dir, backup if path not provided
cwd = sp.run("pwd", capture_output=True, text=True).stdout.strip()



# Helper functions
def error(msg):
    print(f"{RED}{msg}{RESET}", file=sys.stderr)
    sys.exit(1)

# Opens dir based on view args
def open_dir(file_path, args):
    if args.i:
        display_option = "icon"
    elif args.l:
        display_option = "list"
    elif args.c:
        display_option = "column"

    # Gallery view is not supported by AppleScript, blame Apple
    # elif args.g:
    #     display_option = "gallery"
    # If no display arguments are passed through, just open it dir
    else:
        sp.run(["open", file_path])
        return
    
    # If arguments are passed, this runs
    print(display_option)
    script = f'''
    tell application "Finder"
        set theFolder to POSIX file "{file_path}" as alias
        open theFolder
        set current view of window 1 to {display_option} view
        activate
    end tell
    '''
    sp.run(["osascript", "-e", script])

# Handles arguments and directs it to functions
def base_handler(args, cwd):

    # If file path is provided, else give cwd
    if len(args.file_path) != 0:
        file_path = args.file_path[0]
    else:
        file_path = cwd

    # Open dir if it's a dir
    if os.path.isdir(file_path):
        open_dir(file_path, args)
    # Highlight it if it's a file
    elif os.path.isfile(file_path):
        sp.run(["open", "-R", file_path])
    # Raise error if nonexist
    elif not os.path.exists(file_path):
            error(f"File '{file_path}' does not exist")
    else:
        error("Unknow error occurred... Consider reporting this to https://github.com/zibuyin/term2finder/issues")

base_handler(args, cwd)

# else:
#     for i in range(len(sys.argv) - 1):
#         print(sys.argv[i])