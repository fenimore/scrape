#!/usr/bin/env python
"""
# Originally authored by Stephen Sekula (https://hub.polari.us/steve)
# Distributed under an Apache 2.0 license
#
# Modified to post listings for cheap computers on leboncoin in Paris
"""

import re
import sys
import os

from datetime import datetime

from pypump import PyPump, Client
from pypump.models.image import Image
from pypump.models.collection import Collection
from pypump.models.collection import Public
from pypump.models.person import Person
from pypump.exception import PyPumpException

import goodcorners.py


# Place the credentials below for the pump.io account
# These can be obtained by using: http://polari.us/dokuwiki/doku.php?id=navierstokes#a_simple_program_to_authenticate_pypump_against_your_pumpio_instance

client_credentials = ['XXX', 'XXX']
client_tokens = ['XXX', 'XXX']

# Webfinger for your account
webfinger = "goodcorners@hotpump.net"

# Important: define a log file that contains a list of activities to which
# we have already responded.
logfile_name = "cornerbot.activity.log"

def simple_verifier(url):
    print 'Go to: ' + url
    return input('Verifier: ') # they will get a code back


def reply(activity,my_reply):
    try:
        activity.obj.comment(my_reply)
    except PyPumpException:
        print "   ... PyPumpException - ERROR - I will try to get this request next time!"
        return False
        pass
        
    return True


# DEFINE FUNCTIONS


client = Client(
    webfinger,
    name="CornerBot",
    type="native",
    key=client_credentials[0], # client key
    secret=client_credentials[1] # client secret
)

# archive of activities I have already processed

process_log = open(logfile_name,'a+')

#while 1==1:
pump = PyPump(
    client=client,
    token=client_tokens[0], # the token key
    secret=client_tokens[1], # the token secret
    verifier_callback=simple_verifier
)


   
#    print "Sleeping until next cycle..."
#    time.sleep(300000000000)

process_log.close()
    


