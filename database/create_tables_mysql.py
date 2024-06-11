import mysql.connector
import subprocess
import configparser


# Read the configuration file
config = configparser.ConfigParser()
config.read("./configs/variables.config")

db_config = {
    "host": config.get("database", "host"),
    "user": config.get("database", "user"),
    "password": config.get("database", "password"),
    "port": config.get("database", "port"),
    "database": config.get("database", "database"),
    "table": config.get("database", "table"),
    "wait_timeout": config.get("database", "wait_timeout")
}

subprocess.call(["utils/wait-for-it.sh","-t", f"{db_config['wait_timeout']}", f"{db_config['host']}:{db_config['port']}"])
db_conn =  mysql.connector.connect(host=db_config["host"], user=db_config["user"], password=db_config["password"], port=db_config["port"], database=db_config["database"])
db_cursor = db_conn.cursor()


# This is temporary for development purposes, will be commented out in later iterations 
db_cursor.execute(f'''
                  DROP DATABASE IF EXISTS {db_config["database"]}
                  ''')
db_conn.commit()


db_cursor.execute(f'''
                  CREATE DATABASE {db_config["database"]}
                  ''')
db_cursor.execute(f'''
                  USE {db_config["database"]}
                  ''')
db_conn.commit()


db_cursor.execute(f'''
                  CREATE TABLE {db_config["table"]}
                  (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   original_url VARCHAR(250) NOT NULL,
                   short_url VARCHAR(5) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )                
                 ''')
db_conn.commit()


db_conn.close()