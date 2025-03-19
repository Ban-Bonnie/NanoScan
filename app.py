from flask import Flask, jsonify, render_template, request,redirect,url_for
from flask_mysqldb import MySQL
from RFIDreader import Reader

mysql = MySQL()

class NanoScan:
    def __init__(self, name):
        self.app = Flask(name)
        self.userInstance = None  
        self.userSchedule = None

        self.adminInstance = None
        

        # Database Configuration
        self.app.config['MYSQL_HOST'] = "localhost"
        self.app.config['MYSQL_USER'] = "root"
        self.app.config['MYSQL_PASSWORD'] = ""
        self.app.config['MYSQL_DB'] = "nanoscan"
        mysql.init_app(self.app)

    def setup_route(self):

        #Web Routes
        @self.app.route("/")
        def home():
            return render_template("index.html")

        @self.app.route("/admin")
        def admin():
            return render_template("admin-dashboard.html", adminProfile = self.adminInstance)



        #processes
        @self.app.route("/scan-rfid")
        def scan_rfid():
            rfid_reader = Reader(port="COM3")  
            rfid_reader.connect()
            rfid_tag = rfid_reader.read_card()
            rfid_reader.close()  # Close immediately after reading
            return rfid_tag

        @self.app.route("/fetch-user")
        def fetch_user():
            rfid_tag = scan_rfid()

            if not rfid_tag:
                return jsonify({'error': 'No RFID tag detected'}), 400
            else:
                #get user
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM students WHERE tag_no = %s", (rfid_tag,))
                user = cursor.fetchone()
                

                #get user schedule
                cursor.execute("SELECT * FROM section_schedule WHERE section = %s",(user[7]))
                self.userSchedule = cursor.fetchall()
                print(self.userSchedule) #remove
                cursor.close()

            if user:
                self.userInstance = user
                return jsonify({'user': user}) 
            else:
                return jsonify({'error': 'User not found'}), 404

        @self.app.route("/register-rfid")
        def register_rfid():
            rfid = scan_rfid()
            print(rfid)

            if not rfid:
                return jsonify({'error': 'No RFID tag detected'}), 400
            else:
                return jsonify({'rfid': rfid}) 

        @self.app.route("/admin-login",methods=['POST', 'GET'])
        def admin_login():
            if request.method == 'POST':
                username = request.form["admin-username"]
                password = request.form["admin-password"]
                
                
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM admin_accounts WHERE username = %s AND password = %s",(username,password))
                isAdmin = cursor.fetchone()
                self.adminInstance = isAdmin
                cursor.close()
                if(isAdmin == None):
                    print('incorrect password or username')
                    return redirect(url_for('home'))

                else:
                    
                    return redirect(url_for('admin'))

            else:
                return render_template("index.html")
        
        @self.app.route("/admin-register-rfid", methods=["POST","GET"])
        def registerRFID():
            if request == "POST":

                student_id = request.form["student_id"]
                firstname = request.form["firstname"]
                lastname = request.form["lastname"]
                parent_phone = request.form["parent_phone"]
                student_phone = request.form["student_phone"]
                tag_no = request.form["tag_no"]
                section = request.form["section"]
                
                try:
                    cursor = mysql.connection.cursor()
                    
                    # Add student to student table
                    cursor.execute(
                        "INSERT INTO students (student_id, first_name, last_name, parent_phone, student_phone, tag_no, section) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (student_id, firstname, lastname, parent_phone, student_phone, tag_no, section)
                    )

                    # Register RFID to RFID list
                    cursor.execute(
                        "INSERT INTO rfid (tag_no, registered) VALUES (%s, %s)", 
                        (tag_no, "1")
                    )

                    mysql.connection.commit()
                    
                except Exception as e:
                    mysql.connection.rollback()  
                    print(f"Error: {e}")  
                    
                finally:
                    cursor.close()

            else:
                return redirect(url_for('home'))
        
        @self.app.route("/fetch-user-details")
        def fetch_user_details():
            user = self.userInstance

            cursor = mysql.connection.cursor()

            #get user schedule
            cursor.execute("SELECT * FROM section_schedule WHERE section = %s",(user[7]))
            self.userSchedule = cursor.fetchall()
            print(self.userSchedule) #remove

            #Make userIsLate() when have access with arduino

            #camera API to database

        

    def run(self):
        self.app.run(debug=True, use_reloader=False)  

nano_scan = NanoScan(__name__)  
nano_scan.setup_route()
nano_scan.run()
