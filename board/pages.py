from flask import Blueprint, render_template, request
from ai import *
import sqlite3

# Fixme: no global variable?
curSubject = ""
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
    style = request.args.get('style')
    if(request.args.get('rhyming')):
        rhyming = "yes"
    else:
        rhyming = "no"
    print("(Loading) You requested " + subject)
    print("(Loading) You requested " + style)
    return render_template("pages/load.html", topic=subject, type=style, rhyme=rhyming)

@bp.route("/getResponse", methods=['GET'])
def getResponse():
    subject = request.args.get('subject')
    style = request.args.get('style')
    rhyming = request.args.get('rhyming')

    myData = []

    if(rhyming == 'yes'):
        data1 = {
        "role": "system",
        "content": "Always answer in rhymes."
        }
        myData.append(data1)
    
    query = ""
    if(style == 'Free'):
        query = "Write me a poem about " + subject
    else:
        query = "Write me a "+ style +" about " + subject 

    data2 = {
        "role": "user",
        "content": query
    }
    myData.append(data2)
    theResponse = ai_response(myData),
    print(theResponse)
    parsedData = parse_data(theResponse[0])
    print(parsedData)
    global data 
    global curSubject
    curSubject = subject
    data = parsedData
    return "done"


# Display the poem the AI created
@bp.route("/poem")
def poem():
    return render_template("pages/poem.html", aiResponse=data, title=curSubject)


# Display the requested poem by it's id
@bp.route("/savedpoems/<pid>")
def savedpoems(pid):
    print("You'd like id " + pid)
    conn = sqlite3.connect('poetAI.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rating, title, poem from poems where id = " + pid)
    output = cursor.fetchall() 
    conn.close()
    for row in output: 
        print(row) 
        rating = row[0]
        title = row[1]
        text = row[2]
    print("The rating is " + str(rating))
    parsedData = parse_data(text)
    print(parsedData)
    pidA = int(pid)-1
    pidB = int(pid)
    pidC = int(pid)+1
    pidD = int(pid)+2
    return render_template('pages/savedpoems.html', pid=pid, pidA=pidA, pidB=pidB, pidC=pidC, pidD=pidD, rating=rating, poem=parsedData, title=title)

# Save the current poem when the user clicks 'Save poem'
@bp.route('/saving_poem_background')
def saving_poem_background():
    rating = request.args.get('rating')
    print(rating)
    if(rating == "" or rating < 1 or rating > 10):
        rating = "0" # FIXME: 0 is currently a placeholder for unknown/invalid

    global data
    global curSubject
    title = curSubject
    toclean = data
    print(toclean)
    toclean = clean_data(toclean)
    print(toclean)

    conn = sqlite3.connect('poetAI.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO poems (poem, title, rating) VALUES ('"+ toclean +"', '" + title + "', " + rating + ")")
    conn.commit()
    conn.close()
    return ("nothing")

@bp.app_errorhandler(404)
def not_found(e):
    return render_template("pages/404.html"),404

# Turn dictionary into a string for saving, and use escape character for ' to avoid SQL parsing errors
def clean_data(data) :
    cleaned = ''
    cleaned.replace("'", "''")
    for row in data:
        cleaned += row["text"]
        cleaned += '\n'
    cleaned = cleaned.replace("'", "''")
    return cleaned