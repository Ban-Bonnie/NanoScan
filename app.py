from flask import Flask, jsonify, render_template
from flask_mysqldb import MySQL
from RFIDreader import Reader  

mysql = MySQL()

class NanoScan:
    def __init__(self, name):
        self.app = Flask(name)
        self.userInstance = None  # Unused but keeping it

        # Database Configuration
        self.app.config['MYSQL_HOST'] = "localhost"
        self.app.config['MYSQL_USER'] = "root"
        self.app.config['MYSQL_PASSWORD'] = ""
        self.app.config['MYSQL_DB'] = "nanoscan"
        mysql.init_app(self.app)

    def setup_route(self):
        @self.app.route("/")
        def home():
            return render_template("index.html")

        @self.app.route("/about")
        def about():
            return "ABOUT US"

        @self.app.route("/fetch-user")
        def fetch_user():
            """Scans RFID and fetches user from MySQL."""
            rfid_reader = Reader(port="COM3")  
            rfid_reader.connect()
            rfid_tag = rfid_reader.read_card()
            rfid_reader.close()  # Close immediately after reading

            if not rfid_tag:
                return jsonify({'error': 'No RFID tag detected'}), 400

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE tag_no = %s", (rfid_tag,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                return jsonify({'user': user}) 
            else:
                return jsonify({'error': 'User not found'}), 404

    def run(self):
        self.app.run(debug=True, use_reloader=False)  

nano_scan = NanoScan(__name__)  
nano_scan.setup_route()
nano_scan.run()
