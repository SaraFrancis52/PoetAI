from flask import Blueprint, render_template
from ai import *

bp = Blueprint("pages", __name__)

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route("/generatepoem")
def generatepoem():
    return render_template("pages/generatepoem.html")

@bp.route("/poem")
def poem():
    myData = []
    data1 = {
        "role": "system",
        "content": "Always answer in rhymes."
    }
    myData.append(data1)
    data2 = {
        "role": "user",
        "content": "Tell me a joke about data scientists."
    }
    myData.append(data2)
    theResponse = ai_response(myData),
    print(theResponse)
    return render_template("pages/poem.html", aiResponse=theResponse)

@bp.route("/savedpoems")
def savedpoems():
    return render_template("pages/savedpoems.html")