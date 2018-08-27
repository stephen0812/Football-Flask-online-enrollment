from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/DS/Desktop/base.db'
app.config['SECRET_KEY'] = "SOME VAL"
db = SQLAlchemy(app)

db.create_all()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
def getLoginDetails():
    with sqlite3.connect('base.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = " + str(userId))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems) 

@app.route("/")
def root():
    return render_template('Home.html')
@app.route("/about")
def about():
    return render_template('About.html')
@app.route("/Testi")
def Testi():
    return render_template('Testi.html')

@app.route("/contactus")
def contactus ():
    return render_template('Contact.html')

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_valid(username,password):
            session['username'] = username
            return redirect(url_for('enrollForm'))
        else:
            return "invalid ok va"
    return render_template('login.html')


def is_valid(username, password):
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    cur.execute('SELECT username, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == username and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        username = request.form['username']
        

        with sqlite3.connect('base.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, username) VALUES (?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, username))
                con.commit()
                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


@app.route("/enroll", methods = ['GET', 'POST'])
def enrollment():
    if request.method == 'POST':
        email = request.form['email']

        username = request.form['username']

        number = request.form['number']

        address = request.form['address']

        month = request.form['month']

        price = request.form['price']
        age = request.form['age']
        gender = request.form['gender']	
        with sqlite3.connect('base.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO last(email, username,number,address,month,price,age,gender) VALUES (?,?,?,?,?,?,?,?)', (email,username,number,address,month,price,age,gender))
                con.commit()
                msg = "Registered Successfully"
            except: 
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("last.html", error=msg)
    
@app.route("/enrollmentForm")
def enrollForm():
     return render_template("last.html")



if __name__=='__main__':
    app.run(debug=True)


