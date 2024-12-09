from flask import Flask, render_template, redirect, request
import sqlite3

con = sqlite3.connect("database.db")

app =  Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def init():
    if request.method == "POST":
        try:
            user = request.form['user']
            password = request.form['password']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (user, password) VALUES (?, ?)", (user, password))
                con.commit()
                msg = "Thanks for joining our site"
        except:
            con.rollback()
            existing_user = cur.fetchone()
            if existing_user:
                return render_template("register.html", error="user already exists")
            msg = "error at inserting the information into the database"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])      
def login():
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        
        try:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM user WHERE user = ? AND password = ?", (user, password))
                row = cur.fetchone()
                
                if row:
                    print("Login válido. Redirecionando para home.")
                    return redirect("/home", code=302) 
                else:
                    print("Credenciais inválidas. Exibindo erro.")
                    return render_template("login.html", error="Invalid credentials")
        
        except sqlite3.Error as e:
            return render_template("login.html", error="Database error: " + str(e))  
    
    
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)