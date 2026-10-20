from flask import Blueprint,render_template,jsonify,request
import uuid
from threading import Thread
from src.scraper.run_scraper import JOBS,scraper_worker_func

home_bp = Blueprint("home",__name__)

        

@home_bp.route("/")
def dashboard():
    return render_template("dashboard.html")



@home_bp.route('/generate',methods = ['POST'])
def generate():
    # GET DATA FROM FRONTEND 
    # create engine job
    #CREATE JOB ID
    #SEND IT TO LOADING PAGE BY LAODING IT.

    #getting data from frontend
    urls = request.get_json()

    if not urls:
        return jsonify({"error":"Missing URLS json body"}), 400

    # address status validation
    if "addr_status" in urls:
        addr_status = urls.get("addr_status")
        if addr_status:
            del urls["addr_status"]
        else:
            addr_status = False
            del urls["addr_status"]        
    else:
        addr_status = False


    url_list = list(urls)
    #assigning job id
    job_id = str(uuid.uuid4())

    #pending status for job
    JOBS[job_id] = {"status":"PENDING", "result":None }

    #creating a thread for worker function to run in backgroud even when this endpoint ends(i.e even after sending the initial 'OK' response).
    # important : The engine process thread keeps working because threads run independently of the function that created them.
    #

    t1 = Thread(target=scraper_worker_func, args=(job_id, url_list, addr_status))

    #starting the thread...
    t1.start()

    # currently the background worker func is working on the scraper func regardless of this geneate() function
    # once those work is done, it update the data.

    '''
    returing the initial response to the  client , saying that job is created
    and its currently in process.
    '''
    return jsonify({"status":"OK",
                   "job_id":job_id}),202


@home_bp.route('/job-status/<job_id>', methods=['GET'])
def job_status(job_id):

    job = JOBS.get(job_id)

    #check the status in the JOBS and return based on that

    if job:
        status = {"status": job["status"]}
        if "error" in job:
            status["error"] = job["error"]
        return jsonify(status), 200
    else:
        return jsonify({"error":"Job not Found" }) ,404
    