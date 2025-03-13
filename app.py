from flask import Flask, g, jsonify
from app_blueprints import app_blueprints  
from flask_mysqldb import MySQL

mysql = MySQL()

class NanoScan:
    def __init__(self, name):
        self.app = Flask(name)
        self.RFIDtag = "1H 6H 8U 1A"  # RFID TAG temporary
        self.userInstance = None
        self.app.add_url_rule('/fetch-user', 'fetch_user', self.fetch_user_route)

        @self.app.before_request
        def before_request():
            g.RFIDtag = self.RFIDtag
            g.userInstance = self.userInstance

    

        # Database Configuration
        self.app.config['MYSQL_HOST'] = "localhost"
        self.app.config['MYSQL_USER'] = "root"
        self.app.config['MYSQL_PASSWORD'] = ""
        self.app.config['MYSQL_DB'] = "nanoscan"
        mysql.init_app(self.app) 
    
        

    def fetch_user_route(self): #TEMPORARY
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE tag_no = %s", (self.RFIDtag,))  
        user = cursor.fetchone()
        cursor.close()
        return jsonify({'user': user})  # Ensure JSON response

  

    def register_blueprints(self):
        self.app.register_blueprint(app_blueprints)  

    def run(self):
        self.app.run(debug=True)

    


nano_scan = NanoScan(__name__)  
nano_scan.register_blueprints()  
nano_scan.run()
