#!/usr/bin/env python
from flask import Flask, render_template, request, redirect
import socket
import json
import os
import re
app = Flask(__name__)

DOMAIN = 'ff-hh.net'
ABUSE = 'rm-pls@hamburg.freifunk.net'
DB = 'db/'

kwargs = dict(domain=DOMAIN, abuse=ABUSE)


@app.route('/')
def index():
    return render_template('index.html', **kwargs)


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    ipv6 = request.form['ipv6']

    if not re.match('^[a-z0-9]+$', name):
        return 'name rejected'

    with open('blacklist.txt') as f:
        blacklist = [x.strip() for x in f if x.strip()]

    if name in blacklist:
        return 'name is blacklisted'

    if os.path.exists(os.path.join(DB, name)):
        return 'name exists'

    try:
        socket.inet_pton(socket.AF_INET6, ipv6)
    except socket.error:
        return 'invalid ipv6'
    else:
        with open(os.path.join(DB, name), 'w') as f:
            json.dump({'name': name, 'ipv6': ipv6}, f)

        return redirect('/done')


@app.route('/done')
def done():
    return render_template('done.html', **kwargs)


if __name__ == '__main__':
    app.run(port=5001)
