from db_config import conn
from flask import Flask, request, render_template
import qrcode
from pyzbar.pyzbar import decode
import psycopg2

app = Flask(__name__)


def receiver_function(scanned_qr_code):
    try:
        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Fetch item details from the PostgreSQL database using the unique identifier (item name in this case)
        cursor.execute("SELECT * FROM items WHERE item_name = %s", (scanned_qr_code,))
        item_details = cursor.fetchone()

        # Close communication with the PostgreSQL database
        cursor.close()

        return item_details

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

    finally:
        # Close the database connection outside of the try-except block
        if conn is not None:
            conn.close()


@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    if request.method == "POST":
        scanned_qr_code = request.form["qr_code"]

        # Call receiver function to fetch item details from the database
        item_details = receiver_function(scanned_qr_code)

        if item_details:
            return render_template("confirmation.html", item_details=item_details)
        else:
            return "Item not found!"

    return render_template("scanner.html")


if __name__ == "__main__":
    app.run(debug=True)
