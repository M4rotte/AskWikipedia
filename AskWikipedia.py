#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.parse
import urllib.request
import json
import re

try:
	search = sys.argv[1]
except IndexError:
    print("Needs a string as argument. Exiting…")
    exit(1)

data = {}
data['format'] = 'json'
data['action'] = 'query'
data['prop'] = 'extracts'
data['exlimit'] = 'max'
data['explaintext'] = ''
data['titles'] = search
data['redirects'] = ''
data['utf8'] = ''

filters = []
s_filters = ('^(==|===|====)( )(.*)( )(==|===|====)$',\
             '^(.*)\((ISBN)([ 0-9\-])+(\)| )(.*)$',\
             '^Référence (.*) (\()(.+)(\))$',\
             '^\([a-z]{2}\) (.*)$',\
             )
           
for filter in s_filters:
    filters.append(re.compile(filter))

url_values = urllib.parse.urlencode(data)
url = 'http://fr.wikipedia.org/w/api.php'
full_url = url + '?' + url_values


# proxy = urllib.request.ProxyHandler({'http': r'http://user:*****@server:port',
#                                      'https': r'http://user:*****@server:port',})
# auth = urllib.request.HTTPBasicAuthHandler()
# opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
# urllib.request.install_opener(opener)

response = urllib.request.urlopen(full_url)
json = json.loads(response.read().decode("utf8"))


for page in json['query']['pages'].values():

    try:
        content = page['extract']
    except KeyError:
        print("'"+search+"' not found !", file=sys.stderr)
        exit(1)
        
    print("Reading: "+search+" ("+str(len(page['extract']))+")", file=sys.stderr)
    content = page['extract']
    content = content.replace("\n\n","\n")
    
    for line in content.split("\n"):
        for regexp in filters:
            discard = regexp.match(line)
            if (discard):
                break
            else:
                continue
        if (discard or not line):
            continue
        line = line.strip()    
        print(line)        

