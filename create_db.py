import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE web_scraping")
mycursor.execute("CREATE TABLE ebay_raw (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500), part_condition VARCHAR(50), soldprice FLOAT, sold_date DATE, bids VARCHAR(10), link VARCHAR(500))") 
mycursor.execute("CREATE TABLE ebuyer_raw (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500), price FLOAT, link VARCHAR(500), date DATE)") 
mycursor.execute("CREATE TABLE oc_raw (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(500), price FLOAT, link VARCHAR(500), date DATE)") 
