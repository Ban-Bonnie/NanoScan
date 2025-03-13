from flask import Blueprint, render_template,g


app_blueprints = Blueprint('app_blueprint', __name__)  

# Define routes inside the blueprint
@app_blueprints.route("/")
def home():
    return render_template("index.html",rfidTag = g.RFIDtag)

@app_blueprints.route("/about")
def about():
    return "ABOUT US"

