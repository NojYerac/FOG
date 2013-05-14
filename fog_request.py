#!/usr/bin/env python3
"""
USAGE:
fog_request.py [OPTIONS] [PHRASE]

SYNOPSIS:

Free & Open Government (FOG) is an app that generates reports & graphs
based on keywords.  It pulls data from the capitolwords.org API.

When executed directly, this script prints parsed json data directly to stdout.

OPTIONS:

-h --help, display docs

-c --cache-dir=CACHE_DIR, default is /tmp/cache/

-e --endpoint=ENDPOINT default is 'text.json'
 dates.json
 phrases.json
 phrases/{entity}.json {legislator|state|party|bioguide_id|volume|chamber}
 text.json

-k --api-key-file=PATH/TO/FILE, default is ./api.key

-u --url=BASE_URL, default is 'http://capitolwords.org/api/1'

STANDARD OPTIONS:

--state=ABBRV (i.e.: TX)

--party=R|D|I

--chamber=house|senate|extentions

--date=DATE (YYYY-MM-DD)

--start_date=DATE

--end_date=DATE

--json=PATH/TO/FILE.json (pass in additional val:arg pairs)

Read the full API spec at: http://capitolwords.org/api/1
"""

import os, os.path
import json
from hashlib import md5 as md5hash
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlencode
from fog_exceptions import FOG_AlreadyGotOneError

API_LOC = 'api.key' # Enter the file location of the api key file
CACHE_DIR = '/tmp/fog_cache'
BASE_URL, ENDPOINT = 'http://capitolwords.org/api/1', 'text.json'

class FOGRequest():
    def __init__(self, data, endpoint=ENDPOINT, base_url=BASE_URL, api_loc=API_LOC, cache_dir=CACHE_DIR):
        self.data = data
        with open(api_loc, 'rt') as apikey_file:
            self.apikey = apikey_file.read(32)
        self.cache_dir = cache_dir
        self.url = '%s/%s' % (base_url, endpoint)
        self.modifyData(apikey=self.apikey)
        self.urlEncodeData()
        
    def urlEncodeData(self):
        self.url_data = '%s?%s' % (self.url, urlencode(self.data))
        self.md5_digest = self.getHash()
        
    def modifyData(self, **new_data):
        self.data.update(new_data)
        self.urlEncodeData()
        
    def replaceAllData(self, **new_data):
        self.data = {'api_key':self.api_key}
        self.modifyData(new_data)
        
    def fetchResult(self):
        with request.urlopen(self.url_data) as reply:
            self.result = json.loads(reply.read().decode())

    def getHash(self):
        return md5hash(self.url_data.encode()).hexdigest()
        
    def request(self):
        """Only calls fetchResult if cache file doesn't exist.
        Then, reads/writes the json from/to cache_dir.
        Finally, returns the parsed json data."""
        cache_file_name = os.path.join(self.cache_dir, self.md5_digest)
        try:
            if os.path.isdir(self.cache_dir):
                if os.path.isfile(cache_file_name):
                    raise(FOG_AlreadyGotOneError())
            else: os.mkdir(self.cache_dir)
            self.fetchResult()
            with open(cache_file_name, 'wt') as cache_file:
                json.dump(self.result, cache_file)
        except FOG_AlreadyGotOneError:
            with open(cache_file_name, 'rt') as cache_file:
                self.result = json.load(cache_file)
        except HTTPError as err:
             message = """
            This request:
            %s
            
            Yeilded this error:
            %s
             """ % (self.url_data, err)
             failout(message)
        return self.result

#######################################
# TERMINAL FUNCTIONS BELOW THIS POINT #
#######################################
   
def failout(message):
    print(message, file = sys.stderr)
    usage()
    exit(1)

def usage():
    print(__doc__)

def main(data):
    return(FOGRequest(data).request())

if __name__ == '__main__':
    import sys
    from getopt import gnu_getopt
    from pprint import pprint
    try:
        opts, args = gnu_getopt(sys.argv[1:], 'c:e:hk:u:',
                                ['cache-dir=', 'endpoint=', 'api-key-file=',
                                 'help', 'url=', 'state=', 'party=', 'chamber=',
                                 'date=', 'start_date=', 'end_date=', 'json='])
    except GetOptError as err:
        failout(err)
    data = {}
    for o, a in opts:
        if opt in ('-c', '--cache-dir'):
            CACHE_DIR = a
        elif opt in ('-e', '--endpoint'):
            ENDPOINT = a
        elif opt in ('-h', '--help'):
            usage()
            exit(0)
        elif opt in ('-k', '--api-key-file'):
            API_LOC = os.path.expanduser(a)
        elif opt in ('--state', '--party', '--chamber',
                     '--date', '--start_date', '--end_date'):
            data[opt[2:]] = a
        elif opt == '--json':
            with open(os.path.expanduser(a), 'rt') as json_file:
                data.update(json.load(json_file))
    if args:
        data['phrase'] = ' '.join(args)

    pprint(main(data))

    
