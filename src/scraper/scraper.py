#get the url and work on it
from bs4 import BeautifulSoup
import requests

from number_add import add_contact_from_footer,get_contact_url,add_contact_from_text
from email_works import add_email_to_set
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

    custom_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    tot = len(urls)
    completed = 0

    with requests.Session() as session:

        session.headers.update(custom_header)

        for url in urls:
            current_phone_number = set()
            current_email = set()
            current_address = set()
            try:
                response = requests.get(url,timeout=3)
                site_html = response.text
                soup = BeautifulSoup(site_html,"lxml")

                # add contact list from footer if available
                #add_contact_from_footer(soup,current_phone_number)

                #adding from the home page itself
                add_contact_from_text(soup,current_phone_number)
                add_email_to_set(soup,current_email)

                #find contact us link
                contact_url = get_contact_url(soup,url)
                if contact_url:
                    
                    response = requests.get(contact_url,timeout=3)
                    site_html = response.text
                    soup = BeautifulSoup(site_html,"lxml")  
                    add_contact_from_text(soup,current_phone_number)
                    add_email_to_set(soup,current_email)
                    
                #getting email
                print(current_phone_number)
                print(current_email)
            except TimeoutError:
                print("timeout error!")
                continue
            except requests.exceptions.ConnectionError:
                print("connection error")
            except requests.exceptions.ReadTimeout:
                print("read timeout")
            if current_phone_number:
                completed += 1
        print()
        print(f"Out of {tot} , {completed} is completed.")