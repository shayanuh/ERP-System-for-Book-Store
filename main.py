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
        if request.method == 'POST' and 'title' in request.form  and 'author' in request.form and 'genre' in request.form and 'sale_price' in request.form:
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            sale_price = request.form['sale_price']
            
            if(request.form['edition']):
                edition = request.form['edition']
            else:
                edition = 0
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            cursor.execute('INSERT INTO newbook(title,author,genre,edition,status,sale_price) VALUES(%s,%s,%s,%s,%s,%s)',(title,author,genre,edition,'AVAILABLE',sale_price,))
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
        if request.method == 'POST' and 'title' in request.form and 'author' in request.form and 'genre' in request.form and 'sale_price' in request.form and 'rental_price' in request.form and 'cost_price' in request.form and 'purchase_cust_id' in request.form:
            title = request.form['title']
            status = 'AVAILABLE'
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
            cursor.execute('SELECT * from customers WHERE id =%s',(purchase_cust_id,))
            purchase_customer = cursor.fetchone()
            if( purchase_customer):
                cursor.execute('INSERT INTO oldbook(title,author,genre,edition,status,sale_price,cost_price,rental_price,purchase_cust_id,purchase_staff_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(title,author,genre,edition,status,sale_price,cost_price,rental_price,purchase_cust_id,staff['id']))
                mysql.connection.commit()
                msg = 'Succesfully added'
            else:
                mysql.connection.commit()
                msg = 'Invalid Customer Id'

        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('buy_old_book.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/process_rentals',methods=['GET','POST'])
def process_rentals():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'cust_id' in request.form and 'book_id' in request.form and 'duration' in request.form:
            cust_id = request.form['cust_id']
            book_id = request.form['book_id']
            duration = int(request.form['duration'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customers WHERE id =%s ',(cust_id,))
            customer =cursor.fetchone()
            cursor.execute('SELECT * FROM oldbook WHERE id =%s',(book_id,))
            oldbook = cursor.fetchone()
            if(oldbook and customer):
                if(oldbook['status'] == 'AVAILABLE'):
                    cursor.execute('INSERT INTO rentals(cust_id,book_id,due_time,total_price,staff_id) VALUES(%s,%s,  DATE_ADD(NOW(),INTERVAL %s DAY),%s,%s)',(cust_id,book_id,7*duration,oldbook['rental_price']*duration,staff['id']))
                    new_status = 'ON RENT'
                    cursor.execute('UPDATE oldbook SET status =%s where id = %s',(new_status,book_id,))
                    mysql.connection.commit()
                    msg = 'Succesfully added'
                else:
                    mysql.connection.commit()
                    msg = 'Current Book is not available for rent!'   
            else:
                mysql.connection.commit()
                msg = 'Invalid Customer Id ar Book ID !'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('process_rentals.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/rental_submission',methods=['GET','POST'])
def rental_submission():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'book_id' in request.form :
            book_id = request.form['book_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM oldbook WHERE id =%s',(book_id,))
            oldbook = cursor.fetchone()
            if(oldbook):
                if(oldbook['status'] == 'ON RENT' ):
                    cursor.execute('SELECT * FROM rentals WHERE book_id =%s AND status = %s',(book_id,'ACTIVE'))
                    rental =cursor.fetchone()
                    if(rental):
                        new_status = 'AVAILABLE'
                        new_status_rental = 'INACTIVE'
                        cursor.execute('UPDATE rentals SET status =%s , staff_id_submit =%s ,submission_time =CURRENT_TIMESTAMP where id = %s',(new_status_rental,staff['id'],rental['id'],))
                        cursor.execute('UPDATE oldbook SET status =%s where id = %s',(new_status,book_id,))
                        mysql.connection.commit()
                        msg = 'Succesfully submitted'
                    else:
                        mysql.connection.commit()
                        msg = 'No currently active Rental record found with given book id !'
                else:
                    mysql.connection.commit()
                    msg = 'Current Book is not on rent!'   
            else:
                mysql.connection.commit()
                msg = 'Invalid Book ID !'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('rental_submission.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/old_book_sales',methods=['GET','POST'])
def old_book_sales():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'cust_id' in request.form and 'book_id' in request.form :
            cust_id = request.form['cust_id']
            book_id = request.form['book_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customers WHERE id =%s ',(cust_id,))
            customer =cursor.fetchone()
            cursor.execute('SELECT * FROM oldbook WHERE id =%s',(book_id,))
            oldbook = cursor.fetchone()
            if(oldbook and customer):
                if(oldbook['status'] == 'AVAILABLE'):
                    cursor.execute('INSERT INTO sales_old(cust_id,book_id,staff_id) VALUES(%s,%s,%s)',(cust_id,book_id,staff['id']))
                    new_status = 'SOLD'
                    cursor.execute('UPDATE oldbook SET status =%s where id = %s',(new_status,book_id,))
                    mysql.connection.commit()
                    msg = 'Transaction Succesfull!'
                else:
                    mysql.connection.commit()
                    msg = 'Current Book is not already sold !'   
            else:
                mysql.connection.commit()
                msg = 'Invalid Customer Id ar Book ID !'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('old_book_sales.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route('/new_book_sales',methods=['GET','POST'])
def new_book_sales():
    if 'loggedin' in session:
        staff = session['user']
        msg = ''
        if request.method == 'POST' and 'cust_id' in request.form and 'book_id' in request.form :
            cust_id = request.form['cust_id']
            book_id = request.form['book_id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customers WHERE id =%s ',(cust_id,))
            customer =cursor.fetchone()
            cursor.execute('SELECT * FROM newbook WHERE id =%s',(book_id,))
            newbook = cursor.fetchone()
            if(newbook and customer):
                if(newbook['status'] == 'AVAILABLE'):
                    cursor.execute('INSERT INTO sales_new(cust_id,book_id,staff_id) VALUES(%s,%s,%s)',(cust_id,book_id,staff['id']))
                    new_status = 'SOLD'
                    cursor.execute('UPDATE newbook SET status =%s where id = %s',(new_status,book_id,))
                    mysql.connection.commit()
                    msg = 'Transaction Succesfull!'
                else:
                    mysql.connection.commit()
                    msg = 'Current Book is not already sold !'   
            else:
                mysql.connection.commit()
                msg = 'Invalid Customer Id ar Book ID !'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('new_book_sales.html',msg=msg,staff =staff)
    return redirect(url_for('login_staff'))

@app.route("/staff_profile")
def staff_profile():
    if 'loggedin' in session: 
        staff = session['user']
        return render_template("staff_profile.html",staff = staff)
    return redirect(url_for('login_staff')) 

@app.route("/customer_profile")
def customer_profile():
    if 'loggedin' in session: 
        customer = session['user']
        return render_template("customer_profile.html",customer = customer)
    return redirect(url_for('login_customer')) 

@app.route('/browse_old_books/',methods=['GET','POST'])
def browse_old_books():
    if 'loggedin' in session:
        customer = session['user']
        msg = ''
        if request.method == 'POST':
            title =  '%' + request.form['title'] + '%'
            author = '%' + request.form['author'] +'%'
            if(request.form['genre'] != 'All'):
                genre = request.form['genre']
            else:
                genre ='%%' 
            if(request.form['status'] != 'All'):
                status = request.form['status']
            else:
                status ='%%'
            if(request.form['edition']):
                edition = request.form['edition']
            else:
                edition ='%%'

            if(request.form['book_id']):
                book_id = request.form['book_id']
            else:
                book_id ='%%'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from oldbook WHERE id LIKE %s AND title LIKE %s AND author LIKE %s AND genre LIKE %s AND edition LIKE %s AND status LIKE %s ',(book_id,title ,author,genre,edition,status,))
            oldbooks = cursor.fetchall()
            # print(oldbooks)
            if(oldbooks):
                mysql.connection.commit()
                msg = 'Found ' + str(len(oldbooks)) +' book(s)'
            else:
                mysql.connection.commit()
                msg =  'No Such Book Found'
            return render_template("browse_old_books.html",customer=customer,msg=msg,oldbooks =oldbooks)
        return render_template("browse_old_books.html",customer=customer,msg=msg,oldbooks ='')

    return redirect(url_for('login_customer'))

@app.route('/browse_new_books/',methods=['GET','POST'])
def browse_new_books():
    if 'loggedin' in session:
        customer = session['user']
        msg = ''
        if request.method == 'POST':
            title =  '%' + request.form['title'] + '%'
            author = '%' + request.form['author'] +'%'
            if(request.form['genre'] != 'All'):
                genre = request.form['genre']
            else:
                genre ='%%' 
            if(request.form['status'] != 'All'):
                status = request.form['status']
            else:
                status ='%%'
            if(request.form['edition']):
                edition = request.form['edition']
            else:
                edition ='%%'

            if(request.form['book_id']):
                book_id = request.form['book_id']
            else:
                book_id ='%%'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from newbook WHERE id LIKE %s AND title LIKE %s AND author LIKE %s AND genre LIKE %s AND edition LIKE %s AND status LIKE %s ',(book_id,title ,author,genre,edition,status,))
            newbooks = cursor.fetchall()
            # print(oldbooks)
            if(newbooks):
                mysql.connection.commit()
                msg = 'Found ' + str(len(newbooks)) +' book(s)'
            else:
                mysql.connection.commit()
                msg =  'No Such Book Found'
            return render_template("browse_new_books.html",customer=customer,msg=msg,newbooks =newbooks)
        return render_template("browse_new_books.html",customer=customer,msg=msg,newbooks ='')

    return redirect(url_for('login_customer'))

@app.route('/customer_rentals/',methods=['GET','POST'])
def customer_rentals():
    if 'loggedin' in session:
        customer = session['user']
        msg = ''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT r.id as id ,r.book_id as book_id, o.title as title, o.author as author,o.genre as genre, o.edition as edition , r.total_price as total_price , r.issue_time as issue_time ,r.due_time as due_time ,r.submission_time as submission_time, r.status AS rental_status FROM oldbook AS o INNER JOIN rentals AS r ON r.book_id =o.id   WHERE r.cust_id =%s ORDER BY r.issue_time DESC',(customer['id'],) )
        customer_rentals = cursor.fetchall()
                        
        if(customer_rentals):
            mysql.connection.commit()
            msg = 'Found ' + str(len(customer_rentals)) +' rental(s)'
        else:
            mysql.connection.commit()
            msg =  'You do not have any Rentals yet!'
        return render_template("customer_rentals.html",customer=customer,msg=msg,customer_rentals = customer_rentals)
        
    return redirect(url_for('login_customer'))

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