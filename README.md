# StudentPulse

StudentPulse is a Flask web application for managing student records with MongoDB. It supports listing, searching, adding, viewing, editing, deleting, and exporting student data through a small JSON API
## Features

- Add student records with roll number, name, class, email, and age
- Search students by name, roll number, or class
- View individual student details
- Edit and delete existing records
- JSON endpoint at `/api/students`
- MongoDB Atlas and local MongoDB support
- Render deployment configuration included

## Tech Stack

- Python
- Flask
- MongoDB
- PyMongo
- Jinja templates
- Gunicorn for production

## Project Structure

```text
.
+-- app.py
+-- requirements.txt
+-- render.yaml
+-- static/
|   +-- style.css
+-- templates/
    +-- add_student.html
    +-- base.html
    +-- edit_student.html
    +-- index.html
    +-- view_student.html
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your-secret-key
MONGO_URI=mongodb://127.0.0.1:27017/student_db
MONGO_DB_NAME=student_db
```

For MongoDB Atlas, use your Atlas connection string:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>/<database>?retryWrites=true&w=majority
```

## Run Locally

Start the Flask app:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

If your global Python does not have the project packages installed, run with the virtual environment Python directly:

```powershell
.\.venv\Scripts\python.exe app.py
```

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `FLASK_SECRET_KEY` | Yes | Secret key used by Flask sessions and flash messages |
| `MONGO_URI` | Yes | MongoDB connection string |
| `MONGO_DB_NAME` | No | Database name used when `MONGO_URI` does not include one |

## API

Get all students as JSON:

```http
GET /api/students
```

Example response:

```json
{
  "students": [
    {
      "_id": "101",
      "name": "Priya Goswami",
      "roll": "101",
      "class": "12",
      "email": "priya@example.com",
      "age": 18
    }
  ]
}
```

## Deploy on Render

This project includes `render.yaml`.

Before deploying, set these environment variables in Render:

- `FLASK_SECRET_KEY`
- `MONGO_URI`

Render will install dependencies with:

```bash
pip install -r requirements.txt
```

and start the app with:

```bash
gunicorn app:app --workers 3
```
