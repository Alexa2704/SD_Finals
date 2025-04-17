from flask import Flask, render_template, request, redirect, session, url_for, flash
app = Flask(__name__)
app.secret_key = 'secretkey'

admin_users = {
    "M2023-00056": {"name": "Alexa Kate B. Mamato", "password": "1234567890"}
}

student_users = {}

# Role Selection Page
@app.route('/')
def home():
    return render_template('select_role.html')

# ADMIN ROUTES
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        session['admin_name'] = admin_name
        return redirect(url_for('admin_home'))
    return render_template('admin_login.html')

@app.route('/admin/home')
def admin_home():
    admin_name = session.get('admin_name', 'Admin')  # default to 'Admin' if not set
    return render_template('admin_home.html', admin_name=admin_name)

@app.route('/attendance')
def attendance_page():
    return render_template('index.html', active_tab='attendance')

@app.route('/quiz')
def quiz_page():
    return render_template('index.html', active_tab='quiz')

@app.route('/exam')
def exam_page():
    return render_template('index.html', active_tab='exam')


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', records=records)


# Empty data store (you can replace this with a real database later)
records = []
student_number = 1

# ADMIN DASHBOARD (Displaying Attendance)
# ADD STUDENT RECORD (Including Attendance)
@app.route('/admin/add', methods=["POST"])
def add_student():
    global student_number
    student_id = f"{student_number:05d}"
    name = request.form['name']
    attendance = request.form['attendance']
    quiz_score = int(request.form['quiz_score'])
    exam_score = int(request.form['exam_score'])

    records.append({
        "id": student_id,
        "name": name,
        "attendance": attendance,
        "quiz_score": quiz_score,
        "exam_score": exam_score
    })
    student_number += 1
    return redirect(url_for('admin_dashboard'))

# DELETE STUDENT RECORD
@app.route('/admin/delete/<student_id>')
def delete(student_id):
    global records
    records = [r for r in records if r["id"] != student_id]
    return redirect(url_for('admin_dashboard'))

# EDIT STUDENT RECORD
@app.route('/admin/edit/<student_id>', methods=["GET", "POST"])
def edit(student_id):
    record = next((r for r in records if r["id"] == student_id), None)
    if request.method == "POST":
        if record:
            record["name"] = request.form["name"]
            record["attendance"] = request.form["attendance"]
            record["quiz_score"] = int(request.form["quiz_score"])
            record["exam_score"] = int(request.form["exam_score"])
        return redirect(url_for('admin_dashboard'))
    return render_template("edit.html", record=record)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
        else:
            admin_users[username] = {
                "full_name": full_name,
                "email": email,
                "username": username,
                "password": password
            }
            # Redirect to Admin Home Page after successful signup
            return redirect(url_for('admin_home'))
    return render_template('admin_signup.html')


# STUDENT ROUTES
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form['student_id']
        password = request.form['password']
        user = student_users.get(student_id)
        if user and user['password'] == password:
            return f"Welcome, {user['username']}!"
        else:
            flash('Invalid username or password')
    return render_template('student_login.html')

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        school_email = request.form['school_email']
        student_id = request.form['student_id']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
        else:
            student_users[student_id] = {
                "full_name": full_name,
                "school_email": school_email,
                "username": username,
                "password": password
            }
            return redirect(url_for('student_login'))
    return render_template('student_signup.html')

if __name__ == '_main_':
    app.run(debug=True)
