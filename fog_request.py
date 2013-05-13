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
import pickle
from hashlib import md5 as md5hash
from urllib import request
from urllib.parse import urlencode
from fog_exceptions import FOG_AlreadyGotOneError

API_LOC = 'api.key' # Enter the file location of the api key file
CACHE_DIR = '.cache'

class FOGRequest():
    def __init__(self, data, endpoint='http://capitolwords.org/api/text.json', API_LOC=API_LOC):
        self.data = data
        self.endpoint = endpoint
        with open(API_LOC, 'rt') as apikey_file:
            self.apikey = apikey_file.read(32)
        self.modifyData(apikey=self.apikey)
        self.urlEncodeData()
    def urlEncodeData(self):
        self.url_data = urlencode(self.data).encode()
        self.getHash()
    def modifyData(self, **new_data):
        self.data.update(new_data)
        self.urlEncodeData()
    def replaceAllData(self, **new_data):
        self.data = {'api_key':self.api_key}
        self.modifyData(new_data)
    def __fetchResult(self):
        self.result = request.openurl(self.endpoint, self.url_data)
    def getHash(self):
        self.md5_digest = md5hash(self.url_data).hexdigest()
    def request(self):
        cache_file_name = os.path.join(self.cache_dir, self.md5_digest)
        try:
            if os.path.isdir(self.cache_dir):
                if os.path.isfile(cache_file_name):
                    raise(FOG_AlreadyGotOneError())
            else: os.mkdir(self.cache_dir)
            self.fetchResult()
            with open(cache_file_name, 'wb') as cache_file:
                pickle.dump(self.result, cache_file)
        except FOG_AlreadyGotOneError:
            with open(cache_file_name, 'rb') as cache_file:
                self.result = pickle.load(cache_file)
            
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
from getopt import gnu_getopt

    main()

    
