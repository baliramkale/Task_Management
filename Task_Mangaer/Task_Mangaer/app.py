from flask import *
import sqlite3    
app=Flask(__name__)
app.secret_key="baliram"
from datetime import date

# <---LOGIN--->

@app.route("/")
def home():
    return render_template("login.html")
# <---REGISTER--->
@app.route('/register')
def register():
    return render_template("registration.html")

# <---REGISTRATION--->

@app.route("/registration",methods=["POST","GET"])
def registration():
    if request.method=="POST":
        nm = request.form["fullname"]
        em = request.form["email"]
        ps = request.form["password"]
        
        con = sqlite3.connect("task.db")    # Data Base Connectivity
        cur = con.cursor()
        cur.execute("insert into student(fullname,email,password)values(?,?,?)",(nm,em,ps))
        con.commit()
        con.close()
        
        return redirect(url_for("home"))
  
    
# <---LOGINCHECK--->

@app.route("/logincheck",methods=["POST","GET"])
def logincheck():
    if request.method=='POST':
         em= request.form["email"]
         ps= request.form["password"]
         con=sqlite3.connect("task.db")   
         cur=con.cursor()
         cur.execute("select * from student where email=? and password=?",(em,ps))
         student = cur.fetchall()    
         if student:
            session["username"] = em   # Session Start --->
            return redirect(url_for("dashboard"))
         else:
            return redirect(url_for("register"))
        
# <---DASHBOARD--->

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
     
# <---ADDTASK--->
  
@app.route("/addtask")
def addtask():
    return render_template("addtask.html")

# <---ADDINGTASK--->

@app.route("/addingtask",methods=["POST","GET"])
def addingtask():
    if request.method == "POST":
        task = request.form["task"]
        email =  session["username"]
        con = sqlite3.connect("task.db")
        cur=con.cursor()
        
        cur.execute("INSERT INTO tasks(description,created_at,email)VALUES (?,?,?)",(task,date.today(),email))
        con.commit()
        return redirect(url_for("dashboard"))

# <---VIVEWTASK--->

@app.route("/viewtask")
def viewtask():
    con = sqlite3.connect("task.db")
    cur=con.cursor()
    email =  session["username"]
    cur.execute("SELECT id ,description,created_at FROM tasks WHERE email = ? ",[email])
    tasks = cur.fetchall()
    con.close()
    return render_template("viewtask.html",tasks = tasks)
    
# <---DELETE_TASK--->

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    con = sqlite3.connect("task.db")
    cur = con.cursor()
    cur.execute("SELECT description FROM tasks WHERE id = ?", [task_id])
    task = cur.fetchone()
    if task:
        cur.execute("INSERT INTO history (description, created_at) VALUES (?, ?)", (task[0], date.today()))
        cur.execute("DELETE FROM tasks WHERE id = ?", [task_id])
        con.commit()
        con.close()
    return redirect(url_for('viewtask'))

# <---HISTORY--->
@app.route('/history',methods=['GET', 'POST'])
def history():
    tasks = []  
    con = sqlite3.connect("task.db")  
    cur = con.cursor() 
    
    if request.method == "POST":
        start = request.form["startdate"] 
        end = request.form["enddate"] 
        selected_date = True 
        if start and end:
            cur.execute('SELECT id,description, created_at FROM history WHERE created_at BETWEEN ? AND ?' ,(start, end))
            tasks = cur.fetchall()
    return render_template("history.html", tasks=tasks,)

# <---LOGOUT--->

@app.route("/logout")
def logout():
    session.pop("username",None)     #   <---Session End
    return redirect(url_for("home"))


if __name__==("__main__"):
    app.run(debug=True) 
    
#<-------------------------------------------------------THE-----END------------------------------------------------------>