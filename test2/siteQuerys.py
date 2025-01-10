import mysql.connector
from mysql.connector import Error

def loadsites():
    db_config = {
        'host' : 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
        'user' : 'admin',
        'password': 'r7bvuOg7cx2frXJUDxOg',
        'port' : 3306,
        'database' : 'WX_DATA' 
''    }

    query = f"SELECT Name FROM Site;"

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        recordList = cursor.fetchall()
    except Error as e:
        print("issue grabbing records:", e)
    
    return recordList

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

def filetype(site,startdate,enddate):
    db_config = {
        'host': 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
        'user': 'admin',
        'password': 'r7bvuOg7cx2frXJUDxOg',
        'port': 3306,
        'database': 'WX_DATA'
    }

    # Prepare the SQL query with placeholders
    site_query = """
    SELECT DISTINCT SUBSTRING_INDEX(SiteInfo, '_', -1) AS FileType
    FROM `Data`
    WHERE TimeStamp BETWEEN %s AND %s
      AND SiteInfo LIKE %s;
    """

    # debug
    # site_query = """SELECT DISTINCT SUBSTRING_INDEX(SiteInfo, '_', -1) AS FileType FROM `Data` WHERE SiteInfo LIKE %s;"""

    # Define the parameters for the query
    start_date = startdate
    end_date = enddate
    site_param = f"%{site}%"  # Add wildcards for the LIKE operator

    try:
        # Establish the database connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query with parameters
        cursor.execute(site_query, (start_date, end_date, site_param))
        #debug
        # cursor.execute(site_query,(site_param,))

        # Fetch all records
        records = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the records
        print("From method call:", records)
        return records

    except Error as e:
        print("Issue connecting to the database:", e)
        return None

# want to make a csv file based upon the file type, site, start date and end date
def datadownload(site, start_date, end_date, filetype):
    # print("inside datadownload")
    # print("start date:",start_date)
    # print("end date: ", end_date)
    # print("site: ", site)
    # print("filetype: ", filetype)

    db_config = {
        'host': 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
        'user': 'admin',
        'password': 'r7bvuOg7cx2frXJUDxOg',
        'port': 3306,
        'database': 'WX_DATA'
    }

    site_query = """
   SELECT * 
   FROM `Data` 
   WHERE SiteInfo LIKE %s 
   AND SiteInfo LIKE %s 
   AND TimeStamp BETWEEN %s AND %s;
    """

    # Define the parameters for the query
    site_param = f"%_{site}_%"  # Add wildcards for the LIKE operator
    file_param = f"%_{filetype}%"

    try:
        # Establish the database connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query with parameters
        cursor.execute(site_query, (site_param, file_param, start_date, end_date))

        # Fetch all records
        values_tup = cursor.fetchall()
        

        # Close the cursor and connection
        cursor.close()
        connection.close()


    except Error as e:
        print("Issue connecting to the database:", e)
        return None

    # want to get the column names so we can use them for making the csv
    column_names = []
    for description in cursor.description:
        column_names.append(description[0])
    
    newlist = []
    for row in values_tup:  # iterate through each tuple in the values list
        for col, val in zip(column_names, row):  # Zip the columns with the current row
            if val is not None:  # if value is none we skip column and value
                newlist.append((col, val)) 
    # print(newlist)
    col_vals_dict = {}
    for tup in newlist:
        key, value = tup
        if key not in col_vals_dict:
            col_vals_dict[key] = []
        col_vals_dict[key].append(value)

    return col_vals_dict

def siteDesUnitsQuery(filetype, site):
    # print("des units: site:", site)
    # print("des units: filetype", filetype)

    des_type = "DailyDes_Units" 

    db_config = {
        'host': 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
        'user': 'admin',
        'password': 'r7bvuOg7cx2frXJUDxOg',
        'port': 3306,
        'database': 'WX_DATA'
    }

    site_query = f"""
    SELECT {des_type} From Site WHERE Name = %s;
    """
    site_query2 = "SELECT DailyDes_Units From Site WHERE Name = 'Atalaya';"

    try:
        # Establish the database connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query with parameters
        cursor.execute(site_query, (site,))
        # cursor.execute(site_query2)

        # Fetch all records
        dict_to_print = cursor.fetchone()
        

        # Close the cursor and connection
        cursor.close()
        connection.close()


    except Error as e:
        print("Issue connecting to the database:", e)
        return None
    cursor.close()
    connection.close()
    return dict_to_print

def latAndLong(site):
    db_config = {
    'host': 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'r7bvuOg7cx2frXJUDxOg',
    'port': 3306,
    'database': 'WX_DATA'
    }
    query = f'''SELECT Latitude, Longitude FROM Site WHERE Site.Name = '{site}';'''
    lat_long = []
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(query)
        lat_long = cursor.fetchone()
        cursor.close()
        connection.close()
    except Error as e:
        print("Issue connecting to the database:", e)
    lat_long_string = ['Latitude, Longitude' , str(lat_long[0]) +','+ str(lat_long[1])]
    return lat_long_string

def login(username, hashed_password):

    db_config = {
    'host': 'scwmp-db.cfagskq8wo4y.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'r7bvuOg7cx2frXJUDxOg',
    'port': 3306,
    'database': 'WX_DATA'
    }

    print("Username: ", username)
    print("Password hashed: ", hashed_password)

    query = '''SELECT * FROM login_table WHERE username = %s AND password = %s'''
    result = []

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
    except Error as e:
        print("Issue connecting to the database:", e)
    
    return result