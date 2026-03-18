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
parser = argparse.ArgumentParser(description="Refined CLI to open finder from Terminal")
parser.add_argument("file_path", nargs="*", default="", help="Path to open")

args = parser.parse_args()
# print(args)

# Get working dir, backup if path not provided
wd = sp.run("pwd", capture_output=True, text=True).stdout.strip()



# Helper functions
def error(msg):
    print(f"{RED}{msg}{RESET}", file=sys.stderr)
    sys.exit(1)

def grid_view(file_path):
    script = f'''
    osascript -e '
tell application "Finder"
    set target of Finder window 1 to POSIX file "{file_path}"
    set current view of Finder window 1 to icon view
    activate
end tell
'''
    sp.run(script, shell=True)
# Open dir in Finder (fd /path/to/a/dir or fd => fd working directory)
def open_dir(args, wd):
    if len(args.file_path) != 0:
        file_path = args.file_path[0]
        # Open dir if it's a dir
        if os.path.isdir(file_path):
            sp.run(["open", file_path])
            # grid_view(file_path)

        # Highlight it if it's a file
        elif os.path.isfile(file_path):
            sp.run(["open", "-R", file_path])
        # Not file, not dir, what is it?
        else:
            if not os.path.exists(file_path):
                error(f"File '{file_path}' does not exist")
            pass
    else:
        sp.run(["open", wd])

open_dir(args, wd)

# else:
#     for i in range(len(sys.argv) - 1):
#         print(sys.argv[i])