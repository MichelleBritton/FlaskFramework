import os
import json
# Import the Flask class, capital F indicated that is's a class name
from flask import Flask, render_template, request, flash
if os.path.exists("env.py"):
    import env

# Create an instance of this class, the convention is that our variable is called app
# The first argument of the Flask class is the name of the application's module - our package
# Since we are using a single module, we can use __name__ which is a built in Python module
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Flask n eeds to know where to look for templates and static files. Use the route decorator to tell Flask what URL should trigger the function that follows
# In Python a decorator starts with the @ symbol which is also called pie-notation. A decorator is a way of wrapping functions
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    data = []
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", company=data)


@app.route("/about/<member_name>")
def about_member(member_name):
    member = {}
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return render_template("member.html", member=member)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    return render_template("contact.html", page_title="Contact")


@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")

# Use os module from the standard library to get the "IP" environment variable if it exists but set a default if it's not.
# The word 'main' wrapped in double-underscores (__main__) is the name of the default module in Python.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
