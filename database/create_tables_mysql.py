import mysql.connector
import subprocess

subprocess.call(["utils/wait-for-it.sh","-t", "90", "mydb:3306"])
db_conn =  mysql.connector.connect(host="mydb", user="root", password="root", port=3306)
db_cursor = db_conn.cursor()


# This is temporary for development purposes, will be commented out in later iterations 
db_cursor.execute('''
                  DROP DATABASE IF EXISTS url_shortener
                  ''')
db_conn.commit()


db_cursor.execute('''
                  CREATE DATABASE url_shortener
                  ''')
db_cursor.execute('''
                  USE url_shortener
                  ''')
db_conn.commit()


db_cursor.execute('''
                  CREATE TABLE url_mapping
                  (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   original_url VARCHAR(250) NOT NULL,
                   short_url VARCHAR(5) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )                
                 ''')
db_conn.commit()


db_conn.close()