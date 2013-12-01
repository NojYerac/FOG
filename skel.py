#!/usr/bin/env python3
"""
~/bin/skel.py

SYNOPSIS:

A starting point for python scripts

OPTIONS:

enter some options here
"""

import os, os.path, sys
from glob import glob
from getopt import gnu_getopt

def failout(message):
    print(message, file = sys.stderr)
    usage()
    exit(1)

def usage():
    print(__doc__)

def main():
    failout(sys.argv[1:])
    

# TODO:
# IT'S A GOOD IDEA TO STATE OBJECTIVES, MAKE A CHECKLIST OR WRITE SOME
# PSUDOCODE HERE. A LITTLE PREPERATION GOES A LONG WAY!!!!!!!

if __name__ == '__main__':
    main()

    
