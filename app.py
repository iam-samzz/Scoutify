from flask import Flask
from src.blueprints.dashbaord_route import home_bp
app = Flask(__name__)

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)
