from flask import Blueprint, render_template, request
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
    subject = request.args.get('subject')
    print("You requested: " + subject)
    myData = []
    data1 = {
        "role": "system",
        "content": "Always answer in rhymes."
    }
    myData.append(data1)
    data2 = {
        "role": "user",
        "content": "Write me a poem about " + subject
    }
    myData.append(data2)
    theResponse = ai_response(myData),
    print(theResponse)
    parsedData = parse_data(theResponse[0])
    print(parsedData)
    return render_template("pages/poem.html", aiResponse=parsedData)

@bp.route("/savedpoems")
def savedpoems():
    return render_template("pages/savedpoems.html")