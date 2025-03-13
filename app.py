from flask import Flask,g
from app_blueprints import app_blueprints  

class NanoScan:
    def __init__(self, name):
        self.app = Flask(name)
        self.RFIDtag = "1H 6H 8U 1A" #RFID TAG temporary

        @self.app.before_request
        def before_request():
            g.RFIDtag = self.RFIDtag

    

    def register_blueprints(self):
        self.app.register_blueprint(app_blueprints)  

    def run(self):
        self.app.run(debug=True)


nano_scan = NanoScan(__name__)  
nano_scan.register_blueprints()  
nano_scan.run()  
