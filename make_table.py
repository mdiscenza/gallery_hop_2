import mysql.connector
import csv

# Make RDS table and add rows from CSV file

cnx = mysql.connector.connect(user='galleryhop', password='galleryhop', host='galleryhop2.crflf9mu2uwj.us-east-1.rds.amazonaws.com',database='galleryhop2')

cursor = cnx.cursor()

t = """CREATE TABLE galleries_formatted(
shows	VARCHAR(50),
start_date	VARCHAR(50),
start	VARCHAR(50),
end	VARCHAR(50),
gallery	VARCHAR(50),
address	VARCHAR(50),
nbhood	VARCHAR(50),
end_date	VARCHAR(50))"""

cursor.execute(t)
cnx.commit()

f = open('data/galleries_table_date_formated.csv','rU') 
csv_f = csv.reader(f)

for row in csv_f:
	stmt = "INSERT INTO galleries_formatted (shows,start_date,start,end,gallery,address,nbhood,end_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(stmt,row)
	cnx.commit()


