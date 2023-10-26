from db_config import conn
from flask import Flask, request, render_template
import qrcode
import psycopg2

app = Flask(__name__)


def sender_function(item_name, grant_code, dispatcher_name):
    try:
        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Insert data into the PostgreSQL database
        cursor.execute(
            "INSERT INTO items (item_name, grant_code, dispatcher_name) VALUES (%s, %s, %s)",
            (item_name, grant_code, dispatcher_name),
        )

        # Commit the transaction
        conn.commit()

        # Close communication with the PostgreSQL database
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        # Close the database connection outside of the try-except block
        if conn is not None:
            conn.close()


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/sender", methods=["GET", "POST"])
def sender():
    if request.method == "POST":
        item_name = request.form["item_name"]
        grant_code = request.form["grant_code"]
        dispatcher_name = request.form["dispatcher_name"]

        # Call sender function to insert data into the database
        sender_function(item_name, grant_code, dispatcher_name)

        return render_template("success.html", item_name=item_name)

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
