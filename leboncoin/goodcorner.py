"""
    Python 3 Le Bon Coin scraper
    MIT License
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import sys, requests, os, re, datetime
from bs4 import BeautifulSoup

# This is where the files are hosted
sample_url= "http://www.leboncoin.fr/informatique/offres/ile_de_france/?ps=4&pe=8&q=thinkpad&th=1"
"""
    Designed for computers, but could be used for anything I suppose with the right link
    Inside the link parameters:
    - th = photographs (0 = none)
    - ps = low price
    - pe = highest price
    - q = keywords (can take and/or operators, and more)
"""


class Corner(object):
    title = ""
    url = ""
    price = ""
    location = ""
    date = ""
    category = ""
    image = ""
		
    #constructor the de-structor!!  
    def __init__(self, title, url, price, location, date, category, image):
        self.title = title
        self.url = url
        self.price = price
        self.location = location
        self.date = date
        self.category = category
        self.image = image

    #the stringifing printer.... Python is so pretty
    def __str__(self):
        return " Titre: %s \n URL: %s \n Prix: %s \n" % (self.title, self.url, self.price)

    def get_corners(url):
        #corners = []
        corner_dicts = scrape_listings(url)
        #for corner_dict in corner_dicts:
        #    corner = Corner(corner_dict['titre'], corner_dict['url'], corner_dict['prix'], corner_dict['location'], corner_dict['date'], corner_dict['category'],corner_dict['image'])
        #corners.append(corner)
        return corner_dicts
    def get_recent_corners(url):
        corners = scrape_listings(url)
        recents = get_recent(corners)
        return recents



def scrape_listings(url):
    computers = []# define array of listings
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ordinateurs = soup.find_all("div", {"class":"lbc"}) # These are the unsifted listings
    x = 0 # Counter, Why not?
    for ordinateur in ordinateurs:
        url = ordinateur.find_parent('a')['href']
        #images need to be something like, if in class=image div, find img element 
        image_url = "" #ordinateur.find("img")['src'].text
        date = ordinateur.find("div", {'class':'date'}).text.replace('\n'," ").strip()
        details = ordinateur.find('div', {'class':'detail'})
        title = str(details.find('h2', {'class':'title'}).string).replace('\n', '').strip()
        category = str(details.find('div', {'class':'category'}).string).replace('\n', '').strip()
        placement = str(details.find('div', {'class':'placement'}).string).replace('\n', '').strip().replace('                                                                                            /                                                                                                                            	                                        '," ")
        price =  str(details.find('div', {'class':'price'}).string).replace('\n', '').strip()
        ## Images are a bit more complicated:
        try:
            image_div = ordinateur.find('div', {'class':'image'})
            image_nb = image_div.find('div', {'class':'image-and-nb'})
            image_url = image_nb.find('img')['src']
        except:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/200px-No_image_available.svg.png" # No-image image        
        # The ordinateur has english attributes
        # et le computer avais les francais
        computer = {'url':url, 'titre': title, 'prix': price,'location': placement, 'image': image_url, 'date':date, 'category': category }
        # computer is a dictionary, so far lacking the actual url
        computers.append(computer)
        x += 1
        #print(x)
    return computers
    
"""
    Computer = {
                url, titre, prix, location, image, date, category = ...
               }
"""
 
def get_recent(computers): # get the computers listed TODAY
    recent_computers = []
    for computer in computers:
        today = str(datetime.datetime.now().day) + '-' + str(datetime.datetime.now().month)
        c = re.compile('Aujourd\'hui')
        if c.match(computer['date']):
            computer['date'] = computer['date'].replace('Aujourd\'hui', today)
            recent_computers.append(computer)
    return recent_computers


