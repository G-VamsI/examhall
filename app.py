from flask import Flask, render_template, request, send_file,url_for,jsonify
import pandas as pd
import os
from collections import Counter
from flask_bcrypt import Bcrypt
import mysql.connector
from flask_mail import Mail, Message
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="V@mshi",
    database="mydb"
)
cursor = db.cursor()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'omc2651@gmail.com'  
app.config['MAIL_PASSWORD'] = 'ksei uble vnzs hudq'   
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
mail = Mail(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

allocated_data = []
date = None
time = None
# Function to load Excel data
def load_file_data(file):
    if file.endswith('.xlsx'):
        data = pd.read_excel(file)
        return data.to_dict(orient='records')
    elif file.endswith('.csv'):
        data = pd.read_csv(file)
        return data.to_dict(orient='records')  
    else:
        # raise ValueError("Unsupported file format. Only Excel (.xlsx) and CSV files are allowed.")
        return "This type of file is not supported"


# Allocate students and save to Excel file
def allocate_students_to_benches(students, classrooms, teachers):
    global allocated_data
    global teacher_invigilation
    global err
    allocated_data = []  # Reset the allocated data
    err=""
    subject_count = Counter(student['Subject'] for student in students)
    # Sort by subject count (descending) and roll number (ascending)
    students_sorted = sorted(students, key=lambda x: (-subject_count[x['Subject']]))
    ffb = 1
    ffc = 0
    fsb = 1
    fsc = 0
    sfb=1
    ssb = 1
    sfc = 0
    ssc =0
    idx = 0
    teacher_invigilation = []
    try:        
        while idx<len(students_sorted):

            current_cls = ffc
            bench_number = ffb
            student1 = students_sorted[idx]
            subject = student1['Subject']
            while  idx <len(students_sorted) and student1['Subject'] == subject:
                classroom = classrooms[current_cls]
                if(current_cls>= len(teachers)):
                    err= 'No sufficient teachers available for allocation'
                    return [],[]
                teacher = teachers[current_cls]
                student1 = students_sorted[idx] 
                bench_number = 1
                while  idx <len(students_sorted) and  bench_number < int(classroom['Total Benches']) and student1['Subject']==subject: 
                    allocated_data.append({
                                'Classroom': classroom['Classroom ID'],
                                'Bench Number': bench_number,
                                'Reg No': student1['Reg No'],
                                'Student Name': student1['Name'],
                                'Subject': student1['Subject'],
                                'Year of Study': student1['Year of Study'],
                                'Teacher Name': teacher['Name'],
                                'Email':student1['Email']
                            })
                    student1 = students_sorted[idx]
                    bench_number = bench_number+2
                    idx+=1
                row = {
                    'ID':teacher['ID'],
                    'Name':teacher['Name'],
                    'Email':teacher['Email'],
                    'Classroom':classroom['Classroom ID']
                }
                if row not in teacher_invigilation:
                    teacher_invigilation.append(row)
                current_cls+=1
            ffc = classroom
            ffb = bench_number

            if(idx >= len(students_sorted)):
                break


            # first row second column alternatives
            current_cls = fsc
            bench_number = fsb
            student1 = students_sorted[idx]
            subject = student1['Subject']
            while  idx <len(students_sorted) and student1['Subject'] == subject:
                classroom = classrooms[current_cls]
                if(classroom['Total Capacity Per Bench'] == 1):
                    current_cls+=1
                    if(current_cls>= len(teachers)):
                        err = 'No sufficient teachers available for allocation'
                        return [],[]
                    continue
                if(current_cls>= len(teachers)):
                    err= 'No sufficient teachers available for allocation'
                    return [],[]
                teacher = teachers[current_cls]
                student1 = students_sorted[idx] 
                bench_number = 1
                while  idx <len(students_sorted) and bench_number < int(classroom['Total Benches']) and student1['Subject']==subject:
                    
                    allocated_data.append({
                                'Classroom': classroom['Classroom ID'],
                                'Bench Number': bench_number,
                                'Reg No': student1['Reg No'],
                                'Student Name': student1['Name'],
                                'Subject': student1['Subject'],
                                'Year of Study': student1['Year of Study'],
                                'Teacher Name': teacher['Name'],
                                'Email':student1['Email']
                            })

                    student1 = students_sorted[idx]
                    bench_number = bench_number+2
                    idx+=1
                row = {
                    'ID':teacher['ID'],
                    'Name':teacher['Name'],
                    'Email':teacher['Email'],
                    'Classroom':classroom['Classroom ID']
                }
                if row not in teacher_invigilation:
                    teacher_invigilation.append(row)
                current_cls+=1
            fsc = classroom
            fsb = bench_number

            if(idx >= len(students_sorted)):
                break        



            # second row first column alternatives
            current_cls = sfc
            bench_number = sfb
            student1 = students_sorted[idx]
            subject = student1['Subject']
            while  idx <len(students_sorted) and  student1['Subject'] == subject:
                classroom = classrooms[current_cls]
                if(current_cls>= len(teachers)):
                    err= 'No sufficient teachers available for allocation'
                    return [],[]
                teacher = teachers[current_cls]
                bench_number = 2
                while idx <len(students_sorted) and bench_number < int(classroom['Total Benches']) and student1['Subject']==subject: 
                    allocated_data.append({
                                'Classroom': classroom['Classroom ID'],
                                'Bench Number': bench_number,
                                'Reg No': student1['Reg No'],
                                'Student Name': student1['Name'],
                                'Subject': student1['Subject'],
                                'Year of Study': student1['Year of Study'],
                                'Teacher Name': teacher['Name'],
                                'Email':student1['Email']
                            })
                    
                    idx+=1
                    student1 = students_sorted[idx]
                    bench_number = bench_number+2
                row = {
                    'ID':teacher['ID'],
                    'Name':teacher['Name'],
                    'Email':teacher['Email'],
                    'Classroom':classroom['Classroom ID']
                }
                if row not in teacher_invigilation:
                    teacher_invigilation.append(row)
                current_cls+=1
            sfc = classroom
            sfb = bench_number

            if(idx >= len(students_sorted)):
                break


            # second row second column alternatives
            current_cls = ssc
            bench_number = ssb
            student1 = students_sorted[idx]
            subject = student1['Subject']
            while  idx <len(students_sorted) and student1['Subject'] == subject:
                classroom = classrooms[current_cls]
                if(classroom['Total Capacity Per Bench'] == 1):
                    current_cls+=1
                    if(current_cls>= len(teachers)):
                        err= 'No sufficient teachers available for allocation'
                        return [],[]
                    continue
                if(current_cls>= len(teachers)):
                    err= 'No sufficient teachers available for allocation'
                    return [],[]
                teacher = teachers[current_cls]
                bench_number = 2
                while idx < len(students_sorted) and bench_number < int(classroom['Total Benches']) and student1['Subject']==subject:
                    student1 = students_sorted[idx] 
                    allocated_data.append({
                                'Classroom': classroom['Classroom ID'],
                                'Bench Number': bench_number,
                                'Reg No': student1['Reg No'],
                                'Student Name': student1['Name'],
                                'Subject': student1['Subject'],
                                'Year of Study': student1['Year of Study'],
                                'Teacher Name': teacher['Name'],
                                'Email':student1['Email']
                            })
                    student1 = students_sorted[idx]
                    bench_number = bench_number+2
                    idx+=1
                row = {
                    'ID':teacher['ID'],
                    'Name':teacher['Name'],
                    'Email':teacher['Email'],
                    'Classroom':classroom['Classroom ID']
                }
                if row not in teacher_invigilation:
                    teacher_invigilation.append(row)
                current_cls+=1
            ssc = classroom
            ssb = bench_number
            if(idx >= len(students_sorted)):
                break        
        return allocated_data, teacher_invigilation
    
    except IndexError:
        err= 'No sufficient teachers available for allocation'
        return [],[]


    

def save_allocation_to_excel(allocated_data, filename):
    df = pd.DataFrame(allocated_data)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    df.to_excel(output_path, index=False)
    return output_path

@app.route("/input",methods=['POST'])
def input():
    email = request.form.get('email')  # Get the email from the form data
    password = request.form.get('password')  # Get the password from the form data
    cursor.execute("SELECT email, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()  # Fetch the user's email and hashed password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if user and user[1]== hashed_password:  # Check if the user exists and the password matches
        return render_template('index.html')
    if not user:
        return render_template('login.html',msg='user doesn\'t exist')

    return render_template('login.html',
                           msg='passwords do not match')


@app.route('/home',methods=['POST'])
def home():
    email = request.form.get('email')  # Get the email from the form data
    password = request.form.get('password')  # Get the password from the form data
    cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()  # Fetch the user's email and hashed password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if user and user[1]== hashed_password:  # Check if the user exists and the password matches
        return render_template('index.html')
    if not user:
        return render_template('login.html',msg='user doesn\'t exist')

    return render_template('login.html',
                           msg='passwords do not match')
    return render_template('index.html')


otp = 0
@app.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    if not email:
        return "email required"
    global otp
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    # session['otp'] = otp  
    # session['email'] = email
    msg = Message(subject='OTP', sender='omc2651@gmail.com', recipients=[email])
    msg.body = f"Your OTP is {otp}"
    try:
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'OTP sent successfully'})
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to send OTP.'})


@app.route('/')
def html():
    return render_template('login.html',
                           msg='')
@app.route('/register', methods=['POST'])
def register():
    # if 'otp' not in session or 'email' not in session:
    #     return jsonify({'status': 'error', 'message': 'OTP not sent or email missing.'})
    global otp
    entered_otp = request.form.get('otp')
    if entered_otp != otp:
        return jsonify({'status': 'error', 'message': 'Invalid OTP.'})
    try:
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        college = request.form.get('college_name', '')  # Optional field
        role = request.form.get('role', '')  # Optional field

        # Validate passwords
        if len(password)<8:
            return 'paswds must be min 8 characters'
        if password != confirm_password:
            return "paswds do not match"

        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return "'status': 'error', 'message': 'Email already exists.'"

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert data into the database
        cursor.execute(
            "INSERT INTO users (name, college, email, password, role) VALUES (%s, %s, %s, %s, %s)",
            (username,college, email, hashed_password,  role),
        )
        db.commit()
        
        # Successful registration
        # session['user'] = username  # Optional: Store user in session
        
        return render_template('login.html',
                               msg='')

    except mysql.connector.Error as e:
        db.rollback()  # Rollback transaction in case of error
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Server error: {str(e)}'})

    finally:
        cursor.close()
        db.close()

@app.route('/registration', methods=['GET','POST'])
def registration():
    return render_template('registration.html')


@app.route('/send_email_student')
def send_email_student():
    global date,time
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'hall_allocation_with_benches.xlsx')
    data = pd.read_excel(file_path)
    for _, rec in data.iterrows():
        if rec['Email'] == None :  
            continue
        msg = Message(
            subject='Seating Arrangement for the exam ' + rec['Subject'], 
            sender='omc2651@gmail.com',  # Ensure this matches MAIL_USERNAME
            recipients=[rec['Email']]  # Replace with actual recipient's email
        )
        msg.body = f"""Dear {rec['Student Name']},
        You have been allocated Room {rec['Classroom']} for the {rec['Subject']} Exam on {date} at {time}. Your assigned seat is on the {rec['Bench Number']} bench. Kindly ensure you arrive at your allocated room at least 5 minutes before the exam begins.
        Best regards,
        Examination Coordinator"""
        mail.send(msg)
    return render_template('allocation.html')

@app.route('/send_email_faculty')
def send_email_faculty():
    global date,time
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'Teacher Invigilation.xlsx')
    data = pd.read_excel(file_path)
    for _, rec in data.iterrows():
        if pd.isna(rec['Email']) or not rec['Email'].strip():  # Skip if email is None or empty
            continue
        msg = Message(
            subject= f"Invigilation for the exam dated on {date}", 
            sender='omc2651@gmail.com',  # Ensure this matches MAIL_USERNAME
            recipients=[rec['Email']]  # Replace with actual recipient's email
        )
        msg.body = f"Dear {rec['Name']},\n You have been allocated Room {rec['Classroom']} for the invigilation on {date} at {time}. Kindly ensure you arrive at your allocated room at least 5 minutes before the exam begins.\n Best regards,\n Examination Coordinator"
        mail.send(msg)
    return render_template('allocation.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'classrooms' not in request.files:
        return "Classroom file is not selected"
    elif 'teachers' not in request.files:
        return "Teacher file is not selected"
    elif 'students' not in request.files:
        return "Student file is not selected"
    classroom_file = request.files['classrooms']
    teacher_file = request.files['teachers']
    student_file = request.files['students']
    global date 
    date = request.form['date']
    global time
    time = request.form['time']

    classroom_path = os.path.join(app.config['UPLOAD_FOLDER'], classroom_file.filename)
    teacher_path = os.path.join(app.config['UPLOAD_FOLDER'], teacher_file.filename)
    student_path = os.path.join(app.config['UPLOAD_FOLDER'], student_file.filename)

    classroom_file.save(classroom_path)
    teacher_file.save(teacher_path)
    student_file.save(student_path)

    classrooms = load_file_data(classroom_path)
    teachers = load_file_data(teacher_path)
    students = load_file_data(student_path)

    allocated_data,teacher_invigilation = allocate_students_to_benches(students, classrooms, teachers)
    if(len(allocated_data) == 0):
        return err
        
    output_seating = 'hall_allocation_with_benches.xlsx'
    output_invigilation = "Teacher Invigilation.xlsx"
    Invigilation_path = save_allocation_to_excel(teacher_invigilation,output_invigilation)
    output_path = save_allocation_to_excel(allocated_data, output_seating)
    
    return render_template(
        'allocation.html', 
        allocated_data=allocated_data,
        invigilation = teacher_invigilation, 
        seating_arrangement=url_for('download_file', filename=output_seating),
        invigilation_arrangement=url_for('download_file',filename=output_invigilation))







# New route to serve the search page
@app.route('/open_search_page')
def open_search_page():
    return render_template('search.html')








# Route for searching student or teacher allocation
@app.route('/search_allocation', methods=['POST'])
def search_allocation():
    user_type = request.form.get('user_type')  # Get whether it's a student or teacher
    reg_no_or_id = request.form.get('reg_no_or_id')  # Get the entered reg number or teacher name/ID

    # Load the previously generated allocation Excel
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'hall_allocation_with_benches.xlsx')
    data = pd.read_excel(file_path)

    # Logic for searching based on user type
    if user_type == 'student':
        result = data[data['Reg No'].astype(str) == reg_no_or_id]
    elif user_type == 'teacher':
        result = data[data['Teacher Name'].str.contains(reg_no_or_id, case=False, na=False)]

    # Check if the result is found and return the appropriate page
    if result is not None and not result.empty:
        return render_template('search_results.html', allocated_data=result.to_dict(orient='records'), message=None)
    else:
        return render_template('search_results.html', allocated_data=[], message="No allocation found for this ID.")








@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)






if __name__ == '__main__':  # Corrected __name__
    app.run(debug=True)
