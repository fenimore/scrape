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

def scrape_listings(url):
    computers = []# define array of listings
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ordinateurs = soup.find_all("div", {"class":"lbc"}) # These are the unsifted listings
    x = 0 # Counter, Why not?
    for ordinateur in ordinateurs:
        url = ordinateur.find_parent('a')['href']
        image_url = ordinateur.find("img")['src']
        date = ordinateur.find("div", {'class':'date'}).text.replace('\n'," ").strip()
        details = ordinateur.find('div', {'class':'detail'})
        title = str(details.find('h2', {'class':'title'}).string).replace('\n', '').strip()
        category = str(details.find('div', {'class':'category'}).string).replace('\n', '').strip()
        placement = str(details.find('div', {'class':'placement'}).string).replace('\n', '').strip().replace('                                                                                            /                                                                                                                            	                                        '," ")
        price =  str(details.find('div', {'class':'price'}).string).replace('\n', '').strip()
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


