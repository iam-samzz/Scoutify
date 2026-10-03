#get the url and work on it
from bs4 import BeautifulSoup
import requests
import time

from contact import Contact
from url_details import UrlDetails

class Scraper:

    def __init__(self,urls:list,addr_status=False):
        self.urls = urls
        self.total_urls = len(urls)

        self.phone_number_completed = 0
        self.email_address_completed = 0
        self.physical_address_completed = 0

        self.fully_completed = 0

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

        self.result = {}

        self.scrape_information = {}

    def scrape(self) -> dict:
        t0 = time.perf_counter()

        complete_status1 = False #its completion status for phone number
        complete_status2 = False #its completion status for email address
        complete_status3 = False #its completion status for address
        
        print("Starting session..",flush=True)
        with requests.Session() as session:
            print("Session Created.",flush=True)

            session.headers.update(self.custom_header)
            
            for url in self.urls:
                url_detail = UrlDetails(url)
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
                    home_soup = BeautifulSoup(site_html,"lxml")
                    site_title = self.contact.get_title(home_soup)

                    #getting contact url
                    contact_url = self.contact.get_contact_url(home_soup,url)

                    #making contact_page_soup
                    if contact_url:
                        try:
                            print(f"[requests] Sending GET to '{contact_url}'...")
                            response = requests.get(contact_url,timeout=3)
                            print(f"Response received from '{contact_url}' ")
                        
                            
                            site_html = response.text
                            contact_page_soup = BeautifulSoup(site_html,"lxml")  

                    
                            if contact_page_soup:
                                self.contact.add_numbers_from_text(contact_page_soup,current_phone_number)
                                self.contact.add_email_to_set(contact_page_soup,current_email)

                                if self.fetch_addresss_also and len(current_address) <= 1:
                                        self.contact.add_address(contact_page_soup,current_address)
                        except requests.exceptions.Timeout:
                            print(f"Timeout error while trying to contact {contact_url}..")

                    if not current_phone_number:
                        print(f"[scraper] Starting phone number scraping for '{url}' ...")
                        self.contact.add_numbers_from_text(home_soup,current_phone_number)
                        print(f"[scraper] Fetched phone numbers!.")

                    if not current_address:
                        print(f"[scraper] Starting email address scraping for '{url}' ... ")
                        self.contact.add_email_to_set(home_soup,current_email)
                        print(f"[scraper] Fetched email address!.")
                    
                    if self.fetch_addresss_also and len(current_address) <= 1:
                        print(f"[scraper] Starting address scraping for '{url}' ... ")
                        self.contact.add_address(home_soup,current_address)
                        self.contact.add_gmap_address(home_soup,current_address)
                        print(f"[scraper] Fetched contact details!.")

                    
                    #printing details
                    print(f"-----------------'{url}' contact details------------------")
                    print(current_phone_number)
                    print(current_email)
                    print(current_address)
                    print(site_title)
                    print(f"-----------------over-------------------------------------")

                    #instanciating url_detail object
                    url_detail.email = current_email
                    url_detail.phone_number = current_phone_number
                    url_detail.title = site_title
                    if self.fetch_addresss_also:
                        url_detail.address = current_address

                    self.result[url] = url_detail
                    

                except requests.exceptions.ConnectionError as e:
                    print("connection error")
                    url_detail.request_status = False
                    url_detail.error_log.append("Requests ConnectionError.")
                    continue
                except requests.exceptions.ReadTimeout as e:
                    print("READ TIMEOUT")
                    url_detail.request_status = False
                    url_detail.error_log.append("Requests ReadTimeout Exception.")
                    continue
                except requests.exceptions.Timeout:
                    print("Requests time out")
                    url_detail.request_status = False
                    url_detail.error_log.append("Requests Timeout Exception.")
                    continue
                if current_phone_number:
                    complete_status1 = True
                    self.phone_number_completed += 1
                if current_email:
                    complete_status2 = True
                    self.email_address_completed += 1
                if len(current_address) > 1:
                    complete_status3 = True
                    self.physical_address_completed += 1

                if self.fetch_addresss_also:
                    if complete_status1 and complete_status2 and complete_status3:
                        self.fully_completed += 1
                else:
                    if complete_status1 and complete_status2:
                        self.fully_completed += 1
            
            print(f"Out of {self.total_urls} , {self.fully_completed} urls are fully completed.")
            print(f"{self.phone_number_completed} Phone numbers completed out of {self.total_urls} url's")
            print(f"{self.email_address_completed} Email addresses completed out of {self.total_urls} url's")
            if self.fetch_addresss_also:
                print(f"{self.physical_address_completed} Physical address completed out of {self.total_urls}")
        t1 = time.perf_counter()
        total_time_taken = round((t1 - t0),5)

        print(f"Time taken for scraping: {total_time_taken}s")

        self.scrape_information["total_time_taken"] = total_time_taken
        self.scrape_information["tot_fully_complete"] = self.fully_completed
        self.scrape_information["tot_email_address_complete"] = self.email_address_completed
        self.scrape_information["tot_phone_number_complete"] = self.phone_number_completed


        return self.result
    
    def get_detail_from_url(self,url:str)-> UrlDetails | None:
        details_obj = self.result.get(url)
        return details_obj
    
    def get_all_email(self)->dict:
        all_email = {}
        for url_key in self.result:
            detail_obj = self.result[url_key]
            all_email[url_key] = detail_obj.email
        return all_email
    def get_all_phone_number(self)-> dict:
        all_phone_number = {}
        for url_key in self.result:
            detail_obj = self.result[url_key]
            all_phone_number[url_key] = detail_obj.phone_number
        return all_phone_number
    
    def get_all_title(self)->dict:
        all_title = {}
        for url_key in self.result:
            detail_obj = self.result[url_key]
            all_title[url_key] = detail_obj.title
        return all_title
    
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

    scraper = Scraper(urls)


    result = scraper.scrape()
    detail = scraper.get_detail_from_url('https://pinkfort.com')
    if detail:
        print(detail.email)
    else:
        print(None)