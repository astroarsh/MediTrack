import mysql.connector
conn=mysql.connector.connect(host="localhost",user="root",password="arshdeep12",database="arsh")
my_cursor=conn.cursor()

conn.commit()
conn.close()

print("Connection to MySQL DB successful")