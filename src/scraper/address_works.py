from postal.parser import parse_address 
from address_schema import AddressInfo
from model_loader_engine import get_client_instance

def add_gmap_address(soup, current_address):
    # This directly finds <a> tags whose href attribute contains "google.com/maps"
    map_links = soup.select('a[href*="google.com/maps"]')
    
    
    for link in map_links:

        current_address["k"] += 1
        current_address[current_address["k"]] = link.text
        

def get_ai_address(soup):
    
    for hidden_or_code in soup(["script", "style", "svg", "noscript", "iframe"]):
        hidden_or_code.decompose()
    # 2. Extract specific regions if you want to be precise:
    main_content = soup.find("main") or soup.find("body") or soup
    footer_content = soup.find("footer")

    main_text = main_content.get_text(separator="\n") if main_content else ""
    footer_text = footer_content.get_text(separator="\n") if footer_content else ""
    combined_text = f"--- PAGE CONTENT ---\n{main_text}\n\n--- FOOTER & CONTACT INFO ---\n{footer_text}"
    
    client = get_client_instance()

    response = client(
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a strict data extraction engine. Your job is to output structured data matching the schema rules. "
                    "If you cannot locate any physical address strings anywhere on the page, verify that your data fields handle defaults."
                ),
            },
            {
                "role": "user",
                "content": f"Analyze this parsed web text and populate the response fields:\n\n{combined_text}",
            }
            
        ],
        response_model=AddressInfo,
        max_tokens=512
        
    )

    return response


def add_address(soup,current_address):
    #from the pydantic object( response ), we add it to the address set
    response = get_ai_address(soup)
    if response.has_address == True:
        address = {}
        if response.street_address:
            address["street_address"] = response.street_address
        if response.city:
            address["city"] = response.city
        if response.state_or_province:
            address["state_or_province"] = response.state_or_province
        if response.country:
            address["country"] = response.country
        if response.postal_code:
            address["postal_code"] = response.postal_code
        if response.full_formatted_address:
            address["full_formatted_address"] = response.full_formatted_address

        current_address["k"] += 1
        current_address[current_address["k"]] = address       
        return True
    return False
if __name__ == "__main__":
    
    print("hello")