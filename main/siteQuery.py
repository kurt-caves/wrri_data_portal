import mysql.connector
from mysql.connector import Error

def sitequery(site):
    db_config = {
        'host' : 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
        'user' : 'admin',
        'password': 'r7bvuOg7cx2frXJUDxOg',
        'port' : 3306,
        'database' : 'WX_DATA' 
''    }

    site_query = f"SELECT * FROM Site WHERE Site.Name = %s;"
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        cursor.execute(site_query,(site,))
        record = cursor.fetchall()
        # print(record)
    except Error as e:
        print("issue connection to db", e)
    
    return record