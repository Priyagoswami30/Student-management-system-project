from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env (optional)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

# MongoDB connection string - change to your own.
# For local MongoDB: mongodb://localhost:27017/student_db
# For Atlas: mongodb+srv://<user>:<password>@cluster0.mongodb.net/student_db?retryWrites=true&w=majority
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/student_db")


mongo = PyMongo(app)
db = mongo.db
students_coll = db.students

# Home / list students with optional search
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    if q:
        # search by name or roll or class
        query = {"$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"roll": {"$regex": q, "$options": "i"}},
            {"class": {"$regex": q, "$options": "i"}}
        ]}
        students = list(students_coll.find(query).sort("name", 1))
    else:
        students = list(students_coll.find().sort("name", 1))
    return render_template("index.html", students=students, q=q)

# Add new student (GET shows form, POST creates)
@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll", "").strip()
        sclass = request.form.get("class", "").strip()
        email = request.form.get("email", "").strip()
        age = request.form.get("age", "").strip()

        # basic validation
        errors = []
        if not name:
            errors.append("Name is required.")
        if not roll:
            errors.append("Roll number is required.")
        # roll uniqueness check
        if students_coll.find_one({"roll": roll}):
            errors.append("Roll number already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            # re-render with entered values
            return render_template("add_student.html",
                                   name=name, roll=roll, sclass=sclass, email=email, age=age)

        student = {
            "name": name,
            "roll": roll,
            "class": sclass,
            "email": email,
            "age": int(age) if age.isdigit() else None
        }
        students_coll.insert_one(student)
        flash("Student added successfully.", "success")
        return redirect(url_for("index"))
    return render_template("add_student.html")

# View single student
@app.route("/students/<id>")
def view_student(id):
    student = students_coll.find_one({"_id": ObjectId(id)})
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("index"))
    return render_template("view_student.html", student=student)

# Edit student
@app.route("/students/<id>/edit", methods=["GET", "POST"])
def edit_student(id):
    student = students_coll.find_one({"_id": ObjectId(id)})
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll", "").strip()
        sclass = request.form.get("class", "").strip()
        email = request.form.get("email", "").strip()
        age = request.form.get("age", "").strip()

        errors = []
        if not name:
            errors.append("Name is required.")
        if not roll:
            errors.append("Roll number is required.")

        existing = students_coll.find_one({"roll": roll, "_id": {"$ne": ObjectId(id)}})
        if existing:
            errors.append("Another student with this roll number already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("edit_student.html", student=student)

        update = {
            "name": name,
            "roll": roll,
            "class": sclass,
            "email": email,
            "age": int(age) if age.isdigit() else None
        }
        students_coll.update_one({"_id": ObjectId(id)}, {"$set": update})
        flash("Student updated successfully.", "success")
        return redirect(url_for("view_student", id=id))

    return render_template("edit_student.html", student=student)

# Delete student
@app.route("/students/<id>/delete", methods=["POST"])
def delete_student(id):
    students_coll.delete_one({"_id": ObjectId(id)})
    flash("Student deleted.", "info")
    return redirect(url_for("index"))

# Simple API endpoint returning JSON (optional)
@app.route("/api/students")
def api_students():
    students = list(students_coll.find())
    for s in students:
        s["_id"] = str(s["_id"])
    return {"students": students}

if __name__ == "__main__":
    app.run(debug=True)
