#!/usr/bin/env python
"""
    Pump IO Bot for posting leboncoin annonces
    Python 3
    MIT License
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
    Fenimore Love

    See Stephen Sekula's weather bot: http://polari.us/dokuwiki/doku.php?id=weatherbot

"""

import re, sys, os, time
from datetime import datetime

from pypump import PyPump, Client
from pypump.models.collection import Collection
from pypump.models.collection import Public
from pypump.models.person import Person
from pypump.exception import PyPumpException

from goodcorner import Corner # A script for scraping leboncoin into Dicts


# TODO: Format Listing, heading
"""
     Place the credentials below for the pump.io account
     These can be obtained by using: 
     http://polari.us/dokuwiki/doku.php?id=navierstokes
 #a_simple_program_to_authenticate_pypump_against_your_pumpio_instance
      or use the get_credentials script for python 3
"""
client_credentials = [secret, password]
client_tokens = ['puppies', 'kittens'] # These don't go anywhere, but steve had them
webfinger = "goodcorners@hotpump.net"# Webfinger for your account
def simple_verifier(url):
    print('Go to: ' + url)
    return input('Verifier: ') # they will get a code back
client = Client(
    webfinger,
    name="CornerBot",
    type="native",
    key=client_credentials[0], # client key
    secret=client_credentials[1] # client secret
)
pump = PyPump(
    client=client,
    verifier_callback=simple_verifier
)

b_set = set() # the B set is TODAYS postings

# logfile_name = "cornerbot.activity.log"
# process_log = open(logfile_name,'a+')
# process_log.write(blah)

while 99==99:
    listing = ""
    header = ""
    print("\n\nInitiating\n\n")
    timestamp = str(datetime.now())
    header += timestamp + " - Paris - " 
    """
        Gather the Le bon Coin Annonces
        for thinkpads entre 40 et 200 euros
    """
    # a list of Dicts of todays postings
    corners = Corner.get_recent_corners('http://www.leboncoin.fr/informatique/offres/ile_de_france/?ps=4&pe=8&q=thinkpad&th=1')
    """
        Remove the postings which the
        Cornerbot has already posted
        This requires all sorts of funny business
        a_set = most recent scrape
        b_set = today's scrapes
        c_set = the annonces not yet posted by cornerbot
    """
    a_set = set() # Add the tuples to A set
    for corner in corners:
        tup = tuple(sorted(corner.items()))
        a_set.add(tup)
        
    c_set = a_set - b_set # Get the Posting not yet Posted
    b_set = a_set         # Update the Todays posting set (B)
    print("\n New items: " , len(list(c_set)))
    print("\n Total items posted: ", len(list(b_set)))    

    """
        Publish the new items to Pump.io
        Pump publishes in html
    """
    corners_pub = map(dict, c_set) # map takes a function and an iterable 
    print(type(corners_pub))   
    if len(list(c_set)) is not 0: # if there exists new items (from a - b )
        for corner in corners_pub: # TODO: https://pyformat.info/
            # Set up HTML Styled Posting for Pump.io
            listing += "<table><tr><td><img src=" + corner['image'] + " width=100px height=auto/></td><td><b><a href=" + corner['url'] + ">"+ corner['titre'] + "</a></b><br><a href=" + corner['url'] + " >Annonce</a> " + corner['location']+" pour " + corner['prix'] + "<br>" + corner['date'] +"</td></tr></table>" 
            listing += "<br>"
            header += corner['prix']
            print("\nwrote listing")
            print("...   "+ corner['titre'])
        posting = pump.Note(listing, header)
        posting.to = pump.Person("polypmer@microca.st")
        posting.send()
        print("Posting " +timestamp)
    else:
        print("No new corners\n\n\n")    
    # Finished Post
    print("\n\nSleep Now")
    time.sleep(7000) # 3600 Seconds = Hour

#process_log.close()


