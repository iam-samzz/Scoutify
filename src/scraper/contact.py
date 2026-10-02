from number_works import get_contact_url,add_numbers_from_text
from email_works import add_email_to_set
from address_works import add_address,add_gmap_address
from bs4 import BeautifulSoup

class Contact:
    def get_title(self,soup):
        return soup.title
    
    def get_contact_url(self,soup:BeautifulSoup,base_url:str) -> str:
        return get_contact_url(soup,base_url)

    def add_numbers_from_text(self,soup:BeautifulSoup,current_phone_number:set)->None:
        return add_numbers_from_text(soup,current_phone_number)

    def add_email_to_set(self,soup:BeautifulSoup,current_email:set) -> None:
        return add_email_to_set(soup,current_email)

    def add_address(self,soup,current_address:dict) -> bool:
        return add_address(soup,current_address)

    def add_gmap_address(self,soup:BeautifulSoup,current_address:dict) -> None:
        return add_gmap_address(soup,current_address)

    