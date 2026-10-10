from url_validation import validate_and_extract_homepage
import csv
import io

class Url:
    def __init__(self):
        self.urls = set()
        self.non_urls = set()

        #COLUMN NAME FOR CSV FILE
        self.column_name = 'urls'

    def get_final_url_set(self,url_dict : dict) ->list:
        self.urls = set()
        self.non_urls = set()
        for url_key in url_dict:
            current_url = validate_and_extract_homepage(url_key)
            if current_url:
                self.urls.add(url_key)
            else:
                self.non_urls.add(url_key)
        return [self.urls,self.non_urls]
    def process_url_from_file(self, flask_file_object):
        # 1. Read and decode the raw file bytes into a text string
        file_data = flask_file_object.read().decode('utf-8')
        text_stream = io.StringIO(file_data)

        # 2. Read the in-memory stream directly
        reader = csv.DictReader(text_stream)

        # 3. Create a dictionary to store your URLs
        url_dict = {}

        # 4. Loop through the rows and populate the dictionary
        for row in reader:
            url_key = row.get(self.column_name)
            if url_key:
                url_key = url_key.strip()
                # Store the URL as a key in the dictionary (value can be None or whatever you like)
                url_dict[url_key] = None 
        return url_dict
    





