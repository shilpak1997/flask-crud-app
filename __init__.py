from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb
import csv

with open('student.csv', 'r') as readobj:
    read=csv.reader(readobj)
    rows=list (read)




app = Flask(__name__)
app.secret_key = 'welcome'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ra'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'raju'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', todos=data )

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        description = request.form['description']
        assignedby = request.form['assignedby']
        assigndate = request.form['assigndate']
        duedate = request.form['duedate']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (title, description, assignedby, assigndate, duedate) VALUES (%s, %s, %s, %s, %s)", (title, description, assignedby, assigndate, duedate))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        title = request.form['title']
        description = request.form['description']
        assignedby = request.form['assignedby']
        assigndate = request.form['assigndate']
        duedate = request.form['duedate']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET title=%s, description=%s, assignedby=%s, assigndate=%s, duedate=%s
               WHERE id=%s
            """, (title, description, assignedby, assigndate, duedate, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))









if __name__ == "__main__":
    app.run(debug=True)
