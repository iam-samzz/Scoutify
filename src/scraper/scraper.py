#get the url and work on it
from bs4 import BeautifulSoup
import requests
import time

from contact import Contact

class Scraper:

    def __init__(self,urls,addr_status=False):
        self.urls = urls
        self.total_urls = len(urls)
        self.completed = 0
        self.custom_header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
        self.contact = Contact()
        self.fetch_addresss_also = addr_status
    def scrape(self):
        t0 = time.perf_counter()
        with requests.Session() as session:

            session.headers.update(self.custom_header)

            for url in self.urls:
                current_phone_number = set()
                current_email = set()
                site_title = None
                #here k is they key is the count of elements in the dict, and also used to find the next key
                current_address = {"k":0}
                
                try:
                    print(f"[requests] Sending GET to '{url}'...")
                    response = requests.get(url,timeout=3)
                    print(f"[requests] Response Received from '{url}'.")

                    site_html = response.text
                    soup = BeautifulSoup(site_html,"lxml")
                    site_title = self.contact.get_title(soup)

                    # add contact list from footer if available
                    #add_contact_from_footer(soup,current_phone_number)

                    #adding from the home page itself
                    print(f"[scraper] Starting phone number scraping for '{url}' ...")
                    self.contact.add_numbers_from_text(soup,current_phone_number)
                    print(f"[scraper] Fetched phone numbers!.")

                    print(f"[scraper] Starting email address scraping for '{url}' ... ")
                    self.contact.add_email_to_set(soup,current_email)
                    print(f"[scraper] Fetched email address!.")

                    if self.fetch_addresss_also:
                        print(f"[scraper] Starting address scraping for '{url}' ... ")
                        self.contact.add_address(soup,current_address)
                        self.contact.add_gmap_address(soup,current_address)
                        print(f"[scraper] Fetched contact details!.")

                    #find contact us link
                    contact_url = self.contact.get_contact_url(soup,url)
                    if contact_url:
                        print(f"[requests] Sending GET to '{contact_url}'...")
                        response = requests.get(contact_url,timeout=3)
                        print(f"Response received from '{contact_url}' ")
                        site_html = response.text
                        soup = BeautifulSoup(site_html,"lxml")  

                        self.contact.add_numbers_from_text(soup,current_phone_number)
                        self.contact.add_email_to_set(soup,current_email)

                        if self.fetch_addresss_also:
                            if len(current_address) <= 1:
                                self.contact.add_address(soup,current_address)
                        

                        
                    #getting email
                    print(f"-----------------'{url}' contact details------------------")
                    print(current_phone_number)
                    print(current_email)
                    print(current_address)
                    print(site_title)
                    print(f"-----------------over-------------------------------------")
                except TimeoutError:
                    print("timeout error!")
                    continue
                except requests.exceptions.ConnectionError:
                    print("connection error")
                    continue
                except requests.exceptions.ReadTimeout:
                    print("READ TIMEOUT")
                    continue
                if current_phone_number:
                    self.completed += 1
            print()
            print(f"Out of {self.total_urls} , {self.completed} is completed.")

            t1 = time.perf_counter()
            print(f"Time taken for scraping: {(t1 - t0):.5f}s")

if __name__ == "__main__":

    urls = [
    "https://mahifashions.in",
    "https://www.beelittle.in",
    "https://manjuboutique.in",
    "https://www.minikki.in",
    "https://tula.org.in",
    "https://velaura.in",
    "https://shopnadi.in",
    "https://fashioncloud.in",
    "https://styleunion.in",
    "https://ethnicboutique.in",
    "https://dstylz.in",
    "https://ramrajcotton.in",
    "https://spatikaclothing.com",
    "https://stitchhub.in",
    "https://ekantastudio.com",
    "https://kyraboutique.in",
    "https://anyaonline.in",
    "https://jdcstore.com",
    "https://maatshi.com",
    "https://aruviboutique.com",
    "https://giniandjony.com",
    "https://thechikankari.com",
    "https://indianroots.com",
    "https://fabindia.com",
    "https://okhai.org",
    "https://rangoliindia.com",
    "https://craftsvilla.com",
    "https://biba.in",
    "https://wforwoman.com",
    "https://aurelia.in",
    "https://libas.in",
    "https://houseofindya.com",
    "https://globaldesi.in",
    "https://soch.com",
    "https://aacho.in",
    "https://truebrowns.com",
    "https://suta.in",
    "https://pinkfort.com",
    "https://chidiyaa.com",
    "https://okhai.org"
    ]

    scraper = Scraper([
    "https://mahifashions.in",
    "https://www.beelittle.in",
    "https://manjuboutique.in"])
    scraper.scrape()