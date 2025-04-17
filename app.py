from flask import Flask, render_template, request, redirect, session, url_for, flash
app = Flask(__name__)
app.secret_key = 'secretkey'

admin_users = {
    "alexakate": {
        "name": "Alexa Kate B. Mamato",
        "email": "alexa@example.com",
        "password": "yourpassword123"
    },
    # You can add more admins here
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
        admin_id = request.form['admin_id']
        password = request.form['password']

        user = admin_users.get(admin_id)
        if user and user['password'] == password:
            session['admin_name'] = user['name']
            return redirect(url_for('admin_home'))
        else:
            flash("Invalid Admin ID or Password. Please try again.")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')


#FORGOT PASSWORD
@app.route('/admin/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    reset_stage = False
    admin_info = None

    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            if username in admin_users:
                session['reset_user'] = username
                admin_info = admin_users[username]
                reset_stage = True
            else:
                flash("No account found with that username.")
                return redirect(url_for('forgot_password'))
        else:
            # This means we're resetting the password
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if new_password != confirm_password:
                flash("Passwords do not match.")
                reset_stage = True
                admin_info = admin_users.get(session.get('reset_user'))
            else:
                admin_users[session['reset_user']]['password'] = new_password
                flash("Password successfully reset.")
                session.pop('reset_user', None)
                return redirect(url_for('admin_login'))

    return render_template(
        'admin_forgot_password.html',
        reset_stage=reset_stage,
        admin_info=admin_info
    )



#ADMIN HOMEPAGE
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

#ADMIN SIGN UP
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
