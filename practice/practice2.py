from bs4 import BeautifulSoup
import requests


with requests.Session() as session:
    response = session.get("https://www.anjappar.com/")
    html_text = response.text
    soup = BeautifulSoup(html_text,"lxml")

    main = soup.find("main") or soup.find("article") or soup.body
    footer = soup.find("footer") or soup.footer or soup.select(".footer")
    #print(main.get_text("\n",strip="True"))
    #if footer:
     #   print(footer.get_text("\n",strip=True))

    #main_text = main.get_text("\n",strip = True)
    #print(main_text.splitlines())
    #complete_text = main_text.get_text("\n",strip=True)
    #print(complete_text)

    print(soup.find_all(class_="address"))