from flask import Blueprint, render_template, request
from ai import *
import sqlite3

# Fixme: no global variable?
data = []

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

@bp.route("/load")
def load():
    subject = request.args.get('subject')
    print("(Loading) You requested " + subject)
    return render_template("pages/load.html", topic=subject)

@bp.route("/getResponse")
def getResponse():
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
    global data 
    data = parsedData
    return "done"
    
@bp.route("/poem")
def poem():
    return render_template("pages/poem.html", aiResponse=data)

@bp.route("/savedpoems/<pid>")
def savedpoems(pid):
    print("You'd like id " + pid)
    conn = sqlite3.connect('poetAI.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rating, poem from poems where id = " + pid)
    output = cursor.fetchall() 
    conn.close()
    for row in output: 
        print(row) 
        rating = row[0]
        text = row[1]
    print("The rating is " + str(rating))
    parsedData = parse_data(text)
    print(parsedData)
    pidA = int(pid)-1
    pidB = int(pid)
    pidC = int(pid)+1
    pidD = int(pid)+2
    return render_template('pages/savedpoems.html', pid=pid, pidA=pidA, pidB=pidB, pidC=pidC, pidD=pidD, rating=rating, poem=parsedData)

@bp.route('/saving_poem_background')
def saving_poem_background():
    rating = request.args.get('rating')
    print(rating)
    global data
    toclean = data
    print(toclean)
    toclean = clean_data(toclean)
    print(toclean)

    conn = sqlite3.connect('poetAI.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO poems (poem, rating) VALUES ('"+ toclean +"', " + rating + ")")
    conn.commit()
    conn.close()
    return ("nothing")


# Turn dictionary into a string for saving, and remove ' to avoid SQL parsing errors
# FIXME how to save data with single quotes?
def clean_data(data) :
    cleaned = ''
    cleaned.replace("'", "")
    for row in data:
        cleaned += row["text"]
        cleaned += '\n'
    cleaned = cleaned.replace("'", "")
    return cleaned