from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'
  
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'bharatreads'
  
  
mysql = MySQL(app)

@app.route('/')
@app.route('/login_customer',methods =['GET', 'POST'])
def login_customer():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s AND password = %s', (username, password, ))
        customer = cursor.fetchone()
        if customer:
            session['loggedin'] = True
            session['id'] = customer['id']
            session['username'] = customer['username']
            msg = 'Logged in successfully !'
            session['user'] = customer
            return redirect(url_for('index_customer'))
        else:
            msg ='Incorrect Username/Password !'
    return render_template('login_customer.html',msg=msg)

@app.route('/login_staff',methods =['GET', 'POST'])
def login_staff():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE username = %s AND password = %s', (username, password, ))
        staff = cursor.fetchone()
        if staff:
            session['loggedin'] = True
            session['id'] = staff['id']
            session['username'] = staff['username']
            msg = 'Logged in successfully !'
            session['user'] = staff
            return redirect(url_for('index_staff'))
        else:
            msg ='Incorrect Username/Password !'
    return render_template('login_staff.html',msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('user',None)
   return redirect(url_for('login_customer'))

@app.route('/register_customer',methods=['GET','POST'])
def register_customer():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form :
        username =request.form['username']
        password =request.form['password']
        name = request.form['name']
        contact_no =request.form['contact_no']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username =%s',(username,))
        customer = cursor.fetchone()
        if customer:
            msg = 'Username already exists!'
        else:
            if contact_no:
                cursor.execute('INSERT INTO customers(username,password,name,contact_no) VALUES(%s,%s,%s,%s)',((username,password,name,contact_no,)))
            else:
                cursor.execute('INSERT INTO customers(username,password,name) VALUES(%s,%s,%s)',((username,password,name,)))
            mysql.connection.commit()
            msg = 'Succesfully Registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register_customer.html',msg=msg)

@app.route('/register_staff',methods=['GET','POST'])
def register_staff():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form :
            username =request.form['username']
            password =request.form['password']
            name = request.form['name']
            contact_no =request.form['contact_no']
            designation = request.form['designation']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM staff WHERE username =%s',(username,))
            new_staff = cursor.fetchone()
            if new_staff:
                msg = 'Username already exists!'
            else:
                cursor.execute('INSERT INTO staff(username,password,name,contact_no,designation) VALUES(%s,%s,%s,%s,%s)',((username,password,name,contact_no,designation,)))
                mysql.connection.commit()
                msg = 'Succesfully Registered!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('register_staff.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/add_new_book',methods=['GET','POST'])
def add_new_book():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'title' in request.form and 'stock' in request.form and 'author' in request.form and 'genre' in request.form and 'sale_price' in request.form:
            title = request.form['title']
            stock = request.form['stock']
            author = request.form['author']
            genre = request.form['genre']
            sale_price = request.form['sale_price']
            
            if(request.form['edition']):
                edition = request.form['edition']
            else:
                edition = 0
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM newbook WHERE title=%s and author = %s and genre =%s and sale_price = %s  ',(title,author,genre,sale_price,))
            newbook = cursor.fetchone()
            if newbook:
                cursor.execute('UPDATE newbook SET stock = %s + %s WHERE title = %s and author = %s and genre = %s and edition = %s and sale_price =%s',(stock,newbook['stock'],title,author,genre,edition,int(sale_price),) )
                mysql.connection.commit()
                msg = 'Succesfully added'
            else:
                cursor.execute('INSERT INTO newbook(title,author,genre,edition,stock,sale_price) VALUES(%s,%s,%s,%s,%s,%s)',(title,author,genre,edition,stock,sale_price,))
                mysql.connection.commit()
                msg = 'Succesfully added'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('add_new_book.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/buy_old_book',methods=['GET','POST'])
def buy_old_book():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'title' in request.form and 'stock' in request.form and 'author' in request.form and 'genre' in request.form and 'sale_price' in request.form and 'rental_price' in request.form and 'cost_price' in request.form and 'purchase_cust_id' in request.form:
            title = request.form['title']
            stock = request.form['stock']
            author = request.form['author']
            genre = request.form['genre']
            sale_price = request.form['sale_price']
            rental_price =request.form['rental_price']
            cost_price = request.form['cost_price']
            purchase_cust_id = request.form['purchase_cust_id']
            if(request.form['edition']):
                edition = request.form['edition']
            else:
                edition = 0

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO oldbook(title,author,genre,edition,stock,sale_price,cost_price,rental_price,purchase_cust_id,purchase_staff_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(title,author,genre,edition,stock,sale_price,cost_price,rental_price,purchase_cust_id,staff['id']))
            mysql.connection.commit()
            msg = 'Succesfully added'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('buy_old_book.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route("/index_staff")
def index_staff():
    if 'loggedin' in session: 
        staff = session['user']
        return render_template("index_staff.html",staff = staff)
    return redirect(url_for('login_staff'))   

@app.route("/index_customer")
def index_customer():
    if 'loggedin' in session: 
        customer = session['user']
        return render_template("index_customer.html",customer = customer)
    return redirect(url_for('login_customer'))  

if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"))