from flask import Flask, render_template, request
from sender import sender_function  # Import your sender side function
from receiver import receiver_function  # Import your receiver side function

app = Flask(__name__)


@app.route("/sender", methods=["GET", "POST"])
def sender():
    if request.method == "POST":
        # Call your sender function here
        sender_function(
            request.form["item_name"],
            request.form["grant_code"],
            request.form["dispatcher_name"],
        )
    return render_template("form.html")


@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    if request.method == "POST":
        # Call your receiver function here
        receiver_function(request.form["qr_code"])
    return render_template("scanner.html")


if __name__ == "__main__":
    app.run(debug=True)
