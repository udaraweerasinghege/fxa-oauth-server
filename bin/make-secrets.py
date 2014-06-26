#!/usr/bin/env python

import os, sys, hashlib, json

# slightly paranoid: not using raw kernel /dev/urandom, but hashing it first
def make_random_hex(chars):
    assert (chars*4) <= 512
    return hashlib.sha512(os.urandom(512/8)).hexdigest()[:chars]

if len(sys.argv) < 2:
    print "Usage: make-secrets.py APPNAME"
    print " writes to APPNAME-private.json and APPNAME-public.json"
    print " give 'public' to the oauth server admin"
    print " keep 'private' secure on the app/Consumer server"
    sys.exit(0)
app_name = sys.argv[1]
assert "/" not in app_name
assert " " not in app_name

client_id = make_random_hex(16) # merely needs to be unique, not secret
client_secret = make_random_hex(32) # must actually be secret
hashed_secret = hashlib.sha256(client_secret).hexdigest() # note: hash of *hex*
# the client will submit (ascii/hex) client_secret over the wire, so that's
# what will get hashed for comparison

public = {
    "client_id": client_id,
    "hashed_secret": hashed_secret,
    }
private = {
    "client_id": client_id,
    "client_secret": client_secret,
    }

public_fn = "%s-public.json" % app_name
with open(public_fn, "w") as f:
    json.dump(public, f, indent=0)
    f.write("\n")
    print "wrote public (fxa-oauth-server) data to %s" % public_fn

private_fn = "%s-private.json" % app_name
with open(private_fn, "w") as f:
    json.dump(private, f, indent=0)
    f.write("\n")
    print "write private (app/Consumer) data to %s" % private_fn
