import random, string

import database.main as db


def generate_email():
    email = ""
    characters = string.ascii_lowercase
    
    for _ in range( random.randint(8,20) ):
        index = random.randrange(0, len(characters))
        email += characters[index]
        
    email += "@example.com"
    
    return email


def load_database():
    emails : list = []
    
    #
    #   Generate noise 
    #
    for _ in range( 1000 ):
        emails.append( generate_email() )
        
    #
    #   Add known emails from wordlist
    #
    
    with open( "./wordlists/in_database.txt", "r" ) as file:
        for line in file.readlines():
            email = line.strip("\n")
            emails.append( email )
            
    #
    #   Insert emails into database.
    #
    
    db.initialize_db()
    
    table_exists = db.query_database("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    AND table_type='BASE TABLE';
    """
    )[ 0 ][ 0 ].lower() == "Emails".lower()
    
    # Emails exist from a previous run.
    if table_exists:
        return
    
    db.create_tables( { 
        "Emails" : """
            CREATE TABLE Emails ( 
                id    SERIAL PRIMARY KEY, 
                email TEXT NOT NULL --
            );""" 
    })
    
    insert_query =  """
        INSERT INTO Emails (
            email
        )
        VALUES (%s);          
    """
    
    db.insert_data(
        insert_query,
        [ (email,) for email in emails ]
    )
