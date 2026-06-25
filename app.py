from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template("dashboard.html", username=username)

        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Email already registered."

        cursor.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template("register.html")

    

@app.route("/apply/<job_title>")
def apply(job_title):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM applications WHERE username=? AND job_title=?",
        ("osheen", job_title)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "You have already applied for this job."

    cursor.execute(
        "INSERT INTO applications(username, job_title, status) VALUES(?, ?, ?)",
        ("osheen", job_title, "Pending")
    )

    conn.commit()
    conn.close()

    return f"Successfully Applied for {job_title}"


@app.route("/applications")
def applications():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT job_title, status FROM applications WHERE username=?",
    ("osheen",)
)

    jobs = cursor.fetchall()

    conn.close()

    return render_template(
        "applications.html",
        jobs=jobs
    )
@app.route("/upload_resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        resume = request.files["resume"]

        resume.save(
            "uploads/" + resume.filename
        )

        return "Resume Uploaded Successfully"

    return render_template("upload_resume.html")
@app.route("/logout")
def logout():
    return redirect("/login")
@app.route("/admin")
def admin():

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        students=students,
        applications=applications
    )
@app.route("/approve/<int:id>")
def approve(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status=? WHERE id=?",
        ("Accepted", id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")
@app.route("/reject/<int:id>")
def reject(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status=? WHERE id=?",
        ("Rejected", id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)
