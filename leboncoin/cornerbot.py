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
import time

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

client_credentials = 
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
b_set = set() # the B set is TODAYS postings
listing = ""
header = ""

#process_log = open(logfile_name,'a+')

while 99==99:
    print("\n\ninitiating\n\n")
    timestamp = str(datetime.now())
    header += timestamp + " - Paris - " 
    """
        Gather the Le bon Coin Annonces
        for thinkpads entre 40 et 200 euros
    """
    # a list of tuples of todays postings
    corners = Corner.get_recent_corners('http://www.leboncoin.fr/informatique/offres/ile_de_france/?ps=4&pe=8&q=thinkpad&th=1')
    """
        Remove the postings which the
        Cornerbot has already posted
        This requires all sorts of funny business
        a_set = Most recent scrape
        b_set = today's scrapes
        c_set = the annonces not yet posted by cornerbot
    """
    a_set = set() # Add the tuples to a Set
    for corner in corners:
        tup = tuple(sorted(corner.items()))
        a_set.add(tup)
        
    c_set = a_set - b_set
    b_set = a_set
    print("\nUnique items")
    print(len(list(c_set)))
    print("\n Todays itmes")
    print(len(list(b_set)))    
    """
        If there are not 0 new postings
        Post to pump.io
    """
    corners_pub = [dict(x) for x in list(c_set)] # sweet combobulator!!
    
    if corners_pub: # if there exists new items (from a - b )
        for corner in corners_pub:
            # Set up HTML Styled Posting for Pump.io
            listing += "<table><tr><td><img src=" + corner['image'] + " width=100px height=auto/></td><td><b><a href=" + corner['url'] + ">"+ corner['titre'] + "</a></b><br><a href=" + corner['url'] + " >Annonce</a> " + corner['location']+" pour " + corner['prix'] + "<br>" + corner['date'] +"</td></tr></table>" 
            listing += "<br>"
            header += corner['prix']
            print("\nwrote listing")
            print("...   "+ corner['titre'])
        posting = pump.Note(listing, header)
        posting.to = pump.Person("polypmer@microca.st")
        #posting.send()
        print("posting " +timestamp)
        print(todays_corners)
    else:
        print("no new corners\n\n\n")
    # Finished Post
    listing = ""
    header = ""
    print("TODAYS CORNERS:")
    print(todays_corners)
    print("\n\n####CORNERS:\n\n")
    print(new_corners)
    todays_corners.append(new_corners)
    print("\n\nSleep Now")
    time.sleep(3)

#process_log.close()
    
    """
    for x in range(2):
        listing += "<table><tr><td><img src=" + corners[x]['image'] + " width=100px height=auto/></td><td><b>" + corners[x]['titre'] + "</b><br><a href=" + corners[x]['url'] + " >Annonce</a> " + corners[x]['location']+" pour " + corners[x]['prix'] + "<br>" + corners[x]['date'] +"</td></tr></table>" 
        listing += "<br>" 
        # "<br><b>" + corner['titre'] + "</b><br><img src=" + corner['image'] + " width=30px height=auto/><br><a href=" + corner['url'] + " >Annonce</a> " + corner['location']+" pour " + corner['prix'] + "<br><br>"  
        
        
            new_corners = [] # can't remove from list I am iterating over.
    if todays_corners:
        for item in corners:
            if item not in corners:
                new_corners.append(item)
                print("Unique")
                continue
            else:
                print("unique\n") 
                print("...   "+ item['titre'])
                continue
        
        """ 


