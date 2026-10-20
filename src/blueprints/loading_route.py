from flask import Flask,render_template,Blueprint

loading_bp = Blueprint("loading", __name__)

@loading_bp.route("/loading/<job_id>")
def loading(job_id):

    return render_template("loading.html",job_id = job_id)
