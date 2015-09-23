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
    
    Fenimore Love
"""

import sys, requests, os, re, datetime
from bs4 import BeautifulSoup

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
		
    # constructor the de-structor!!  
    # I haven't yet actually automated one such method though
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
        corner_dicts = scrape_listings(url)
        return corner_dicts
    def get_recent_corners(url):
        corners = scrape_listings(url)
        recents = get_recent(corners)
        return recents
        
"""
    This is the bread and butter of the program. Scrape Listing
    Constructs a dict for each of the from page of a search,
    given a url. This can then be put into the Corner object.
    Or just handled as a dict.    
"""

def scrape_listings(url):
    computers = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ordinateurs = soup.find_all("div", {"class":"lbc"})
    # x = 0 # Counter, Why not?
    """
        The ordinateur has english attributes
        et le computer a les francais
        Duh
        Getting images can be tricky, if they don't exist.
        Le Bon Coin uses all kinds of weird newline and space oddities
        to mess with us. Hence the plentiful (but necessary!)
        replace() and strip() functions 
    """
    
    for ordinateur in ordinateurs:
        url = ordinateur.find_parent('a')['href']
        date = ordinateur.find("div", {'class':'date'}).text.replace('\n'," ").strip()
        details = ordinateur.find('div', {'class':'detail'})
        title = str(details.find('h2', {'class':'title'}).string).replace('\n', '').strip()
        category = str(details.find('div', {'class':'category'}).string).replace('\n', '').strip()
        placement = str(details.find('div', {'class':'placement'}).string).replace('\n', '').strip().replace('                                                                                            /                                                                                                                            	                                        '," ")
        price =  str(details.find('div', {'class':'price'}).string).replace('\n', '').strip()
        try:
            image_div = ordinateur.find('div', {'class':'image'})
            image_nb = image_div.find('div', {'class':'image-and-nb'})
            image_url = image_nb.find('img')['src']
        except:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/200px-No_image_available.svg.png" # No-image image        
        computer = {'url':url, 'titre': title, 'prix': price,'location': placement, 'image': image_url, 'date':date, 'category': category }
        computers.append(computer) # A list of Dicts
        #x += 1 # Counter, why not?
    return computers
    
"""
    Computer = {
                url, titre, prix, location, image, date, category = ...
               }
"""
 
def get_recent(computers): # TODAYS listings
    recent_computers = []
    for computer in computers:
        today = str(datetime.datetime.now().day) + '-' + str(datetime.datetime.now().month)
        c = re.compile('Aujourd\'hui') # Regex match, this is because of Le Bon Coin's format
        if c.match(computer['date']):
            computer['date'] = computer['date'].replace('Aujourd\'hui', today)
            recent_computers.append(computer)
    return recent_computers


