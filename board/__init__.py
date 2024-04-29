# Start with `python -m flask --app board run --port 8000 --debug`
# Helpful link: https://realpython.com/flask-project/
from flask import Flask
from board import pages

print("\n******************************* \n Visit: http://localhost:8000/ \n******************************* \n")

# app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages.bp)
    return app