
from phone_number import get_numbers
from urllib.parse import urljoin
def add_contact_from_text(soup,current_phone_number):
    #geting html from the current url's soup
    text = soup.get_text(" ",strip=True)

    # getting numbers from text
    numbers_list = get_numbers(text)

    #updating the current url's phonenumber set
    current_phone_number.update(numbers_list)
    

def add_contact_from_footer(soup,current_phone_number):
    footer = soup.footer
    if footer:
        footer_text = footer.get_text(" ",strip=True)
        current_phone_number.update(get_numbers(footer_text))
    else:
        footer = soup.find_all(class_=['foot','footer','footer-main','main-footer' 'site-footer', 'page-footer'])
        for f in footer:
            footer_text = f.get_text(" ",strip=True)
            current_phone_number.update(get_numbers(footer_text))
    

def get_contact_url(soup,base):
    full_url = None
    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True).lower()
        raw_href = link["href"].lower()

        if raw_href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        if ("contact" in text) or ("contact" in raw_href):
            full_url = urljoin(base, link["href"])
            break
    return full_url



if __name__ == "__main__":
    print("")