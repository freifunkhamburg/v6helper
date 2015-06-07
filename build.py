#!/usr/bin/env python
from glob import glob
import json
import os

DOMAIN = 'ff-hh.net'
OUT = '/etc/nginx/v6helper.d/'

template = '''
server {
    listen 80;
    listen [::]:80;

    server_name %%s.%s;

    access_log off;
    error_log /dev/null crit;

    location / {
        proxy_pass http://[%%s];
        include /etc/nginx/proxy_params;
    }
}
''' % DOMAIN

for path in glob('db/*'):
    with open(path) as f:
        x = json.load(f)
    with open(os.path.join(OUT, x['name']), 'w') as f:
        f.write(template % (x['name'], x['ipv6']))
