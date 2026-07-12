from flask import Flask, render_template, request, redirect, url_for
from flask import session, flash
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "vehicle_rental_secret_key"

DATABASE = "database.db"


# ==========================
# DATABASE CONNECTION
# ==========================

def get_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================
# CREATE TABLES
# ==========================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # USERS

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT,

        email TEXT UNIQUE,

        password TEXT,

        phone TEXT,

        role TEXT DEFAULT 'user'

    )

    """)

    # BOOKINGS

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS bookings(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        booking_id TEXT,

        fullname TEXT,

        mobile TEXT,

        vehicle TEXT,

        booking_date TEXT,

        amount INTEGER,

        payment_method TEXT,

        payment_status TEXT,

        status TEXT,

        created_at TEXT

    )

    """)

    conn.commit()

    conn.close()


create_tables()


# ==========================
# PRICE LIST
# ==========================

PRICE = {

    "Car":2000,

    "Bike":800,

    "Scooter":500

}


# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================
# REGISTER
# ==========================

@app.route("/register")
def register():

    return render_template("register.html")


@app.route("/register_user",methods=["POST"])
def register_user():

    fullname=request.form["fullname"]

    email=request.form["email"]

    password=request.form["password"]

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user=cursor.fetchone()

    if user:

        flash("Email Already Exists")

        conn.close()

        return redirect("/register")

    cursor.execute(

        """

        INSERT INTO users(

        fullname,

        email,

        password,

        phone

        )

        VALUES(?,?,?,?)

        """,

        (

            fullname,

            email,

            password,

            ""

        )

    )

    conn.commit()

    conn.close()

    flash("Registration Successful")

    return redirect("/login")


# ==========================
# LOGIN
# ==========================

@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/login_user",methods=["POST"])
def login_user():

    email=request.form["email"]

    password=request.form["password"]

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM users

        WHERE

        email=?

        AND

        password=?

        """,

        (

            email,

            password

        )

    )

    user=cursor.fetchone()

    conn.close()

    if user:

        session["user"]=user["fullname"]

        session["role"]=user["role"]

        flash("Welcome "+user["fullname"])

        return redirect("/dashboard")

    flash("Invalid Login")

    return redirect("/login")
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully")

    return redirect("/")


# ==========================
# BOOK VEHICLE
# ==========================

@app.route("/book", methods=["POST"])
def book():

    fullname = request.form["fullname"]
    mobile = request.form["mobile"]
    vehicle = request.form["vehicle"]
    booking_date = request.form["booking_date"]

    amount = PRICE.get(vehicle, 0)

    session["booking"] = {
        "fullname": fullname,
        "mobile": mobile,
        "vehicle": vehicle,
        "booking_date": booking_date,
        "amount": amount
    }

    return redirect("/payment")


# ==========================
# PAYMENT PAGE
# ==========================

@app.route("/payment")
def payment():

    if "booking" not in session:
        return redirect("/")

    return render_template(
        "payment.html",
        booking=session["booking"]
    )


# ==========================
# PAYMENT SUCCESS
# ==========================

@app.route("/payment_success", methods=["POST"])
def payment_success():

    if "booking" not in session:
        return redirect("/")

    payment_method = request.form["payment_method"]

    booking = session["booking"]

    booking_id = "VRS" + str(random.randint(10000,99999))

    payment_status = "Paid"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO bookings(

    booking_id,

    fullname,

    mobile,

    vehicle,

    booking_date,

    amount,

    payment_method,

    payment_status,

    status,

    created_at

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """,

    (

        booking_id,

        booking["fullname"],

        booking["mobile"],

        booking["vehicle"],

        booking["booking_date"],

        booking["amount"],

        payment_method,

        payment_status,

        "Approved",

        datetime.now().strftime("%d-%m-%Y %H:%M")

    ))

    conn.commit()

    conn.close()

    session["receipt"] = {

        "booking_id": booking_id,

        "fullname": booking["fullname"],

        "mobile": booking["mobile"],

        "vehicle": booking["vehicle"],

        "booking_date": booking["booking_date"],

        "amount": booking["amount"],

        "payment_method": payment_method,

        "payment_status": payment_status

    }

    session.pop("booking")

    return redirect("/receipt")
# ==========================
# RECEIPT
# ==========================

@app.route("/receipt")
def receipt():

    if "receipt" not in session:
        return redirect("/")

    return render_template(
        "receipt.html",
        receipt=session["receipt"]
    )


# ==========================
# PROFILE
# ==========================

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE fullname=?",
        (session["user"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# ==========================
# BOOKINGS
# ==========================

@app.route("/bookings")
def bookings():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM bookings
        ORDER BY id DESC
        """
    )

    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        "bookings.html",
        bookings=bookings
    )


# ==========================
# SEARCH
# ==========================

@app.route("/search")
def search():

    keyword = request.args.get("keyword")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM bookings

        WHERE

        fullname LIKE ?
        OR
        vehicle LIKE ?
        OR
        booking_id LIKE ?

        ORDER BY id DESC
        """,

        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )

    )

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "bookings.html",
        bookings=data
    )


# ==========================
# DELETE BOOKING
# ==========================

@app.route("/delete/<int:id>")
def delete_booking(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    flash("Booking Deleted Successfully")

    return redirect("/bookings")
# ==========================
# UPDATE BOOKING
# ==========================

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_booking(id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        fullname = request.form["fullname"]
        mobile = request.form["mobile"]
        vehicle = request.form["vehicle"]
        booking_date = request.form["booking_date"]
        status = request.form["status"]

        amount = PRICE.get(vehicle, 0)

        cursor.execute("""

        UPDATE bookings

        SET

        fullname=?,
        mobile=?,
        vehicle=?,
        booking_date=?,
        amount=?,
        status=?

        WHERE id=?

        """,

        (
            fullname,
            mobile,
            vehicle,
            booking_date,
            amount,
            status,
            id
        ))

        conn.commit()

        flash("Booking Updated Successfully")

        conn.close()

        return redirect("/bookings")

    cursor.execute(

        "SELECT * FROM bookings WHERE id=?",

        (id,)

    )

    booking = cursor.fetchone()

    conn.close()

    return render_template(
        "update.html",
        booking=booking
    )


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin")
def admin():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM bookings")

    revenue = cursor.fetchone()[0]

    if revenue is None:
        revenue = 0

    cursor.execute("""

    SELECT *

    FROM bookings

    ORDER BY id DESC

    LIMIT 10

    """)

    recent_bookings = cursor.fetchall()

    conn.close()

    return render_template(

        "admin.html",

        total_users=total_users,

        total_bookings=total_bookings,

        total_revenue=revenue,

        recent_bookings=recent_bookings

    )


# ==========================
# ERROR PAGE
# ==========================

@app.errorhandler(404)
def page_not_found(error):

    return "<h2>404 | Page Not Found</h2>"


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )