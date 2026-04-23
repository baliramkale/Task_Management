import sqlite3
con=sqlite3.connect("task.db")
cur=con.cursor()
cur.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT,fullname varchar(100),email varchar(100),password varchar(20))")

cur.execute("""
     CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
         description TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
""")
cur.execute("ALTER TABLE tasks add column email varchar(50)")
cur.execute("ALTER TABLE tasks drop column colum")
cur.execute("""
        SELECT id, description, created_at 
        FROM tasks 
        WHERE email = ? 
        ORDER BY created_at ASC
    """)
tasks = cur.fetchall()
con.close()

cur.execute('CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT,descripton varchar(60),created_at DATE)')
cur.execute("CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT,description varchar(5000),created_at DATE)")

con.commit()
con.close()
