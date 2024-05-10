# Start with `python -m flask --app board run --port 8000 --debug`
# Helpful link: https://realpython.com/flask-project/
from flask import Flask
from board import pages
import sqlite3

print("\n******************************* \n Visit: http://localhost:8000/ \n******************************* \n")

# app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages.bp)
    conn = sqlite3.connect('poetAI.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS poems (id INTEGER PRIMARY KEY, user TEXT, poem TEXT, rating INTEGER)")
    # cursor.execute("SELECT * from poems")
    # output = cursor.fetchall() 
    # for row in output: 
    #     print(row) 
    conn.commit()
    conn.close()
    return app