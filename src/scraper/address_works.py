def add_gmap_address(soup, current_address):
    # This directly finds <a> tags whose href attribute contains "google.com/maps"
    map_links = soup.select('a[href*="google.com/maps"]')
    
    for link in map_links:
        current_address.add(link)

def add_address(soup,current_address):
    addr1 = soup.find_all(class_=["address","addr","location"])
    addr = soup.find_all("address")
