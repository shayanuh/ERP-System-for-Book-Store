	DROP DATABASE IF EXISTS bharatreads;
    CREATE DATABASE IF NOT EXISTS bharatreads DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    USE BharatReads;
    
    CREATE TABLE IF NOT EXISTS customers(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
  	username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    contact_no char(10) ,
    PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS staff(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
  	username varchar(50) NOT NULL,
  	password varchar(255) NOT NULL,
    designation varchar(50) NOT NULL,
    contact_no char(10) ,
    PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS newbook(
    id int NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    author varchar(100) NOT NULL,
    edition int,
    genre varchar(100),
    status varchar(100) NOT NULL,
    sale_price int NOT NULL,
    PRIMARY KEY (id)
    );
    
    CREATE TABLE IF NOT EXISTS oldbook(
    id int NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    author varchar(100) NOT NULL,
    edition int,
    genre varchar(100),
    status varchar(100) NOT NULL,
    sale_price int NOT NULL,
    cost_price int NOT NULL,
    rental_price int NOT NULL,
    purchase_staff_id int NOT NULL,
    purchase_cust_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (purchase_staff_id) REFERENCES staff(id),
    FOREIGN KEY (purchase_cust_id) REFERENCES customers(id)
    );
    
    CREATE TABLE IF NOT EXISTS sales_old(
    id int NOT NULL AUTO_INCREMENT,
    book_id int NOT NULL,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    cust_id int NOT NULL,
    staff_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (cust_id) REFERENCES customers(id),
    FOREIGN KEY (book_id) REFERENCES oldbook(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
    );
    
    CREATE TABLE IF NOT EXISTS sales_new(
    id int NOT NULL AUTO_INCREMENT,
    book_id int NOT NULL,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    cust_id int NOT NULL,
    staff_id int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (cust_id) REFERENCES customers(id),
    FOREIGN KEY (book_id) REFERENCES newbook(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
    );
    
    CREATE TABLE IF NOT EXISTS rentals(
    id int NOT NULL AUTO_INCREMENT,
    cust_id int NOT NULL,
    book_id int NOT NULL,
    issue_time timestamp DEFAULT CURRENT_TIMESTAMP,
    due_time timestamp NOT NULL,
    submission_time timestamp ,
    total_price int NOT NULL,
    staff_id int NOT NULL,
    staff_id_submit int ,
    status varchar(100) ,
    PRIMARY KEY(id),
    FOREIGN KEY (cust_id) REFERENCES customers(id),
    FOREIGN KEY (book_id) REFERENCES oldbook(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id),
    FOREIGN KEY (staff_id_submit) REFERENCES staff(id)
    );
    INSERT INTO staff(name,username,password,designation,contact_no) VALUES('Shayan Ul Haq','shayan','123456','CEO', 8290709732); 
    
 