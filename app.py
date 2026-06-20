from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE = "volunteers.json"


def load_data():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()

        if not name or not email or not phone:
            return "All fields are required"

        if not phone.isdigit() or len(phone) != 10:
            return "Phone number must contain exactly 10 digits"

        data = load_data()

        for volunteer in data:
            if volunteer["email"].lower() == email:
                return "Volunteer with this email already exists"

        volunteer = {
            "name": name,
            "email": email,
            "phone": phone
        }

        data.append(volunteer)
        save_data(data)

        return redirect("/volunteers")

    return render_template("add.html")


@app.route("/volunteers")
def volunteers():
    data = load_data()
    total = len(data)

    return render_template(
        "volunteers.html",
        volunteers=data,
        total=total
    )


@app.route("/search")
def search():
    query = request.args.get("query", "").strip().lower()

    data = load_data()

    if query == "":
        return render_template(
            "volunteers.html",
            volunteers=data,
            total=len(data)
        )

    results = [
        volunteer
        for volunteer in data
        if query in volunteer["name"].lower()
    ]

    return render_template(
        "volunteers.html",
        volunteers=results,
        total=len(results)
    )


if __name__ == "__main__":
    app.run(debug=True)