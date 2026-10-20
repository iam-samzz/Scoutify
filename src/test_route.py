from flask import Flask, render_template


class Sample_url:

    def __init__(self,url,title = None,phone_number = None,email = None,address = None):
        self.url = url
        self.title = title
        self.phone_number = phone_number
        self.email = email
        self.address = address

        self.request_status = True #True => Successful, False -> Not Successful
        self.error_log = []        
obj1 = Sample_url('google.com',"Google", ['+91 9360401099' , '+91 934334334'], ['sds@gmail.com' , 'klfhdnji@gmail.com'], ['address1 fdkfhndfdkfdnfmdfldf,dmf, address2 dkjsjfnsdfjdsldjknm'])
obj2 = Sample_url('google.com',"Google", ['+91 9360401099' , '+91 934334334'], ['sds@gmail.com' , 'klfhdnji@gmail.com'], ['address1 fdkfhndfdkfdnfmdfldf,dmf, address2 dkjsjfnsdfjdsldjknm'])
obj3 = Sample_url('google.com',"Google", ['+91 9360401099' , '+91 934334334'], ['sds@gmail.com' , 'klfhdnji@gmail.com'], ['address1 fdkfhndfdkfdnfmdfldf,dmf, address2 dkjsjfnsdfjdsldjknm'])
obj4 = Sample_url('google.com',"Google", ['+91 9360401099' , '+91 934334334'], ['sds@gmail.com' , 'klfhdnji@gmail.com'], ['address1 fdkfhndfdkfdnfmdfldf,dmf, address2 dkjsjfnsdfjdsldjknm'])
obj5 = Sample_url('google.com',"Google", ['+91 9360401099' , '+91 934334334'], ['sds@gmail.com' , 'klfhdnji@gmail.com'], ['address1 fdkfhndfdkfdnfmdfldf,dmf, address2 dkjsjfnsdfjdsldjknm'])

urls = [obj1 , obj2 , obj2 , obj3 , obj4, obj5]

app = Flask(__file__)


@app.route("/",methods = ['GET'])
def home():

    return render_template('dashboard.html')

@app.route("/results", methods = ['GET'])
def show_result():

    return render_template('results.html',urls = urls)


if __name__ == "__main__":

    app.run(debug=True)