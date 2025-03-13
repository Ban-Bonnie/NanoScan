from flask import Blueprint, render_template, g, current_app

app_blueprints = Blueprint('app_blueprint', __name__)  

@app_blueprints.route("/")
def home():
    
    return render_template("index.html", rfidTag=g.RFIDtag, students = g.userInstance)

@app_blueprints.route("/about")
def about():
    return "ABOUT US"


