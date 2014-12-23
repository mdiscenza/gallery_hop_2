import mysql.connector
import csv

# Make RDS table and add rows from CSV file

cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')

cursor = cnx.cursor()

t = """CREATE TABLE photos(
artist	VARCHAR(50),
photo	VARCHAR(5000))"""

cursor.execute(t)
cnx.commit()

urls = ['https://s3.amazonaws.com/galleryhop/copperwhite.jpg','https://s3.amazonaws.com/galleryhop/gitman.jpg','https://s3.amazonaws.com/galleryhop/silverstein.jpg']

artists = ['copperwhite','gitman','silverstein']

for i in range(0,len(urls)):
	stmt = "INSERT INTO photos (artist, photo) VALUES (%s,%s)"
	cursor.execute(stmt,(artists[i],urls[i]))
	cnx.commit()
