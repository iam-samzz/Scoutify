from postal.parser import parse_address 

def add_gmap_address(soup, current_address):
    # This directly finds <a> tags whose href attribute contains "google.com/maps"
    map_links = soup.select('a[href*="google.com/maps"]')
    
    for link in map_links:
        current_address.add(link)

def add_address(soup,current_address):
    addr1 = soup.find_all(class_=["address","addr","location"])
    addr2 = soup.find_all("address")

    addresses = addr1 + addr2
    for address in addresses:
        current = parse_address(address.text)


if __name__ == "__main__":
    
    print(parse_address("Finding the perfect spot to read a book in the city can be an absolute challenge, especially with the constant hum of traffic and the busy rush of people crowding the sidewalks. However, if you walk just a few blocks past the old historic clock tower and turn down the quiet, tree-lined avenue, you will stumble upon a hidden gem of a cafe known for its incredible espresso and peaceful courtyard. The exact location of this little sanctuary is 4522 Maplewood Avenue, Suite 100, Austin, TX 78722, tucked neatly between a vintage bookstore and a family-owned flower shop. Regulars love to gather here in the late afternoons to sit under the shaded oak trees, sip on iced lattes, and escape the chaotic pace of everyday life. It is the kind of place that feels like a well-kept secret, even though it sits just minutes away from the heart of the bustling downtown district."))