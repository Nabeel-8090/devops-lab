from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {}

# REGISTER USER
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    full_name = data.get("full_name")
    username = data.get("username")
    password = data.get("password")

    if not full_name or not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    if username in users:
        return jsonify({"error": "Username already exists."}), 400

    users[username] = {"full_name": full_name, "password": password}
    return jsonify({"message": f"User {username} registered successfully."}), 201

# LOGIN USER
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users:
        return jsonify({"error": "User not found."}), 404

    if users[username]["password"] != password:
        return jsonify({"error": "Wrong password."}), 401

    session["username"] = username
    return jsonify({"message": f"User {username} logged in successfully."}), 200

# DASHBOARD
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    username = session["username"]
    full_name = users[username]["full_name"]
    return jsonify({"username": username, "full_name": full_name}), 200

# PROFILE
@app.route("/profile/<username>", methods=["GET"])
def profile(username):
    if username in users:
        user = users[username]
        return jsonify({"username": username, "full_name": user["full_name"]}), 200
    return jsonify({"error": "User not found."}), 404

# LOGOUT
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out successfully."}), 200

# MAIN
if __name__ == "__main__":
    app.run(debug=True)