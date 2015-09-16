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
from pypump.models.collection import Collection
from pypump.models.collection import Public
from pypump.models.person import Person
from pypump.exception import PyPumpException

from goodcorner import Corner

"""
     Place the credentials below for the pump.io account
     These can be obtained by using: http://polari.us/dokuwiki/doku.php?id=navierstokes#a_simple_program_to_authenticate_pypump_against_your_pumpio_instance
      or use the get_credentials script for python 3
"""

client_credentials = ['hugs', 'kisses']
client_tokens = ['puppies', 'kittens'] # These don't go anywhere, but steve had them

# Webfinger for your account
webfinger = "goodcorners@hotpump.net"

# Important: define a log file that contains a list of activities to which
# we have already responded.
#logfile_name = "cornerbot.activity.log"

def simple_verifier(url):
    print('Go to: ' + url)
    return input('Verifier: ') # they will get a code back
    
"""
    Functions for leboncoin
"""

client = Client(
    webfinger,
    name="CornerBot",
    type="native",
    key=client_credentials[0], # client key
    secret=client_credentials[1] # client secret
)

# archive of activities I have already processed

#process_log = open(logfile_name,'a+')

#while 1==1:
pump = PyPump(
    client=client,
    #token=client_tokens[0], # the token key NOT NEEDED?
    #secret=client_tokens[1], # the token secret NOT NEEDED?
    verifier_callback=simple_verifier
)


#posting.send()
# gather the listings
# and format the most recent three
# and add their prices to the note total
corners = Corner.get_recent_corners('http://www.leboncoin.fr/informatique/offres/ile_de_france/?ps=4&pe=8&q=thinkpad&th=1')
listing = ""
header = ""
for corner in corners:
    listing += corner['titre'] + "\n" + corner['url']+ "\n\n\n"
    header += corner['prix'] #header = corners[0]['prix'] + corners[1]['prix']  + "et " + corners[2]['prix']
posting = pump.Note(listing, header)
posting.send()
print(listing + header)
# + " pour " + corners[0]['price'] + " à " + corners[0]['location'] + "\n "
   
#    print "Sleeping until next cycle..."
#    time.sleep(300000000000)

#process_log.close()
    


