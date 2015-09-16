#!/usr/bin/env python
#  Copyright 2014, Stephen Jacob Sekula
# http://polari.us/dokuwiki/doku.php?id=navierstokes#a_simple_program_to_authenticate_pypump_against_your_pumpio_instance
# modified to take arguements, and work with python3

from pypump import PyPump, Client
import sys
"""
arg 1 webfinger
arg 2 client name
"""
client = Client(
    webfinger=sys.argv[1],
    type="native", # Can be "native" or "web"
    name=sys.argv[2]
)

def simple_verifier(url):
    print('Go to: ' + url)
    return input('Verifier: ') # they will get a code back

pump = PyPump(client=client, verifier_callback=simple_verifier)
client_credentials = pump.get_registration() # will return [<key>, <secret>, <expirey>]
client_tokens = pump.get_token() # [<token>, <secret>]

print("client_credentials: %s,%s" % (client_credentials[0],client_credentials[1]))
print("client_tokens: %s,%s" % (client_tokens[0],client_tokens[1]))
