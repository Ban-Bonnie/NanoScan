from flask import Flask, g, jsonify,render_template
from flask_mysqldb import MySQL

mysql = MySQL()

class NanoScan:
    def __init__(self, name):
        self.app = Flask(name)
        self.RFIDtag = "8U 2J 0E 1W"  # RFID TAG temporary
        self.userInstance = None

        # Database Configuration
        self.app.config['MYSQL_HOST'] = "localhost"
        self.app.config['MYSQL_USER'] = "root"
        self.app.config['MYSQL_PASSWORD'] = ""
        self.app.config['MYSQL_DB'] = "nanoscan"
        mysql.init_app(self.app) 
    
    def setup_route(self):
        @self.app.route("/")
        def home():
            return render_template("index.html", rfidTag=self.RFIDtag)
        
        @self.app.route("/about")
        def about():
            return "ABOUT US"
        
        @self.app.route("/fetch-user")
        def fetch_user():  # Moved this inside setup_route() as a proper route
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE tag_no = %s", (self.RFIDtag,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                return jsonify({
                    'user': user  # Sending user data as JSON
                })
            else:
                return jsonify({'error': 'User not found'}), 404


    


    def run(self):
        self.app.run(debug=True)

nano_scan = NanoScan(__name__)  
nano_scan.setup_route()
nano_scan.run()
