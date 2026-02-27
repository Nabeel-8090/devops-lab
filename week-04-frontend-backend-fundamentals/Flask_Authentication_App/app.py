from flask import Flask, request, url_for, session, render_template, redirect

app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=['GET', "POST"])
def register():
    error = None
    if request.method == "POST":
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        password = request.form.get("password")

        if not full_name or not username or not password:
            error = "All fields are required."

        elif username in users:
            error = "Username already exists."

        else:
            users[username] = {
                "full_name": full_name,
                "password": password
            }
    return render_template("register.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username not in users:
            error = "user not found."

        elif users[username]["password"] != password:
            error = "Wrong password."

        else:
            session["username"] = username
            return redirect(url_for("dashboard"))
        
    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))   
    username = session["username"]
    full_name = users[username]["full_name"]

    return render_template("dashboard.html", full_name=full_name)


@app.route("/profile/<username>")
def profile(username):
    if username in users:
        user = users[username]
        return render_template("profile.html", user=user, username=username)
    else:
        return render_template("profile.html", user=None, username=username)
    
     
@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)