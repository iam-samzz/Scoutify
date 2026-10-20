from src.scraper.run_scraper import JOBS
from flask import Blueprint,render_template,jsonify


result_bp = Blueprint("results" , __name__)

def format_address(address):
    if not address:
        return ""
    if isinstance(address, dict):
        full_address = address.get("full_formatted_address")
        if full_address:
            return full_address
        parts = (
            address.get(field)
            for field in ("street_address", "city", "state_or_province", "postal_code", "country")
        )
        return ", ".join(part for part in parts if part)
    return str(address)


@result_bp.route('/results/<job_id>')
def results(job_id):

    job = JOBS.get(job_id)
    if job is None:
        return jsonify({"error" : "job id not found"}) ,404

    if job["status"] != "COMPLETED":
        return jsonify({"error": "job has not completed"}), 409

    result_obj = job["result"] or {}
    urls = []
    for detail in result_obj.values():
        address_data = detail.address or {}
        if isinstance(address_data, dict):
            addresses = [
                format_address(value)
                for key, value in address_data.items()
                if key != "k"
            ]
        else:
            addresses = [format_address(address_data)]

        urls.append({
            "url": detail.url,
            "title": detail.title,
            "email": sorted(detail.email or []),
            "phone_number": sorted(detail.phone_number or []),
            "address": [address for address in addresses if address],
        })

    return render_template('results.html', urls=urls)
