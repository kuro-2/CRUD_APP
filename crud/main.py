from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector # Importing the mysql connector library

app = Flask(__name__) # Creating the Flask app instance 
app.secret_key = 'your_secret_key'  # this is required for flash messages to work properly

# SQL CONFIGURATION DETAILS
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",  
    database="emp_db"
)

@app.route('/') # this is the homepage route 
def index():
    cur = db.cursor()  # Using the db connection we created
    cur.execute("SELECT * FROM employees") # it will execute this SQL query and will show us the data from the employees table
    data = cur.fetchall()# it will fetch all the data from the employees table
    cur.close()
    return render_template('index.html', employees=data)  # Changed 'actors' to 'employees'

# This route is for inserting data (CREATE operation)
@app.route('/add_emp', methods=['POST'])
def add_emp():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        emp_email = request.form['emp_email']
        cur = db.cursor()  # Using the db connection we created
        cur.execute("INSERT INTO employees (emp_id, emp_name, emp_email) VALUES (%s, %s, %s)", 
                   (emp_id, emp_name, emp_email))
        db.commit()  # Using db instead of mysql.connection
        flash('Employee added successfully')
        return redirect(url_for('index'))

# This route is for updating data (UPDATE operation)
@app.route('/edit/<string:emp_id>', methods=['POST', 'GET'])
def edit_emp(emp_id):
    cur = db.cursor()
    
    if request.method == 'POST':
        new_emp_id = request.form['emp_id']
        emp_name = request.form['emp_name']
        emp_email = request.form['emp_email']
        
        cur.execute("""
            UPDATE employees
            SET emp_id = %s,
            emp_name = %s,
            emp_email = %s
            WHERE emp_id = %s
        """, (new_emp_id, emp_name, emp_email, emp_id))
        db.commit()
        flash('Employee updated successfully')
        return redirect(url_for('index'))# redirects to the homepage

    cur.execute("SELECT * FROM employees WHERE emp_id = %s", (emp_id,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', employee=data[0])# returns the edit.html page with the data of the employee to edit the data

# This route is for deleting data (DELETE operation)
@app.route('/delete/<string:emp_id>')
def delete_emp(emp_id):
    cur = db.cursor()
    cur.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
    db.commit()
    flash('Employee deleted successfully')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)