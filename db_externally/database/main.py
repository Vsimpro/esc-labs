import os, psycopg2 # pip install psycopg2-binary


# Global Variables
CONNECTION = None


def create_tables( tables : dict ) -> bool:
    """
    Create tables defined in the Tables dictionary.
    
    
    Parameters:
        dict : `tables` The dictionary should be of format 'name' -> 'query'

    Returns:
        bool: True on success, False on any error.
    """
    global CONNECTION
    
    
    try:
        cursor = CONNECTION.cursor()
        
        for table_name in tables:
            #
            #   Create the table
            #
            cursor.execute( tables[table_name] )
            print( "[DATABASE] [+] Table: ", table_name, "created" )           

        print( "[DATABASE] Ready." )
        CONNECTION.commit()
        cursor.close()

    except Exception as e:
        print( "[DATABASE] [!] Error when creating tables,", e )
        return False
    
    return True


def query_database( query : str, user_input : tuple = None ) -> list:
    """
    Run specified query in the Database.

    Parameters:
        str   : `query` the query to be ran agaisnt the DB.
        tuple : `user_input`: None, or the user specified parameters. 
    
    Returns:
        list: the results of the query.
    """
    
    global CONNECTION
    rows : list = []

    cursor = CONNECTION.cursor()
    
    try:
        
        if user_input:
            cursor.execute(query, user_input)
    
        else:
            cursor.execute(query)

    except Exception as e:
        print( f"[DATABASE] [!] Ran into an issue while running execute({ query }). Details: ", e )
        return False
    
    
    rows = cursor.fetchall()
    return rows
    

def insert_data( query:str, data ) -> bool:
    """
    Insert data into a table using premade queries.

    Parameters:
        str        : `query` the SQL insert query
        list,tuple : `data` the data to be inserted. Either as a tuple or as a list of tuples

    Returns:
        bool: Upon success
    """
    global CONNECTION

    try:
        
        cursor = CONNECTION.cursor()
        
        # List of tuples
        if type(data) == list:
            cursor.executemany( query, data )
            CONNECTION.commit()

        # Single tuple
        if type(data) == tuple:
            cursor.execute( query, data )
            CONNECTION.commit()

    except Exception as e:
        CONNECTION.rollback()
        print( f"[DATABASE] [!] Ran into an issue while running execute({ query }), with data {data}, details: ", e )
        return False
    
    return True


def update_data( query : str, data ) -> tuple:
    """
    Update data in a table using premade queries.

    Parameters
        str   : `query` the query to update the rows with
        tuple : `data` the data typle
    
    Returns:
        bool: Upon success
    """
    global CONNECTION
 
    try:
        cursor = CONNECTION.cursor()
        if type(data) == tuple:
            cursor.execute( query, data )

        CONNECTION.commit()
        print( f"[DATABASE] [?] Rows updated: { cursor.rowcount }" )

    except Exception as e:
        CONNECTION.rollback()
        print( f"[DATABASE] [!] Ran into an issue while running execute({ query }), with data {data}, details: ", e )
        return False
    
    return True


def initialize_db() -> bool:
    """
    Prepare the Database for use.

    Returns: 
        bool: Boolean upon success.
    """
    global CONNECTION

    db_address = "0.0.0.0:5432"
   
    try:        
        print( "[>] Connecting to database.")
        CONNECTION = psycopg2.connect(
                dbname   = "timing-labs",
                
                user     = "user",  
                password = "s3cur3_p4ss",  
                
                host = "0.0.0.0",      
                port = "5432"
            )
        print( "[>] Connection made " )
        
    except Exception as error:
        print(f"Error: {error}")
        return False

    return True