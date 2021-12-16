import mysql.connector
import datetime
from utils import format_string

def database_connect():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='cli',
                                            user='root',
                                            password='admin')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("connected to database: ", record)

        return connection;

    except:
        print("error connecting to database")

def database_get_table():
    today = datetime.date.today()
    title = today.strftime("%d_%m_%Y");
    query  = "CREATE TABLE " + title 
    query += ''' (
                id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                country_name VARCHAR(255) NOT NULL,
                total_cases INT NOT NULL,
                total_deaths INT NOT NULL,
                new_cases INT NOT NULL,
                new_deaths INT NOT NULL,
                population INT NOT NULL
             ); '''

    try:
        db_connection = database_connect()
        cursor = db_connection.cursor()

        cursor.execute(query)
        print('table created')
        db_connection.commit()
    except:
        print("table already exists")

    return title;

def database_insert_to_table(title, data):
    db_connection = database_connect()
    cursor = db_connection.cursor()
    
    for obj in data:
        query  = "INSERT INTO " + title 
        query += "(country_name, total_cases, total_deaths, new_cases, new_deaths, population) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (obj.country_name, int(format_string(obj.total_cases)), int(format_string(obj.total_deaths)), int(format_string(obj.new_cases)), int(format_string(obj.new_deaths)), int(format_string(obj.population)))
        
        try:
            cursor.execute(query, val)    
            db_connection.commit();
        except:
            print("insert error")
    
    print('done');

def database_debug_table():
    db_connection = database_connect()
    cursor = db_connection.cursor()

    cursor.execute('SELECT * FROM test')
    rows = cursor.fetchall()
    for row in rows:
        print(row)