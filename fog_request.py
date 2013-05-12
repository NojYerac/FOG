#!/usr/bin/env python3
"""
fog_request.py

SYNOPSIS:

Free & Open Government (FOG) is an app that generates reports & graphs
based on keywords.  It pulls data from the capitolwords.org API.

OPTIONS:

-a --api-key-file=PATH/TO/FILE


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
# 
#
# IT'S A GOOD IDEA TO STATE OBJECTIVES, MAKE A CHECKLIST OR WRITE SOME
# PSUDOCODE HERE. A LITTLE PREPERATION GOES A LONG WAY!!!!!!!

if __name__ == '__main__':
    main()

    
