class UrlDetails:

    def __init__(self,url,title = None,phone_number = None,email = None,address = None):
        self.url = url
        self.title = title
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.request_status = True #True => Successful, False -> Not Successful
        self.error_log = []


        