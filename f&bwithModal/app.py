from flask import Flask, render_template, request, session, jsonify, redirect, url_for#1.create a new flask project(common part- first 2)
import json #2.to use json files
import os #3.to access system

app = Flask(__name__)#1
app.secret_key = "your_secret_key"  # Required for session management

user_file = "users.json"

#function to load users from json
def load_users():
    if not os.path.exists(user_file):
        with open(user_file, "w") as file:
            json.dump([], file)
    
    with open(user_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

#function to save users to json
def save_users(users):
    with open(user_file, "w") as file :
        json.dump(users, file, indent = 4)

#routing to verify the email
@app.route("/verify_email", methods=["POST"])
def verify_email():
    data = request.get_json()
    email = data.get("email")

    users = load_users()
    exists = any(user["email"].lower() == email.lower() for user in users)

    return jsonify({"exists": exists})

@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("new_password")

    users = load_users()

    for user in users:
        if user["email"].lower() == email.lower():
            user["password"] = new_password
            save_users(users)
            return jsonify({"success": True})

    return jsonify({"success": False})

#routing the index page
@app.route('/')#1
def index():
    # """Redirect to login if user is not logged in"""
    if "user_name" not in session:
        return redirect(url_for("log"))
    return render_template("homepage.html", user_name = session["user_name"])
    # def index():#1
    #     return render_template('index.html')#1

#routing to register page
@app.route('/registration')
# def registration():
#     return redirect(url_for("reg")) #automatically searches for the reg()

# @app.route('/reg')
# def reg():
#     return render_template('Registration.html')
def registration():
    return render_template('Registration.html')

#routing to login page
@app.route('/login', methods = ["GET"])
# def login():
#     return redirect(url_for('log'))

# @app.route('/log')
def log():
    return render_template('login.html')

#routing to forgotpassword page
@app.route('/forgotpass')
# def forgotpass():
#     return redirect(url_for('forgot'))

# @app.route('/forgot')
def forgot():
    return render_template('forgotPassword.html')

#routing to signing in process
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()  # Fix: Use request.get_json() instead of request.json()
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    user = next((user for user in users if user["email"].lower() == email), None)

    if user is None or user["password"] != password:
        return jsonify({"message": "Invalid email or password"}), 401
    
    session["user_name"] = user["name"]  # Store user name in session
    return jsonify({"message": "Login Successful"}), 200

#routing to registration process url
@app.route('/register', methods = ["POST"])
def register():
    data = request.json # Get JSON data from the request
    users = load_users()

    # Check if email or phone already exists
    if any(user["email"].lower() == data["email"].lower() for user in users):
        return jsonify({"message": "Email already registered"}), 400
    if any(user["phone"] == data["phone"] for user in users):
        return jsonify({"message": "Phone number is already registered"}), 400
    
    users.append(data)
    save_users(users)

    return jsonify({"message": "User has successfully registered"}), 200

#logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("log"))

#routing to successfully signing in to homepage
@app.route("/homepage")
# def homepage():
#     return redirect(url_for('home'))

# @app.route("/home")
def home():
    if "user_name" not in session:
        return redirect(url_for("log"))
    return render_template("homepage.html", user_name=session["user_name"])

#routing to get data from the json
@app.route('/get_users', methods = ["GET"])
def get_users():
    users = load_users() # Load users from JSON file
    sorted_users = sorted(users, key= lambda x: x["name"].lower()) # Sort by name (case-insensitive)
    return jsonify(sorted_users) # Send user data as JSON

if __name__ == '__main__':#1
    app.run(debug=True)#1