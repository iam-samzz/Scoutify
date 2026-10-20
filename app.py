from flask import Flask
from src.blueprints.dashboard_route import home_bp

from src.blueprints.loading_route import loading_bp
from src.blueprints.results_route import result_bp

app = Flask(__name__,template_folder="src/templates")



app.register_blueprint(home_bp)
app.register_blueprint(loading_bp)
app.register_blueprint(result_bp)

if __name__ == "__main__":
    app.run(debug=True)
