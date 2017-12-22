from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from content_management import Content
from dbconnect import connection
from functools import wraps
import datetime
import time


mydate = datetime.date(1943,3, 13)

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

TOPIC_DICT = Content()

app = Flask(__name__)
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('dashboard'))

    return wrap

@app.route('/',methods =["GET","POST"])
def homepage():
        return render_template("main.html")


    


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Required(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

class TaskForm(Form):
    taskname = TextField('Task  name', [validators.Length(min=4, max=20)])
    category = TextField('Category', [validators.Length(min=6, max=50)])
    description = TextField('Description', [validators.Length(min=6, max=5000)])
    mobile = TextField('Mobile Number', [validators.Length(min=6, max=50)])   
		





@app.route('/dashboard/', methods=["GET","POST"])

def dashboard():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            

            data = c.execute("SELECT * FROM users WHERE username = (%s)",[thwart(request.form['username'])])
                             
            
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("dashboard.html",TOPIC_DICT=TOPIC_DICT, error=error)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        flash(error)
        return render_template("dashboard.html",TOPIC_DICT=TOPIC_DICT)  
		
		
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = (form.username.data)
            email = (form.email.data)
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",[thwart(username)])

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",[thwart(username),thwart(password), thwart(email), thwart("/abc/")])
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username  

                return redirect(url_for("dashboard"))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))



@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('dashboard'))


@app.route('/slashboard/')
def slashboard():
    try:
               

                 
        return render_template("dashboard.html", TOPIC_DICT = shamwow)
    except Exception as e:
	    return render_template("500.html", error = str(e))


@app.route('/report/' ,methods=["GET","POST"])
@login_required
def report():
    try:
        username=session['username']

        c, conn = connection()
        if request.method == "POST":
                    c.execute("INSERT INTO report(username,time,date) VALUES (%s,%s,SYSDATE())",[thwart(username),thwart(timestamp)])
                    conn.commit()
                    flash("YOU HAVE REPORTED!")
                    c.close()
                    conn.close()
                    gc.collect()
                    return redirect(url_for("dashboard"))
                      
        return render_template("report.html")        
                   
             
         
    except Exception as e:
        
	    return render_template("report.html", error = str(e))		


        
                      
     




@app.route('/check/' ,methods=["GET","POST"])
@login_required
def check():
    username=session['username']
    try:
        c, conn = connection()
        data = c.execute("SELECT  * FROM report WHERE username = (%s)   ",[thwart(username)])
        data = c.fetchall()
        
        
          
        
        

        conn.commit()
        
        c.close()
        conn.close()
        gc.collect()
        

            
            
        
                      
        return render_template("check.html",data=data)        
                   
             
         
    except Exception as e:
        
	    return render_template("check.html", error = str(e))	



@app.route('/task/' ,methods=["GET","POST"])
@login_required
def task():
    try:
        username=session['username']
        form = TaskForm(request.form)

        if request.method == "POST" and form.validate():
            taskname  = (form.taskname.data)
            category = (form.category.data)
            description = (form.description.data)
            mobile = (form.mobile.data)
            
            c, conn = connection()
            c.execute("INSERT INTO tasks (username,taskname, genre, description,mobile) VALUES (%s,%s, %s, %s, %s)",[thwart(username),thwart(taskname),thwart(category), thwart(description), thwart(mobile)])
            conn.commit()
            flash("Task Submitted!")
            c.close()
            conn.close()
            gc.collect()

            

        return render_template("task.html",form=form)        
                   
             
         
    except Exception as e:
        
	    return render_template("dashboard.html", error = str(e))		



@app.route('/performance/' ,methods=["GET","POST"])
@login_required
def performance():
    username=session['username']
    try:
        c, conn = connection()
        data = c.execute("SELECT  * FROM tasks WHERE username = (%s)  ",[thwart(username)])
        data = c.fetchall()
        
        
          
        
        

        conn.commit()
        
        c.close()
        conn.close()
        gc.collect()
        

            
            
        
                      
        return render_template("performance.html",data=data)        
                   
             
         
    except Exception as e:
        
	    return render_template("performance.html", error = str(e))   

                   
             
   


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
