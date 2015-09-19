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

client_credentials = []
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
todays_corners = []
listing = ""
header = ""

#process_log = open(logfile_name,'a+')

while 1==1:
    time = str(datetime.now())
    header += time + " - Paris - " 
    """
        Gather the Le bon Coin Annonces
        for thinkpads entre 40 et 200 euros
    """
    corners = Corner.get_recent_corners('http://www.leboncoin.fr/informatique/offres/ile_de_france/?ps=4&pe=8&q=thinkpad&th=1')
    for corner in corners:
        # Set up HTML Styled Posting for Pump.io
        listing += "<table><tr><td><img src=" + corner['image'] + " width=100px height=auto/></td><td><b>" + corner['titre'] + "</b><br><a href=" + corner['url'] + " >Annonce</a> " + corner['location']+" pour " + corner['prix'] + "<br>" + corner['date'] +"</td></tr></table>" 
        listing += "<br>"
        header += corners[x]['prix']
    """
        Remove the postings which the
        Cornerbot has already posted
    """
    for corner in corners:
        if corner in todays_corners:
            corners.remove(corner)
            print("found one duplicate")    
    """
        If there are not 0 new postings
        Post to pump.io
    """
    if not not corners:
        posting = pump.Note(listing, header)
        posting.to = pump.Person("polypmer@microca.st")
        posting.send()
        print("posting " +time)
    else:
        print("No new items")
    # Finished Post
    listing = ""
    header = ""
    todays_corners.append(corners)
    print("TODAYS CORNERS:")
    print(todays_corners)
    print("\n\n####CORNERS:\n\n")
    print(corners)
    print("\n\nSleep Now")
    time.sleep(3000)

#process_log.close()
    
    """
    for x in range(2):
        listing += "<table><tr><td><img src=" + corners[x]['image'] + " width=100px height=auto/></td><td><b>" + corners[x]['titre'] + "</b><br><a href=" + corners[x]['url'] + " >Annonce</a> " + corners[x]['location']+" pour " + corners[x]['prix'] + "<br>" + corners[x]['date'] +"</td></tr></table>" 
        listing += "<br>" 
        # "<br><b>" + corner['titre'] + "</b><br><img src=" + corner['image'] + " width=30px height=auto/><br><a href=" + corner['url'] + " >Annonce</a> " + corner['location']+" pour " + corner['prix'] + "<br><br>"  
        """ 


