import re

def get_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    return re.findall(pattern,text)

def add_email_to_set(soup,current_email):
    text = soup.get_text(" ",strip = True)
    email_set = set(get_email(text))

    current_email.update(email_set)

if __name__ == "__main__":
    print(get_email("jksfbfnikdjkdn sam@email.com @nfam; sklfj"))