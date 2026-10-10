from flask import Flask
from src.blueprints.dashboard_route import home_bp
app = Flask(__name__,template_folder="src/templates")

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)
