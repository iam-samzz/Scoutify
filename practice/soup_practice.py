# practicing Beautiful Soup
import requests
from bs4 import BeautifulSoup
with requests.Session() as session:
    response = session.get("https://www.anjappar.com/")

    html_text = response.text

    soup = BeautifulSoup(html_text,"lxml")

    #print(soup.find("div",class_ = "main_MF"))

    #print(soup.select("href"))
    #print(soup.find_all("a",href=True))

    #print(type(soup))

    JUNK = ["script", "style", "noscript", "svg", "iframe",
        "nav", "header", "aside", "form", "button",
        "template", "link", "meta"]
    #print(soup(["header","div"]))
    
    for tag in soup(JUNK):
        tag.decompose()
    print(soup)
