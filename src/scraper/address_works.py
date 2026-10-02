from postal.parser import parse_address 
from address_schema import AddressInfo
from model_loader_engine import get_client_instance
import time

def add_gmap_address(soup, current_address):
    # This directly finds <a> tags whose href attribute contains "google.com/maps"
    map_links = soup.select('a[href*="google.com/maps"]')
    
    if map_links:
        for link in map_links:

            current_address["k"] += 1
            current_address[current_address["k"]] = link.text
        
        

def get_ai_address(soup):
    #
    t0 = time.perf_counter()

    reduced_text = get_reduced_text(soup)

    #
    t1 = time.perf_counter()


    client = get_client_instance()

    #
    t2 = time.perf_counter()

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
                "content": f"Analyze this parsed web text and populate the response fields:\n\n{reduced_text}",
            }
            
        ],
        response_model=AddressInfo,
        max_tokens=512,
        temperature = 0.0
        
    )
    #
    t3 = time.perf_counter()

    print(f"[ai] prep text:  {t1 - t0:.2f}s", flush=True)
    print(f"[ai] get client: {t2 - t1:.2f}s", flush=True)
    print(f"[ai] llm call:   {t3 - t2:.2f}s", flush=True)
    print(f"[ai] total:      {t3 - t0:.2f}s", flush=True)

    return response

def get_reduced_text(soup):


    JUNK = ["script", "style", "noscript", "svg", "iframe",
        "nav", "header", "aside", "form", "button"]

    for tag in soup(JUNK):
        tag.decompose()

    main_text = soup.find("main") or soup.find("body") or soup.body or soup
    footer_text = soup.find("footer") or soup.find(id="main-footer") or soup.find("div",id = "footer") or soup.select_one("div[class*='footer']")

    main_text = main_text.get_text("\n",strip = True)
    if footer_text:
        footer_text = footer_text.get_text("\n",strip = True)
    else:
        footer_text = ""
    
    combined_text = shrink(main_text+footer_text)
    return combined_text

#shrinking the text
def shrink(text,limit = 6000):
    line_list = []
    
    for line in text.splitlines():
        if line:
            line_list.append(line)
    complete_text = "\n".join(line_list)
    if len(complete_text) <= limit:
        return complete_text
    half = limit // 2
    return complete_text[:half] + "\n...[cut]...\n" + complete_text[-half:]

    

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