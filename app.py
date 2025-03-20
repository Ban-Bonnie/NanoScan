from flask import Flask, jsonify, render_template, request,redirect,url_for
from flask_mysqldb import MySQL
from RFIDreader import Reader
from datetime import timedelta

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
            return render_template("index1.html")


        @self.app.route("/admin")
        def admin():
            return render_template("admin-dashboard.html", adminProfile = self.adminInstance)



        #processes
        def scan_rfid():
            rfid_reader = Reader(port="COM3")  
            rfid_reader.connect()
            rfid_tag = rfid_reader.read_card()
            rfid_reader.close()  # Close immediately after reading
            return rfid_tag

        @self.app.route("/fetch-user")
        def fetch_user():
            try:
                rfid_tag = scan_rfid()
                
                if rfidIsAdmin(rfid_tag):
                    return jsonify({'redirect': url_for('admin')})
                
                if not rfid_tag:
                    return jsonify({'error': 'No RFID tag detected'}), 400

                print("✅ RFID scanned:", rfid_tag)

                # Get user
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM students WHERE tag_no = %s", (rfid_tag,))
                user = cursor.fetchone()

                if not user:
                    cursor.close()
                    return jsonify({'error': 'User not found'}), 404
                
                

                user_keys = ["id", "first_name", "last_name", "parent_phone", "student_phone", "tag_no","section", "id_no", "program"]
                user_dict = dict(zip(user_keys, user))

                # Get user schedule
                cursor.execute("SELECT * FROM section_schedule WHERE section = %s", (user_dict["section"],))
                schedule_data = cursor.fetchall()

                column_names = [desc[0] for desc in cursor.description]
                user_schedule = []

                #Convert timedelta to string
                for row in schedule_data:
                    row_dict = dict(zip(column_names, row))
                    
                    if isinstance(row_dict["start_time"], timedelta):
                        row_dict["start_time"] = str(row_dict["start_time"])
                    if isinstance(row_dict["end_time"], timedelta):
                        row_dict["end_time"] = str(row_dict["end_time"])

                    user_schedule.append(row_dict)


                cursor.close()

                return jsonify({
                    'user': user_dict,
                    'userSchedule': user_schedule
                })

            except Exception as e:
                import traceback
                traceback.print_exc() 
                return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

        @self.app.route("/register-rfid")
        def register_rfid():
            rfid = scan_rfid()
            print(rfid)
            if not rfid:
                return jsonify({'error': 'No RFID tag detected'}), 400
            
            if rfidIsRegistered(rfid):
                return jsonify({'error': 'RFID tag already registered'}), 400

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
            if request.method == "POST":

                student_id = request.form["student_id"]
                firstname = request.form["firstname"]
                lastname = request.form["lastname"]
                parent_phone = request.form["parent_phone"]
                student_phone = request.form["student_phone"]
                tag_no = request.form["tag_no"]
                section = request.form["section"]
                program = request.form["program"]
                try:
                    cursor = mysql.connection.cursor()
                    
                    # Add student to student table
                    cursor.execute(
                        "INSERT INTO students (student_id, first_name, last_name, parent_phone, student_phone, tag_no, section, program) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                        (student_id, firstname, lastname, parent_phone, student_phone, tag_no, section,program)
                    )

                    # Register RFID to RFID list
                    cursor.execute(
                        "INSERT INTO rfid (tag_no, registeredn, admin) VALUES (%s, %s, %s)", 
                        (tag_no, 1,0)
                    )

                    mysql.connection.commit()
                    
                except Exception as e:
                    mysql.connection.rollback()  
                    print(f"Error: {e}")  
                    
                finally:
                    cursor.close()
                    return redirect(url_for('admin'))

            else:
                return redirect(url_for('home'))
        
            
        
        def rfidIsRegistered(rfid):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT tag_no FROM rfid WHERE registered = %s", (1,))
            tags = cursor.fetchall() 
            tags = [tag[0] for tag in tags]
            print("RFID is registered: " ,rfid in tags  )
            return rfid in tags  
        
        def rfidIsAdmin(rfid):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT tag_no FROM rfid WHERE admin = %s", (1,))
            tags = cursor.fetchall() 
            tags = [tag[0] for tag in tags]
            print("RFID is admin: " ,rfid in tags )
            return rfid in tags  

        

    def run(self):
        self.app.run(debug=True, use_reloader=False)  

nano_scan = NanoScan(__name__)  
nano_scan.setup_route()
nano_scan.run()
